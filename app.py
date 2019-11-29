from flask import Flask, request, render_template
from SPARQLWrapper import SPARQLWrapper, JSON
import string
import osmapi
import overpy
from ValidationModule import ValidationModule
from NltkModule import NltkModule
app = Flask(__name__)

@app.route('/')
def index():
	return render_template("index.html", message = "")


@app.route('/send', methods=['GET','POST'])
def send():
	if request.method == 'POST':
		text = request.form['search']

		validInstance = ValidationModule()
		validResponse = validInstance.check_valid(text)
		isValid = True if validResponse != 0 else False 	# a if condition else b - syntax

		if isValid == True:
			api = overpy.Overpass()
			nltkInstance = NltkModule(text)
			nltkResponse = nltkInstance.GetResponse(validResponse)
			
			result = ""
			if nltkResponse != "error":
				result = api.query(nltkResponse)
				return render_template("overpassResult.html", result = result, questionIndex = validResponse, resultLen = len(result.nodes) ) 
				#return render_template("nltkTest.html", nltkList = nltkResponse ) 
			else:
				return("error")
		else:
			return render_template("index.html", message = "Try to ask something else") 
	return("no post")


if __name__ == "__main__":
	app.run()