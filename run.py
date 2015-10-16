# Run a test server.
from fastfood import app
from fastfood.business.db_business import RecipeBO, StepBO, RecipeItemBO
import json 

#rbo = RecipeBO()
#f = open("output2.json")
#rbo.save_extracted_data(f.read())

# running the app now with gunicorn run:app
#app.run(host='0.0.0.0', port=8080, debug=True)

#ribo = RecipeItemBO()

#ribo.filter_by_items(['ovo', 'chocolate'])

#recipes = rbo.list_recipes_by_items(['ovo', 'chocolate'])
#print json.dumps(recipes)

@app.route('/')
def api_base():
	return 'hello'
