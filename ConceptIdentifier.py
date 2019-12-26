import spacy
from numpy import genfromtxt
import numpy as np

class ConceptIdentifier:

	def __init__(self, text):
		#private variables
		self.__sentence = text
		self.__tourism = genfromtxt('features/tourism.csv', delimiter=';', dtype=None, encoding='utf-8')	
		self.__amenity = genfromtxt('features/amenity.csv', delimiter=';', dtype=None, encoding='utf-8')	
		self.__concept = list() # main class variable, that could contain tuple
		self.Identify()

	def GetConcept(self):
		return self.__concept

	def Identify(self):
		nlp = spacy.load("en_core_web_sm")
		docx = nlp(self.__sentence) 
		instClass = None
		instValue = None
		instInfo = None

		for chunk in docx.noun_chunks:
			#1 Check chunks
			chunkText = chunk.text
			print("chunk"+chunkText)
			instClass, instValue, instInfo = self.__NumpyData(chunkText)
			#2 Check rootText
			if instClass == None and instValue == None and instInfo == None:
				rootText = chunk.root.text
				print("rootText"+rootText)
				instClass, instValue, instInfo = self.__NumpyData(rootText)
			#3 Check lemma
			if instClass == None and instValue == None and instInfo == None:
				lemma = chunk.lemma_
				print("lemma"+lemma)
				instClass, instValue, instInfo = self.__NumpyData(lemma)
			#
			if instClass != None and instValue != None and instInfo != None:
				self.__concept.append((instClass,instValue,instInfo))
		if len(self.__concept) == 0:
			self.__concept.append((instClass,instValue,instInfo))



	def __NumpyData(self,word):
		instClass = None
		instValue = None
		instInfo = None	
		#
		npMask = np.where( (self.__tourism[:,2] == word) )
		result = self.__tourism[npMask, :]
		if (len(result[0]) != 0):
			if word == result[0].item(2):
				instClass = "tourism"
				instValue = result[0].item(0)
				instInfo = result[0].item(1)
				return (instClass,instValue,instInfo)
		#
		npMask = np.where( (self.__amenity[:,2] == word) )
		secondResult = self.__amenity[npMask, :]
		if (len(secondResult[0]) != 0):
			if word == secondResult[0].item(2):
				instClass = "amenity"
				instValue = secondResult[0].item(0)
				instInfo = secondResult[0].item(1)
				return (instClass,instValue,instInfo)
		#
		return (instClass,instValue,instInfo)