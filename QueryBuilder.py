class QueryBuilder:

	def __init__(self, questionIndex, concepts, entities):
		self.__questionIndex = questionIndex
		self.__entities = entities
		self.__concepts = concepts

		self.__conceptClass = (self.__concepts[0])[0] if self.__concepts != None else None
		self.__conceptValue = (self.__concepts[0])[1] if self.__concepts != None else None
		self.__entityText = (self.__entities[0])[0] if self.__entities != None else None

	def GetQuery(self):
		index = self.__questionIndex
		if(index == 0):
			return None
		elif(index == 1):
			return self.__showme()
		elif(index == 2):
			return self.__whatIsAddress()
		elif(index == 3):
			return self.__actionSomewhere()
		elif(index == 4):
			return self.__whereiscity()
		elif(index == 5):
			return self.__howmanyams()

		return None

	# 1
	def __showme(self):
		# show me <location> in <city>
		query = f"""[out:json];area[name = "{self.__entityText}"]; node(area)[{self.__conceptClass}={self.__conceptValue}]; out;"""
		print(query)
		return query

	# 2
	def __whatIsAddress(self):
		# (What is address(NN) of <cafe name/restaurant name etc>?) // extend later with nnps and nns. Could be multiple NNPs because of its one name
		# Caffe Bene, Bobamosa, Bouchon Backery,
		query = f"""[out:json];area[name = "New York"]; node(area)[name="{self.__entityText}"]; out;"""
		return query

	# 3 !
	def __actionSomewhere(self):
		pass

	# 4
	def __whereiscity(self):
		# where is <city>
		query = f"""[out:json];(node["place"="city"]["name"="{self.__entityText}"];);out body;>;out skel qt;"""
		return query

	# 5
	def __howmanyams(self):
		# how many <amenity/tourism> in <city>
		query = f"""[out:json];area[name = "{self.__entityText}"]; node(area)[{self.__conceptClass}={self.__conceptValue}]; out;"""
		return query
