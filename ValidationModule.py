class ValidationModule:

	# later:
	# use regex
	# change method logic (improve)
	def check_valid(self, text):
		text = text.lower()

		if text.startswith("show me"):
			return 1
		if (text.startswith("what is address of")):
			return 2
		if text.startswith("i would like to") and text.endswith("somewhere"):
			return 3
		if text.startswith("where is"):
			return 4
		if text.startswith("how many"):
			return 5

		return 0 # error