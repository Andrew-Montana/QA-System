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

	questionIndex = patternIdC.GetPattern()
	concepts = conceptIdC.GetConcept()
	entities = entityIdC.GetEntity()
	print("question index: " + str(questionIndex))
	print("concepts: " + str(concepts))
	print("concepts: " + str(entities))
	print("entity: " + str(entities[0]))
	# 4 Component. Query Builder
	queryBuilderC = QueryBuilder(questionIndex,concepts,entities)
	query = queryBuilderC.GetQuery()

	#
	print("1 component: " + str(questionIndex))
	print("2 component: " + str(concepts))
	print("3 component: " + str(entities))
	print("4 component: " + str(query))
	# 5 Component. Query Executor
	queryExecutorC = QueryExecutor(query) 
	response = queryExecutorC.ExecuteQuery()

	#
	return render_template("overpassResult.html", result = response, questionIndex = questionIndex, resultLen = len(response.nodes) ) 



if __name__ == "__main__":
	app.run()