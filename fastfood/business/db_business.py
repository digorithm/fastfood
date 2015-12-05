# -*- encoding: utf-8 -*-

from fastfood.models.db import Recipe, Step, RecipeItem, User, UserLikeRecipe
import json
from fastfood.business.base import CrudBO
from fastfood.utils import _extract_selections, basic_food
from flask import g
from fastfood import auth
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


class RecipeBO(CrudBO):

    model = Recipe
    model_selections = ['id', 'title', 'rating', 'author', 'complexity',
                        'description']

    # TODO: create logic to extract author and complexity
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
                sbo = StepBO()
                sbo._create(s)
            for ingredient in recipe['ingredients']:
                item = RecipeItem()
                item.recipe_id = obj_id
                item.ingredient = ingredient.strip()
                ribo = RecipeItemBO()
                ribo._create(item)
            return obj_id

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
            return {'error': 'No recipe found'}
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

        selections = _extract_selections(obj, self.model_selections)

        self._session.close()

        return selections

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
                            match += 1
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


class UserBO(CrudBO):

    model = User
    model_selections = ['name', 'login', 'password', 'email', 'role']

    def check_login(self, login):

        obj = self._session.query(User)\
                  .filter(self.model.login == login).first()
        self._session.close()
        return obj

    @auth.verify_password
    def verify_password(username_or_token, password):
 
        userbo = UserBO()
        user = userbo.verify_auth_token(username_or_token)
        if not user:
            user = userbo._session.query(User)\
                         .filter(User.login == username_or_token).first()
            if not user or not user.verify_password(password):
                return False
        g.user = user
        userbo._session.close()
        return True

    @staticmethod
    def verify_auth_token(token):
        key = 'the quick brown fox jumps over the lazy dog'
        userbo = UserBO()
        s = Serializer(key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = userbo._session.query(User)\
                     .filter(User.id == data['id']).first()
        userbo._session.close()
        return user

    def register_new_user(self, User):
        return self._create(User)


class UserLikeRecipeBO(CrudBO):

    model = UserLikeRecipe
    model_selections = ['recipe_id', 'user_id']

    def get_user_likes(self, user_id):

        query = self._session.query(self.model)\
                    .filter(self.model.user_id == user_id)

        recipes = self._list(query=query)

        likes = [recipe['recipe_id'] for recipe in recipes]

        return likes

    def get_recipe_likes(self, recipe_id):

        query = self._session.query(self.model)\
                    .filter(self.model.recipe_id == recipe_id)

        users = self._list(query=query)

        ids = [user['user_id'] for user in users]
        return ids

    def like_recipe(self, user_id, recipe_id):
        obj = UserLikeRecipe(user_id=user_id, recipe_id=recipe_id)
        return self._create(obj)

    def remove_like(self, user_id, recipe_id):

        query = self._session.query(self.model)\
                    .filter(self.model.user_id == user_id,
                            self.model.recipe_id == recipe_id)
        return self._delete(query)
