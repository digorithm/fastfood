from fastfood import app
from fastfood.business.db_business import RecipeBO, StepBO, RecipeItemBO
import json
from flask_restful import Resource, Api

api = Api(app)

rbo = RecipeBO()
sbo = StepBO()
ribo = RecipeItemBO()

class Recipes(Resource):
    def get(self, recipe_id=None):
        if recipe_id is None:
            return rbo.list_full_recipes()
        return rbo.list_full_recipe_by_id(recipe_id)

api.add_resource(Recipes,
        '/api/v1/recipes/',
        '/api/v1/recipes/<recipe_id>/')

