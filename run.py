# Run a test server.
from fastfood import app
from fastfood.business.db_business import RecipeBO, StepBO, RecipeItemBO
import json

rbo = RecipeBO()
f = open("items.json")
rbo.save_extracted_data(f.read())

# running the app now with gunicorn run:app

#ribo = RecipeItemBO()

#ribo.filter_by_items(['ovo', 'chocolate'])

#recipes = rbo.list_recipes_by_items(['ovo', 'chocolate'])
#print json.dumps(recipes)

#if __name__ == '__main__':
#	app.run(debug=True)
