#!/usr/bin/python

# token.py - Token class. Represents an element of the tokenized PostScript stream.

class Token:
	def __init__(self, name = "", data_type = "name"):
		self.name = name
		self.data_type = data_type
		self.depth = 0

	def append(self, character):
		self.name += character

	def isValid(self, character):
		if (self.data_type == "string"):
			if (character == "("):
				if (self.name[-1:] == "\\"):
					return True
				else:
					self.depth += 1
					return True
			if (character == ")"):
				if (self.name[-1:] == "\\"):
					return True
				if self.depth:
					self.depth -= 1
					return True
				return False
			return True

		if (self.data_type == "hex"):
			if (character in (WHITE_SPACE + HEX)):
				return True
			if (character == ">"):
				return False
			raise Exception("Invalid character: " + character)

		if (self.data_type == "base85"):
			if (character == "~"):
				return False
			return True

		if (self.data_type == "operator"):
			if (len(self.name) == 1):
				if ((self.name == "<")
						and ((character == "<")
							or (character == "~"))):
					return True
				if ((self.name == ">")
						and (character == ">")):
					return True
				if ((self.name == "~")
						and (character == ">")):
					return True
				if ((self.name == "/")
						and (character == "/")):
					return True
			return False

		return not (character in (WHITE_SPACE + SPECIAL_CHARACTERS))

