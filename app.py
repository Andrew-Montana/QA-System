from flask import Flask, request, render_template
from SPARQLWrapper import SPARQLWrapper, JSON
import string
import osmapi
import overpy
#import stanfordnlp

app = Flask(__name__)
patterns = list(["how many people live in the city named","when was","born"])

@app.route('/')

def index():
        return render_template("index.html")

def resultName(name):
	name = string.capwords(name)
	sparql = SPARQLWrapper("http://dbpedia.org/sparql")
	sparql.setQuery("""
	    PREFIX dbo: <http://dbpedia.org/ontology/>
	PREFIX foaf: <http://xmlns.com/foaf/0.1/>
	select ?person ?birthDate ?abstract
	where {
	  ?person foaf:name \""""+name+"""\"@en.
	  ?person a foaf:Person.
	  ?person dbo:birthDate ?birthDate .
	  ?person dbo:abstract ?abstract .
	  FILTER (lang(?abstract) = 'en')
	}""")
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()

	resultList = list()
	for result in results["results"]["bindings"]:
		resultList.append([
			  result["person"]["value"],
			  result["birthDate"]["value"],
			  result["abstract"]["value"]
			])
	return resultList

def resultPopulation(city):
	city = string.capwords((city.replace(patterns[0],"")).strip())
	sparql = SPARQLWrapper("http://dbpedia.org/sparql")
	sparql.setQuery("""
    PREFIX db: <http://dbpedia.org/>
	PREFIX dbp: <http://dbpedia.org/property/>
	PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
	PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
	PREFIX dbo: <http://dbpedia.org/ontology/> 
	PREFIX dbr: <http://dbpedia.org/resource/> 
    SELECT * 
	WHERE { ?s rdfs:label \""""+city+"""\" @en . 
	  ?s dbo:populationTotal ?numberOfInhabitants . }""")
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()

	resultList = list()
	for result in results["results"]["bindings"]:
		resultList.append([
			  result["numberOfInhabitants"]["value"],
			  result["numberOfInhabitants"]["value"],
			  result["numberOfInhabitants"]["value"]
			])

	return resultList

def send22():
	if request.method == 'POST':
		search = request.form['search'].lower()
		# Population pattern
		if search.startswith(patterns[0]):
			answer_response = resultPopulation(search)
			return render_template('result.html', len=len(answer_response), resultList = answer_response, flag = False)
		# Person Born pattern
		elif search.startswith(patterns[1]) and patterns[2] in search:
			text = search
			start = text.find(patterns[1]) + len(patterns[1])
			end = text.find(patterns[2], start)
			text = text[start:end].strip()
			answer_response = resultName(text)
			# if multiple answers
			if len(answer_response) > 1:
				return render_template('result.html', len=len(answer_response), resultList = answer_response, flag = True)
			return render_template('result.html', len=len(answer_response), resultList = answer_response, flag = False)
		
		
	return render_template('index.html')

@app.route('/send', methods=['GET','POST'])
def send():
	if request.method == 'POST':
		text = request.form['search'].lower()
		isValid = check_valid(text)
		if isValid == True:
			nltk()
		#
		answer = ("ANSWER is " + str(isValid))
		return(answer)
	return("no post")

def check_valid(text):
	# 1.1 (Show me <location> that are/is close to <location>.)
	if (text.startswith("show me") and "that are close to" in text) or ((text.startswith("show me") and "that is close to" in text)):
		return True;
	# 1.2 (Show me <location>)
	else if text.startswith("show me"):
		return True;

	# 2 (What is <address> of <place>?)
	if (text.startswith("what is") and "of" in text):
		return True;
	# 3 Tell me the openning hours of <place>.
	if text.startswith("tell me the openning hours of"):
		return True;
	# 4 I would like to <action> somewhere.
	if text.startswith("i would like to"):
		return True;


if __name__ == "__main__":
	app.run()