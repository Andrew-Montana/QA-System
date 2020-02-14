from flask import Flask, request, render_template
from SPARQLWrapper import SPARQLWrapper, JSON
import string
import osmapi
from PatternIdentifier import PatternIdentifier
from ConceptIdentifier import ConceptIdentifier
from QueryBuilder import QueryBuilder
from QueryExecutor import QueryExecutor
from EntitiesIdentifier import EntitiesIdentifier

app = Flask(__name__)

@app.route('/')
def index():
	return render_template("index.html", message = "")


@app.route('/send', methods=['GET','POST'])
def send():
	if request.method == 'POST':
		text = request.form['search'] # text

	patternIdC = PatternIdentifier(text) # 1 Component
	conceptIdC = ConceptIdentifier(text) # 2 Component
	entityIdC = EntitiesIdentifier(text) # 3 Component

	questionIndex = patternIdC.GetPattern() # int number or None
	concepts = conceptIdC.GetConcept()		# None or [[string key, string value]] or None
	entities = entityIdC.GetEntity()		# ([string text, string label]) or None

	print("###")
	print("CONCEPTS:")
	print(concepts)
	print("ENTIEIS")
	print(entities)
	print("INDEX")
	print(questionIndex)
	print("###")
	# 4 Component. Query Builder
	queryBuilderC = QueryBuilder(questionIndex,concepts,entities)
	query = queryBuilderC.GetQuery()
	# 5 Component. Query Executor
	try:
		queryExecutorC = QueryExecutor(query) 
		response = queryExecutorC.ExecuteQuery()
		return render_template("overpassResult.html", result = response, questionIndex = questionIndex, resultLen = len(response.nodes) ) 
	except Exception as e:
		print("#Error inside of Query Executor")
		print(e)
		return render_template("index.html")
		#print message later
		#use validation as separated component later


if __name__ == "__main__":
	app.run()