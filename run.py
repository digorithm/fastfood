# Run a test server.
from fastfood import app
from fastfood.business.db_business import RecipeBO, StepBO, RecipeItemBO

#f = open("output.json")
#rbo.save_extracted_data(f.read())
app.run(host='0.0.0.0', port=8080, debug=True)

