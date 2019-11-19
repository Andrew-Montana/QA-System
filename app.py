from flask import Flask, request, render_template
from SPARQLWrapper import SPARQLWrapper, JSON
import string
import osmapi
import overpy
import nltk
from nltk.corpus import treebank

app = Flask(__name__)

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

def nltk_check(tags, isTwo):
	kol = 0
	nnpKol = 0
	for i,j in tags:
		if (j == "NN"):
			kol = kol + 1
		if (j == "NNS"):
			kol += 1
		if (j == "NNP"):
			nnpKol += 1
	# if we work only with NNP
	if isTwo == False:
		if(nnpKol == 0):
			return "error"
	# if we work with nnp and nn/nns simultaniously
	if isTwo == True:
		if(kol == 0):
			return "error"
		if(nnpKol == 0):
			return "error"

	return "ok"

def nltk_dictMultiple(tags):
	nltkList = dict()
	tmpList = list()
	for i,j in tags:
		if j == "NNP":
			tmpList.append(i)

	nltkList["NNP"] = " ".join(tmpList)
	return nltkList

def nltk_dict(tags):
	nltkList = dict()
	for i,j in tags:
		if(j == "NNP"):
			nltkList["NNP"] = i
		if(j == "NN"):
			nltkList["NN"] = i
		if(j == "NNS"):
			nltkList["NNS"] = i
	return nltkList

def nltk_showme(text, isTwo):
	# if show me <location< in <city>
	sentence = text
	tokens = nltk.word_tokenize(sentence)
	tags = nltk.pos_tag(tokens)
	ent = nltk.chunk.ne_chunk(tags)

	checkResponse = nltk_check(tags, isTwo)
	if(checkResponse == "error"):
		return "error"

	nltkList = nltk_dict(tags)
	return nltkList

def nltk_whatIsAddress(text, isTwo):
	# (What is address(NN) of <amenity>?) // extend later with nnps and nns. Could be multiple NNPs because of its one name
	# Caffe Bene, Bobamosa, Bouchon Backery,
	sentence = text
	tokens = nltk.word_tokenize(sentence)
	tags = nltk.pos_tag(tokens)
	ent = nltk.chunk.ne_chunk(tags)
	# remove address as NN
	for i in tags:
		for j in range(0,2):
			if(i[j].lower() == "address"):
				tags.remove(i)
    #
	checkResponse = nltk_check(tags, isTwo)
	if(checkResponse == "error"):
		return "error"

	# because of possible NNPs we use another function. In future need to improve this implementation
	nltkList = nltk_dictMultiple(tags)
		
	return nltkList

def actionSomewhere(text):
	#I would like to <action>(check from amenity) somewhere. Extend later, maybe use wants to eat and sleep somewhere.
	#actionList = list(["eat","watch","dance","sleep","drink","relax"])

	# Make better later, like loop available actions and retrieve amenities from somekinda list array etc
	#for item in actionList:
	#	if item in text:
	amenity = ""
	if "eat" in text:
		amenity = "restaurant"
	if "watch" in text:
		amenity = "cinema"
	if "dance" in text:
		amenity = "nightclub"
	if "drink" in text:
		amenity = "drinking_water"
	if "relax" in text:
		amenity = "cinema"




@app.route('/send', methods=['GET','POST'])
def send():
	if request.method == 'POST':
		text = request.form['search']
		isValid = check_valid(text)
		if isValid[0] == True:
			api = overpy.Overpass()
			nltkResponse = ""
			query = ""
			questionIndex = 0
			if(isValid[1] == 1):
				nltkResponse = nltk_showme(text, True)
				questionIndex = 1
				query = f"""[out:json];area[name = "{nltkResponse["NNP"]}"]; node(area)[amenity={nltkResponse["NN"]}]; out;"""
			elif(isValid[1] == 2):
				nltkResponse = nltk_whatIsAddress(text, False)
				questionIndex = 2
				query = f"""[out:json];area[name = "New York"]; node(area)[name="{nltkResponse["NNP"]}"]; out;"""
			elif(isValid[1] == 3):
				nltkResponse = actionSomewhere(text)
			#elif(isValid[1] == 4):
			#	nltkResponse = nltk_showme(text)

			print(nltkResponse)
			
			if len(query) != 0:
				result = api.query(query)
			if nltkResponse != "error":
				return render_template("overpassResult.html", result = result, questionIndex = questionIndex ) 
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

	# 2 (What is address(NN) of <place>(NN - now is this)(NN,NNP)?)
	if (text.startswith("what is address of")):
		return list([True,2])
	# 3 Tell me the openning hours of <place>.
	#if text.startswith("tell me the openning hours of"):
	#	return True;
	# 4 I would like to <action> somewhere.
	if text.startswith("i would like to"):
		return list([True,3])
	# where is <city>
	if text.startswith("where is"):
		return list([True,4])


if __name__ == "__main__":
	app.run()