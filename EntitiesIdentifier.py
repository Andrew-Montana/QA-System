import spacy
class EntitiesIdentifier:

	def __init__(self, text):
		self.__sentense = text
		self.__nlp = spacy.load("en_core_web_sm", disable=['tagger','parser'])
		self.__entity = list() # main class variable, that could contain tuple
		self.Identify()

	def GetEntity(self):
		return self.__entity

	def Identify(self):
		doc = self.__nlp(self.__sentense)
		for ent in doc.ents:
			if ent.text not in self.__GetExcessLabels():
				self.__entity.append((ent.text,ent.label_))
		if len(self.__entity) == 0:
			self.__entity = None

	def __GetExcessLabels(self):
		return ['magic carpet','zip line','bbq','grit bin','atm','bureau de change','social centre','kneipp water cure','hampshire gate','jersey barrier','kissing gate','motorcycle barrier','house','kiosk','mosque','hut','saddler','turner','lifeguard tower','lifeguard platform','tertiary','highwater mark','adult gaming centre','summer','beacon','bunker silo','groyne','kiln','hot spring','archipelago','mast','inline','trolleybus','kiosk','second','atv','scuba diving','9pin','10pin','american','australian','canadian','rugby league','rugby union','scuba diving','taekwondo','alpine hut','wilderness hut']
