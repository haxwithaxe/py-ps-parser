#!/usr/bin/python

# tokenizer.py - Functions for tokenizing the input stream.

import string

SPECIAL_CHARACTERS = "()<>[]{}/%"
BLOCK_START = "(<[{"
WHITE_SPACE = "\x00\t\x0a\x0c\x0d "
NEWLINE = "\x0a\x0c\x0d"
HEX = "0123456789abcdefABCDEF"

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

		return not (character in (WHITE_SPACE + SPECIAL_CHARACTERS))

def tokenize(input_file):
	token_list = []
	current_token = Token()
	character = input_file.read(1)
	while (character != ""):
		#if (isWhiteSpace(character) or isSpecialCharacter(character)):
		if (not current_token.isValid(character)):
			if ((len(current_token.name) > 0)
					or (current_token.data_type == "string")
					or ((len(token_list) > 0)
						and (token_list[-1].data_type == "operator")
						and (token_list[-1].name == "/"))):
				token_list.append(current_token)
				current_token = Token()
			if character == "%":
				while ((character != "") and not (character in NEWLINE)):
					character = input_file.read(1)
			else:
				if (character in SPECIAL_CHARACTERS):
					token_list.append(Token(name=character, data_type="operator"))
					if character in BLOCK_START:
						if character == "(":
							current_token = Token(data_type="string")
						elif character == "<":
							character = input_file.read(1)
							if (character == "<"):
								token_list = token_list[:-1]
								token_list.append(Token(name="<<", data_type="operator"))
								current_token = Token()
							else:
								current_token = Token(data_type="hex")
								continue
					if character == ">":
						character = input_file.read(1)
						if character == ">":
							token_list = token_list[:-1]
							token_list.append(Token(name=">>", data_type="operator"))
						else:
							continue
		else:
			current_token.append(character)
		character = input_file.read(1)
	if (len(current_token.name) > 0):
		token_list.append(current_token)
	return token_list
