class PatternIdentifier:

	def __init__(self, text):
		self.__text = text.lower()

	def GetPattern(self):
		if self.__text.startswith("show me"):
			return 1
		if (self.__text.startswith("what is address of")):
			return 2
		if self.__text.startswith("i would like to") and self.__text.endswith("somewhere"): # dont try it
			return 3
		if self.__text.startswith("where is"):
			return 4
		if self.__text.startswith("how many"):
			return 5

		return 0 # error