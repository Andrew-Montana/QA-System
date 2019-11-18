from flask import Flask, request, render_template
from SPARQLWrapper import SPARQLWrapper, JSON
import string
import osmapi
import overpy
import nltk
from nltk.corpus import treebank

app = Flask(__name__)
patterns = list(["how many people live in the city named","when was","born"])

@app.route('/')

def index():
	#api = overpy.Overpass()
	#result = api.query("""[out:json];area[name = "Berlin"]; node(area)[amenity=restaurant]; out;""")
	#api = overpy.Overpass()
# fetch all ways and nodes
	#result = api.query("""node [amenity=restaurant](11.904373,51.717910,12.036896,51.782950);out;""")
	#result = api.query("""node [name=drinking_water](12.342453,41.784658,12.634964,41.996786);out;""")
	#result = api.query("[out:json];node[amenity=restaurant](12.318420,41.763919,12.663116,42.025611);out;")
	##result = api.query("""[out:json];area[name = "New York"]; node(area)[amenity=restaurant]; out;""")
	#print(len(result.nodes))
	#print(len(result.ways))
	#print(result)
	return render_template("index.html")#, result = result)

def nltk_showme(text):
	sentence = text
	tokens = nltk.word_tokenize(sentence)
	tags = nltk.pos_tag(tokens)
	ent = nltk.chunk.ne_chunk(tags)

	#
	print(tokens)
	print(tags)
	print(ent)
	kol = 0
	nnpKol = 0
	for i,j in tags:
		if (j == "NN"):
			kol = kol + 1
		if (j == "NNS"):
			kol += 1
		if (j == "NNP"):
			nnpKol += 1

	if(kol == 0):
		return "error"
	if(nnpKol == 0):
		return "error"

	# if show me <location< in <city>
	nltkList = dict()
	for i,j in tags:
		if(j == "NNP"):
			nltkList["NNP"] = i#nltkList.append(i)
		if(j == "NN"):
			nltkList["NN"] = i#
		if(j == "NNS"):
			nltkList["NNS"] = i#
	return nltkList

#def nltk_whatIsAddress(text):

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
		text = request.form['search']
		isValid = check_valid(text)
		if isValid[0] == True:
			nltkResponse = ""
			if(isValid[1] == 1):
				nltkResponse = nltk_showme(text)
			#elif(isValid[1] == 2):
			#	nltkResponse = nltk_whatIsAddress(text)
			#elif(isValid[1] == 3):
			#	nltkResponse = nltk_showme(text)
			#elif(isValid[1] == 4):
			#	nltkResponse = nltk_showme(text)

			print(nltkResponse)
			api = overpy.Overpass()
			query = f"""[out:json];area[name = "{nltkResponse["NNP"]}"]; node(area)[amenity={nltkResponse["NN"]}]; out;"""
			print(query)
			result = api.query(query)
			if nltkResponse != "error":
				return render_template("overpassResult.html", result = result ) 
				#return render_template("nltkTest.html", nltkList = nltkResponse ) 
	return("no post")

def check_valid(text):
	# 1.1 (Show me <location> that are/is close to <location>.)
	#if (text.startswith("show me") and "that are close to" in text) or ((text.startswith("show me") and "that is close to" in text)):
	#	return True;
	# 1.2 (Show me <location> in <city>)
	#elif
	text = text.lower()

	if text.startswith("show me"):
		return list([True,1])

	# 2 (What is <address> of <place>?)
	if (text.startswith("what is") and "of" in text):
		globalNltkIndex = 2
		return list([True,2])
	# 3 Tell me the openning hours of <place>.
	#if text.startswith("tell me the openning hours of"):
	#	return True;
	# 4 I would like to <action> somewhere.
	if text.startswith("i would like to"):
		globalNltkIndex = 3
		return list([True,3])
	# where is <city>
	if text.startswith("where is"):
		globalNltkIndex = 4
		return list([True,4])


if __name__ == "__main__":
	app.run()