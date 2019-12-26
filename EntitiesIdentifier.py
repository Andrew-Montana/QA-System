import spacy

class EntitiesIdentifier:

	def __init__(self, text):
		self.__sentense = text
		self.__nlp = spacy.load("en_core_web_sm")
		self.__entity = list() # main class variable, that could contain tuple
		self.Identify()

	def GetEntity(self):
		return self.__entity

	def Identify(self):
		doc = self.__nlp(self.__sentense)
		entText = None
		entLabel = None
		for ent in doc.ents:
			self.__entity.append((ent.text,ent.label_))
