#!/usr/bin/python

# tokenizer.py - Functions for tokenizing the input stream.

import string

SPECIAL_CHARACTERS = "()<>[]{}/%"
WHITE_SPACE = "\x00\t\x0a\x0c\x0d "

class Token:
	def __init__(self):
		self.name = ""
	def __init__(self, token_string):
		self.name = token_string
	def append(self, character):
		self.name += character

def isWhiteSpace(character):
	return character in WHITE_SPACE

def isSpecialCharacter(character):
	return character in SPECIAL_CHARACTERS

def tokenize(input_file):
	token_list = []

	if (type(input_file) != type(file)):
		raise TypeError("Argument is not a file.")

	inComment = False
	current_token = Token()
	while ((character = input_file.read(1)) != ''):
		if (isWhiteSpace(character) or isSpecialCharacter(character)):
			if (len(current_token.name) > 0):
				token_list.append(current_token)
				current_token = Token()
		else:
			if (not inComment):
				current_token.append(character)
	if (len(current_token.name) > 0):
		token_list.append(current_token)

	return token_list
