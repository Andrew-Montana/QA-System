import spacy
import io
import json
import string
from spacy.matcher import Matcher

class ConceptIdentifier:

	def __init__(self, text):
		#private variables
		self.__start = None

		self.__sentence = text
		self.__patterns = self.__GetPatterns()
		self.__nlp = spacy.load("en_core_web_sm", disable=['parser','ner'])
		self.__matcher = Matcher(self.__nlp.vocab)
		# Load Patterns
		self.__LoadPatterns()
		# Identify
		self.__concepts = self.Identify()

	def GetStartIndex(self):
		return self.__start

	def __GetPatterns(self): # Get json data with patterns
		try:
			with open('features/patterns.json') as data_file:
				return json.load(data_file)
		except:
			print("#Error. There is no patterns.json file found")
			return None


	def __LoadPatterns(self): # Split json data to Key-Value and load it to the Matcher engine
		if self.__patterns != None:
			for item in self.__patterns:
				pattern = item[1]
				ID = item[0][0]
				self.__matcher.add(ID, None, *pattern)
		else:
			print("#Error. Patterns cannot be loaded. String is empty ")

	def GetConcept(self):
		return self.__concepts # None or [[key,value]..]

	def Identify(self):
		try:
			concepts = list()
			#
			doc = self.__nlp(self.__sentence.lower()) # making text in lower case
			# matches
			matches = self.__matcher(doc)
			for match_id, start, end in matches:
				string_id = self.__nlp.vocab.strings[match_id]  # Get string representation
				span = doc[start:end]  # The matched span
				self.__start = start # for further use in PI component
				text = self.__GetClearText(span.text)
				#
				docx = self.__nlp(text, disable=['parser','ner'])
				resultText = docx[0].lemma_ if len(docx) == 1 else str(docx[0].lemma_) + " " + str(docx[1].lemma_)
				concepts.append([string_id, resultText]) # [key, value]
			
			if len(concepts) > 1:
				concepts = self.__RidOfExcessData(concepts)

			for word in concepts:
				word[1] = word[1].replace(" ","_") # i.e. parking space become parking_space (it's for overpass)
			
			return concepts if len(concepts) > 0 else None
		except Exception as e:
			print("#Error. Something wrong inside of CI.Identify()")
			print(e)
			return None
	
	def __RidOfExcessData(self, concepts):
		# define variables
		text = self.__GetClearText(self.__sentence)
		tmp = ""
		# preprocess text
		for token in self.__nlp(text,disable=['parser','ner']):
			tmp += token.lemma_ + " "
		text = tmp
		#

		concept_list = concepts
		new_concept_list = []
		kol = 0
		# sort
		concept_list.sort(key=lambda x:len(x[1]), reverse=True)
		# get concepts
		for item in concept_list:
			# get first concept
			if kol == 0:
				if item[1] in text: 
					new_concept_list.append(item)
					kol = 1
					text = text.replace(item[1],"",1)
					continue
			# get second concept
			if kol == 1:
				if item[1] in text:
					new_concept_list.append(item)
					kol = 2
					text = text.replace(item[1],"",1)
					break
		return new_concept_list

	def __GetClearText(self, arg_text):
		translator = str.maketrans(string.punctuation, ' '*len(string.punctuation))
		text = arg_text.lower().translate(translator)
		text = text.replace("  ", " ") if "  " in text else text
		text = ' '.join(text.split())
		return text