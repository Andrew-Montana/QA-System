import nltk
from nltk.corpus import treebank
from nltk.stem import WordNetLemmatizer

class NltkModule:

	def __init__(self, text):
		#private variables
		self.__sentence = text
		self.__tokens = nltk.word_tokenize(self.__sentence)
		self.__tags = nltk.pos_tag(self.__tokens)
		self.__ent = nltk.chunk.ne_chunk(self.__tags)

	def GetResponse(self, index):
		nltkList = self.__GetNltkList()
		if len(nltkList) == 0:
			return "error"
		switch = {1:self.__nltk_showme(nltkList),
		 2:self.__nltk_whatIsAddress(nltkList),
		  3:self.__actionSomewhere(),
		   4:self.__nltk_whereiscity(nltkList),
		    5:self.__nltk_howmanyams(nltkList)}
		return switch.get(index, 'error')

	# 1
	def __nltk_showme(self, dataList):
		# show me <location> in <city>
		name = (dataList[0])["NNP"]
		amenity = (dataList[0])["NN"]
		query = f"""[out:json];area[name = "{name}"]; node(area)[amenity={amenity}]; out;"""
		return query

	# 2
	def __nltk_whatIsAddress(self, dataList):
		# (What is address(NN) of <cafe name/restaurant name etc>?) // extend later with nnps and nns. Could be multiple NNPs because of its one name
		# Caffe Bene, Bobamosa, Bouchon Backery,
		nnpList = list()
		for item in dataList:
			nnpList.append(item["NNP"])
		name = " ".join(nnpList)
		query = f"""[out:json];area[name = "New York"]; node(area)[name="{name}"]; out;"""
		return query

	# 3 !
	def __actionSomewhere(self):
		#I would like to <action>(check from amenity/tourism...). Extend later, maybe user wants to eat and sleep somewhere simultaneously.
		#actionList = list(["eat","watch","dance","sleep","drink","relax"])

		# Make better later, like loop available actions and retrieve amenities from somekinda list array database etc
		#for item in actionList:
		#	if item in text:
		amenity = dict()
		if "eat" in self.__sentence:
			amenity["NN"] = "restaurant"
		if "watch" in self.__sentence:
			amenity["NN"] = "cinema"
		if "dance" in self.__sentence:
			amenity["NN"] = "nightclub"
		if "drink" in self.__sentence:
			amenity["NN"] = "drinking_water"
		if "relax" in self.__sentence:
			amenity["NN"] = "cinema"
		
		if len(amenity) == 0:
			return "error"
		query = f"""[out:json];area[name = "New York"]; node(area)[amenity="{amenity["NN"]}"]; out;"""
		return query

	# 4
	def __nltk_whereiscity(self, dataList):
		# where is <city>
		name = (dataList[0])["NNP"]
		query = f"""[out:json];(node["place"="city"]["name"="{name}"];);out body;>;out skel qt;"""
		return query

	# 5
	def __nltk_howmanyams(self, dataList):
		# how many <amenity> in <city>
		name = (dataList[0])["NNP"]
		amenity = (dataList[0])["NNS"]
		lemmatizer = WordNetLemmatizer()
		query = f"""[out:json];area[name = "{name}"]; node(area)[amenity={lemmatizer.lemmatize(amenity)}]; out;"""
		return query

	####
	def __GetNltkList(self):
		nltkList, nnpList, nnList, nnsList = list(), list(), list(), list()
		for i,j in self.__tags:
			if j == "NNP":
				nnpList.append(i)
			if j == "NN":
				nnList.append(i)
			if j == "NNS":
				nnsList.append(i)
		#
		max = len(nnpList) if len(nnpList) >= len(nnList) else len(nnList)
		max = max if max >= len(nnsList) else len(nnsList)

		for i in range(0,max):
			tmpDict = dict()
			if len(nnpList) > i:
				tmpDict["NNP"] = nnpList[i]
			else:
				tmpDict["NNP"] = ""

			if len(nnList) > i:
				tmpDict["NN"] = nnList[i]
			else:
				tmpDict["NN"] = ""

			if len(nnsList) > i:
				tmpDict["NNS"] = nnsList[i]
			else:
				tmpDict["NNS"] = ""

			if len(tmpDict) != 0:
				nltkList.append(tmpDict)
		return nltkList
