from fastfood import app
from fastfood.business.db_business import RecipeBO, StepBO, RecipeItemBO
import json
from flask_restful import Resource, Api, reqparse
from flask import request

api = Api(app)

rbo = RecipeBO()
sbo = StepBO()
ribo = RecipeItemBO()

class Recipes(Resource):

    def get(self, recipe_id=None):
        
        # check if it was passed items to be filtered
        if 'items' in request.args:
            items = request.args['items'].split(',')

            # check if the ingredients are restrict
            if 'restrict' in request.args:
                restrict = True
                return rbo.list_recipes_by_items(items, restrict)

            return rbo.list_recipes_by_items(items)

        # if nothing specified, return the big list
        if recipe_id is None:
            return rbo.list_full_recipes()

        # check if specific recipe was requested
        return rbo.list_full_recipe_by_id(recipe_id)

api.add_resource(Recipes,
        '/api/v1/recipes/',
        '/api/v1/recipes/<recipe_id>/',
        '/api/v1/recipes/items/')
# /recipes/items/?items=list,of,items,to,be,searched&restrict=true/false
