from . import BaseTestCase
from fastfood.business.db_business import RecipeBO
import ujson as json


class DBBusinessTestCase(BaseTestCase):

    def first_test(self):
        self.assertEqual(1, 1)

    def test_save_extracted_data(self):
        recipe_bo = RecipeBO()

        data = [{
                "title": "test recipe",
                "steps": [
                    "step 1",
                    "step 2",
                    "step 3"
                ],
                "ingredients": [
                    "ingredient 1",
                    "ingredient 2",
                    "ingredient 3"
                ]
                }]

        with open('data.json', 'w') as fp:
            json.dump(data, fp)

        f = open("data.json")
        data_id = recipe_bo.save_extracted_data(f.read())

        recipe = recipe_bo.list_full_recipe_by_id(data_id)

        self.assertEqual(recipe['title'], data[0]['title'])
        self.assertEqual(recipe['ingredients'], data[0]['ingredients'])
        self.assertEqual(recipe['steps'], data[0]['steps'])
