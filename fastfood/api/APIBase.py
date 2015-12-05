from fastfood import app, auth
from fastfood.business.db_business import RecipeBO, StepBO, RecipeItemBO, UserBO, UserLikeRecipeBO
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
parser.add_argument('user_id')
parser.add_argument('recipe_id')
parser.add_argument('action')
rbo = RecipeBO()
sbo = StepBO()
ribo = RecipeItemBO()
ubo = UserBO()
ulrbo = UserLikeRecipeBO()


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

    def get(self):

        args = parser.parse_args()
        user_id = args['user_id']
        return ubo.get(user_id)

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

        user = User(login=login, email=login, name=name, role=role)
        user.hash_password(password)
        
        try:
            ubo.register_new_user(user)
            return "User Registration successful"
        
        except Exception as e:
            raise e


class LikeRecipe(Resource):

    def post(self):

        args = parser.parse_args()

        user_id = args['user_id']
        recipe_id = args['recipe_id']
        action = args['action']

        try:
            if action == 'like':
                ulrbo.like_recipe(user_id, recipe_id)
            else:
                ulrbo.remove_like(user_id, recipe_id)

        except Exception as e:
            raise e

        finally:
            return 'Action successful', 200


class UserLikes(Resource):
    # possible alternative: return the whole recipes instead of ids
    def get(self):

        args = parser.parse_args()
        user_id = args['user_id']

        try:
            likes = ulrbo.get_user_likes(user_id)
        except Exception as e:
            raise e
        finally:
            return likes


class RecipeLikes(Resource):
    
    def get(self):

        args = parser.parse_args()
        recipe_id = args['recipe_id']

        try:
            ids = ulrbo.get_recipe_likes(recipe_id)
        except Exception as e:
            raise e
        finally:
            return ids


api.add_resource(Recipes,
        '/api/v1/recipes/',
        '/api/v1/recipes/<recipe_id>/',
        '/api/v1/recipes/items/')

api.add_resource(Users,
                 '/api/v1/users/')

api.add_resource(LikeRecipe,
                 '/api/v1/likerecipe/')

api.add_resource(UserLikes,
                 '/api/v1/userlikes/')

api.add_resource(RecipeLikes,
                 '/api/v1/recipelikes/')
# /recipes/items/?items=list,of,items,to,be,searched&restrict=true/false


@app.route('/api/v1/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(1500)

    return jsonify({'token': token.decode('ascii'), 'duration': 1500,
                    'user': {'name': g.user.name,
                             'id': g.user.id,
                             'role': g.user.role,
                             'email': g.user.email}})
