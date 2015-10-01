# -*- encoding: utf-8 -*-

from fastfood.models.db import Recipe, Step, RecipeItem
import json
from fastfood.business.base import CrudBO
from fastfood.utils import _extract_selections, basic_food 


class RecipeBO(CrudBO):

    model = Recipe
    model_selections = ['id', 'title', 'rating', 'author', 'complexity', 'description']

    def save_extracted_data(self, jsonfile):
        """
        get extracted json data and build a object to send to the
        database
        """ 
        data = json.loads(jsonfile)
        for recipe in data:
            rec = Recipe()
            rec.title = recipe['title']
            rec.description = 'No description yet'
            rec.author = 1
            rec.complexity = 1
            obj_id = self._create(rec, return_id=True)
            for step in recipe['steps']:
                s = Step()
                s.recipe_id = obj_id
                s.description = step
                self._create(s)
            for ingredient in recipe['ingredients']:
                item = RecipeItem()
                item.recipe_id = obj_id
                item.ingredient = ingredient.strip()
                self._create(item)
    
    def list_full_recipes(self):
        ribo = RecipeItemBO()
        sbo = StepBO()
        recipes = self.list()
        for recipe in recipes:
            items_list = []
            steps_list = []
            recipe_items = ribo.filter_by_recipe_id(recipe['id'])
            recipe_steps = sbo.filter_by_recipe_id(recipe['id'])
            for item in recipe_items:
                items_list.append(item['ingredient'])
            for step in recipe_steps:
                steps_list.append(step['description'])
            recipe['ingredients'] = items_list
            recipe['steps'] = steps_list
        return recipes

    def list_full_recipe_by_id(self, recipe_id):
        ribo = RecipeItemBO()
        sbo = StepBO()
        recipe = self.filter_by_id(recipe_id)
        # TODO: proper exception handling, this is such a tech debt
        if not recipe:
            return {'error':'No recipe found'}
        items_list = []
        steps_list = []
        recipe_items = ribo.filter_by_recipe_id(recipe['id'])
        recipe_steps = sbo.filter_by_recipe_id(recipe['id'])

        for item in recipe_items:
            items_list.append(item['ingredient'])
        for step in recipe_steps:
            steps_list.append(step['description'])
        recipe['ingredients'] = items_list
        recipe['steps'] = steps_list

        return recipe 

    def filter_by_id(self, recipe_id):

        obj = self._session.query(Recipe)\
                .filter(self.model.id == recipe_id).first()
        return _extract_selections(obj, self.model_selections)
    
    
    def list_recipes_by_items(self, items, restrict=False):
        """
        This is kinda tricky. We have 2 modes:
        1. Browsing Mode

        The Broswing Mode the user will receive any recipe that has those
        required items (but has other items as well). This is useful in 
        cases such as users wanting to browse through recipes without 
        knowing exactly all ingredients

        2. Restrict Mode

        The Restrict Mode will retrieve only recipes that use only
        those specific items PLUS some items that I called 'basic food'
        such as water, oil, paper and stuffs. This way a recipe that uses
        only beans, rice and water, will be retrieve even if the user
        searched for beans and rice
        """
        items = [item.lower() for item in items]
        recipes = []
        ribo = RecipeItemBO()
        recipe_ids = ribo.filter_by_items(items)
        for recipe_id in recipe_ids:
            recipe = self.list_full_recipe_by_id(recipe_id)
            recipes.append(recipe)
        
        if restrict:
            recipes_match = []
            total_matches = 0
            for idx, rec in enumerate(recipes):
                match = 0
                for ing in rec['ingredients']:
                    for basic_item in basic_food:
                        if basic_item in ing.lower():
                            match +=1
                    for item in items:
                        if item in ing.lower():
                            match += 1
                if match >= len(rec['ingredients']):
                    # found a match
                    recipes_match.append(rec)
                    total_matches += 1
            return recipes_match

        return recipes


class StepBO(CrudBO):

    model = Step
    model_selections = ['recipe_id', 'description']
    def filter_by_recipe_id(self, recipe_id):

        query = self._session.query(Step)\
                .filter(self.model.recipe_id == recipe_id)
        return self._list(query=query)

class RecipeItemBO(CrudBO):

    model = RecipeItem
    model_selections = ['recipe_id', 'ingredient']
    
    def filter_by_recipe_id(self, recipe_id):

        query = self._session.query(RecipeItem)\
                .filter(self.model.recipe_id == recipe_id)
        return self._list(query=query)

    def filter_by_items(self, items):
        result = []
        for i in items:
            query = self._session.query(RecipeItem)\
                    .filter(self.model.ingredient.like("%"+i+"%"))\
                    .group_by(self.model.recipe_id)
            partial_result = self._list(query=query, limit=None)
            for res in partial_result:
                if res['recipe_id'] not in result:
                    result.append(res['recipe_id'])
        return result
