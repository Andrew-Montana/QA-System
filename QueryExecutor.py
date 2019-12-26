import overpy

class QueryExecutor:

	def __init__(self, query):
		self.__api = overpy.Overpass()
		self.__query = query

	def ExecuteQuery(self):
		return self.__api.query(self.__query)

