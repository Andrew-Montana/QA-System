import spacy
from spacy.matcher import Matcher

class PatternIdentifier:

	def __init__(self, text, numEnts, numConcepts):
		self.__nlp = spacy.load("en_core_web_sm", disable=['parser','ner'])
		self.__text = text.lower()
		self.__matcher = Matcher(self.__nlp.vocab)
		self.__LoadMatcherPatterns()
		
		self.__ents = numEnts
		self.__concepts = numConcepts

	def GetPattern(self):
		doc = self.__nlp(self.__text)
		matches = self.__matcher(doc)
		pattern_ids = list()
		
		for match_id, start, end in matches:
			string_id = self.__nlp.vocab.strings[match_id]
			if string_id not in pattern_ids:
				pattern_ids.append(string_id)
		
		#print(pattern_ids)
		# Define which pattern
		result = None
		
		for pattern in pattern_ids:
			if pattern == "PS1":
				if self.__ents == 0 and self.__concepts == 1:
					result = "PS1"
			elif pattern == "PS2" and result == None:
				if self.__ents == 0 and self.__concepts == 2:
					result = "PS2_1"
				elif self.__ents == 1 and self.__concepts == 1:
					result = "PS2_2"
			elif pattern == "PA" and result == None:
				if self.__ents == 0 and self.__concepts == 1:
					result = "PA_1"
				elif self.__ents == 1 and self.__concepts == 0:
					result = "PA_2"
			elif pattern == "POH" and result == None:
				if self.__ents == 0 and self.__concepts == 1:
					result = "POH_1"
				elif self.__ents == 1 and self.__concepts == 0:
					result = "POH_2"
		return result
	
	def __LoadMatcherPatterns(self):
		patterns_PS1 = [
		[{'LOWER': 'show'},{'LOWER': 'me'},{'IS_ASCII': True, 'OP': '+'}],[{'LOWER': 'show'},{'IS_ASCII': True, 'OP': '+'}],
		[{'LOWER': 'where'},{'LOWER': 'is'},{'IS_ASCII': True, 'OP': '+'}], [{'LOWER': 'where'},{'LOWER': 'are'},{'IS_ASCII': True, 'OP': '+'}],[{'LOWER': 'location'},{'LOWER': 'of'},{'IS_ASCII': True, 'OP': '+'}],
		[{'LOWER': 'what'},{'LOWER': 'is'},{'LOWER': 'location'},{'LOWER': 'of'},{'IS_ASCII': True, 'OP': '+'}]]

		patterns_PS2 = [
		[{'LOWER': 'show'},{'LOWER': 'me'},{'IS_STOP' : True, 'OP' : '?'},{'IS_ASCII': True},{'IS_ASCII': True, 'OP': '?'},{'LOWER': 'close'},{'IS_STOP': True, 'OP': '?'},{'IS_ASCII': True}],
		[{'LOWER': 'show'},{'LOWER': 'me'},{'IS_STOP' : True, 'OP' : '?'},{'IS_ASCII': True},{'IS_ASCII': True, 'OP': '?'},{'LOWER': {'IN' : ['near','nearby','around','in']}},{'IS_ASCII': True}]	,
		[{'LOWER': 'show'},{'IS_STOP' : True, 'OP' : '?'},{'IS_ASCII': True},{'IS_ASCII': True, 'OP': '?'},{'LOWER': {'IN' : ['near','nearby','around','in']}},{'IS_ASCII': True}],
		[{'LOWER': 'show'},{'IS_STOP' : True, 'OP' : '?'},{'IS_ASCII': True},{'IS_ASCII': True, 'OP': '?'},{'LOWER': 'close'},{'IS_STOP': True, 'OP': '?'},{'IS_ASCII': True}],]

		patterns_PA = [
		[{'LOWER': 'what'},{'IS_STOP': True, 'OP': '+'},{'LOWER': 'address'},{'IS_STOP': True, 'OP': '+'},{'IS_ASCII': True}],
		[{'LOWER': 'address'},{'IS_STOP': True, 'OP': '+'},{'IS_ASCII': True}],
		[{'LOWER': 'tell'},{'LOWER': 'me'},{'IS_STOP': True, 'OP': '?'},{'IS_ASCII': True},{'IS_ASCII': True, 'OP': '?'},{'LOWER' : 'address'}]]

		patterns_POH = [
		[{'LOWER': 'what'},{'IS_STOP': True, 'OP': '*'},{'LOWER': 'opening'},{'LOWER': 'hours'},{'IS_STOP': True, 'OP': '*'},{'IS_ASCII' : True}],
		[{'LOWER': 'when'},{'IS_STOP': True, 'OP': '?'},{'IS_ASCII': True},{'IS_ASCII': True, 'OP': '?'},{'IS_STOP': True },{'LEMMA': 'close'}],
		[{'LOWER': 'when'},{'IS_STOP': True, 'OP': '?'},{'IS_ASCII': True},{'IS_ASCII': True, 'OP': '?'},{'IS_STOP': True },{'LEMMA': 'open'}]]

		self.__matcher.add("PS1", None, *patterns_PS1)
		self.__matcher.add("PS2", None, *patterns_PS2)
		self.__matcher.add("PA", None, *patterns_PA)
		self.__matcher.add("POH", None, *patterns_POH)