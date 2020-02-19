class QueryBuilder:

	def __init__(self, patternID, concepts, entities):
		self.__patternID = patternID
		self.__entities = entities
		self.__concepts = concepts

		#self.__conceptClass = (self.__concepts[0])[0] if self.__concepts != None else None
		#self.__conceptValue = (self.__concepts[0])[1] if self.__concepts != None else None
		#self.__entityText = (self.__entities[0])[0] if self.__entities != None else None

	def GetQuery(self):
		pattern = self.__patternID
		if(pattern == "PS1"):
			return self.__PS1()
		elif(pattern == "PS1_2"):
			return self.__PS1_2()
		elif(pattern == "PS2_2"):
			return self.__PS2_2()
		#elif(pattern == "PA_1"):
			#return self.__actionSomewhere()
		elif(pattern == "PA_2"):
			return self.__PA_2()
		#elif(pattern == "POH_1"):
			#return self.__howmanyams()
		elif(pattern == "POH_2"):
			return self.__POH_2()
		elif(pattern == "PC"):
			return self.__PC()
		elif(pattern == "PCE"):
			return self.__PCE()

		return None


	def __PS1(self):
		cityByDefault = "Berlin"
		concept_key = self.__concepts[0][0]
		concept_value = self.__concepts[0][1]
		query = f"""[out:json];area[name = "{cityByDefault}"]; node(area)[{concept_key}="{concept_value}"]; out;""" 
		return query

	def __PS1_2(self):
		#city = self.__entities[0][1].title() if self.__entities[0][0] == "GPE" else None
		city = self.__entities[0][1].title()
		query = f"""[out:json];
(
 node["place"="city"]["name"="{city}"];
 node["place"="city"]["name:ca"="{city}"];
 node["place"="city"]["name:af"="{city}"];
 node["place"="city"]["name:ab"="{city}"];
 node["place"="city"]["alt_name:an"="{city}"];
 node["place"="city"]["name:cs"="{city}"];
 node["place"="city"]["name:hr"="{city}"];
);

out body;>;out skel qt;"""
		return query

	def __PS2_2(self):
		#city = self.__entities[0][1].title() if self.__entities[0][0] == "GPE" else None # title makes first letter of each word capital. GPE - cities countries states label
		city = self.__entities[0][1].title()
		concept_key = self.__concepts[0][0]
		concept_value = self.__concepts[0][1]
		query = f"""[out:json];area[name = "{city}"]; node(area)[{concept_key}="{concept_value}"]; out;""" 
		return query

	# after required to get particular properties from node
	def __PA_2(self):
		entityName = self.__entities[0][1]
		#query = f"""[out:json];area[name = "{cityByDefault}"]; node(area)[name="{entityName}"]; out;"""
		query = f"""[out:json];node["{entityName}"]; out;"""
		return query

	# after required to get particular properties from node
	def __POH_2(self):
		entityName = self.__entities[0][1]
		query = f"""[out:json];node["{entityName}"]; out;"""
		return query

	# Pattern Concept: <concepts> restaurants
	def __PC(self):
		cityByDefault = "Berlin"
		concept_key = self.__concepts[0][0]
		concept_value = self.__concepts[0][1]
		query = f"""[out:json];area[name = "{cityByDefault}"]; node(area)[{concept_key}="{concept_value}"]; out;""" 
		return query

	# Pattern Concept Entity: <concepts> <entity> i.e. cafe in Berlin
	def __PCE(self):
		#city = self.__entities[0][1].title() if self.__entities[0][0] == "GPE" else None
		city = self.__entities[0][1].title()
		concept_key = self.__concepts[0][0]
		concept_value = self.__concepts[0][1]
		query = f"""[out:json];area[name = "{city}"]; node(area)[{concept_key}="{concept_value}"]; out;""" 
		return query










	# # 1
	# def __showme(self):
	# 	# show me <location> in <city>
	# 	query = f"""[out:json];area[name = "{self.__entityText}"]; node(area)[{self.__conceptClass}={self.__conceptValue}]; out;"""
	# 	print(query)
	# 	return query

	# # 2
	# def __whatIsAddress(self):
	# 	# (What is address(NN) of <cafe name/restaurant name etc>?) // extend later with nnps and nns. Could be multiple NNPs because of its one name
	# 	# Caffe Bene, Bobamosa, Bouchon Backery,
	# 	query = f"""[out:json];area[name = "New York"]; node(area)[name="{self.__entityText}"]; out;"""
	# 	return query

	# # 3 !
	# def __actionSomewhere(self):
	# 	pass

	# # 4
	# def __whereiscity(self):
	# 	# where is <city>
	# 	query = f"""[out:json];(node["place"="city"]["name"="{self.__entityText}"];);out body;>;out skel qt;"""
	# 	return query

	# # 5
	# def __howmanyams(self):
	# 	# how many <amenity/tourism> in <city>
	# 	query = f"""[out:json];area[name = "{self.__entityText}"]; node(area)[{self.__conceptClass}={self.__conceptValue}]; out;"""
	# 	return query
