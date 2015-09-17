from fastfood.models.db import Recipe, Step, RecipeItem
import json
from fastfood.business.base import CrudBO
from fastfood.utils import _extract_selections 


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
