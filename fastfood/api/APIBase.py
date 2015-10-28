from fastfood import app, auth
from fastfood.business.db_business import RecipeBO, StepBO, RecipeItemBO, UserBO
from fastfood.models.db import User
import json
from flask_restful import Resource, Api, reqparse, abort
from flask import request, g, jsonify


api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('login')
parser.add_argument('password')
parser.add_argument('role')
parser.add_argument('name')
rbo = RecipeBO()
sbo = StepBO()
ribo = RecipeItemBO()
ubo = UserBO()

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


class Users(Resource):

    def post(self):
        args = parser.parse_args()
        login = args['login']
        password = args['password']
        name = args['name']
        role = args['role']
        if login is None or password is None:
            # TODO: raise proper exception
            abort(400) # missing arguments
        if ubo.check_login(login) is not None:
            # TODO: raise proper exception
            abort(400) # existing user

        user = User(login = login, email = login, name = name, role = role)
        user.hash_password(password)
        
        try:
            ubo.register_new_user(user)
            return "User Registration successful"
        
        except Exception as e:
            raise e

api.add_resource(Recipes,
        '/api/v1/recipes/',
        '/api/v1/recipes/<recipe_id>/',
        '/api/v1/recipes/items/')

api.add_resource(Users,
                 '/api/v1/users/')
# /recipes/items/?items=list,of,items,to,be,searched&restrict=true/false


@app.route('/api/v1/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(1500)
    return jsonify({'token': token.decode('ascii'), 'duration': 1500})
