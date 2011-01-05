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

class Tokenizer:
	def __init__(self, instream):
		self.instream = instream
		self.mode = "name"
		self.last_char = ""
		self.last_token = None
		self.depth = 0

	def __iter__(self):
		return self

	def nextChar(self):
		self.last_char = self.instream.read(1)
		return self.last_char

	def next(self):
		if (self.mode == "EOF"):
			raise StopIteration
		if ((self.last_token != None)
				and (self.last_token.data_type == "operator")
				and (self.mode != "operator")):
			if (self.last_token.name == "("):
				self.mode = "string"
			elif (self.last_token.name == "<"):
				self.mode = "hex"
			elif (self.last_token.name == "<~"):
				self.mode = "base85"
			else:
				self.mode = "name"
		current_token = Token(data_type=self.mode)
		if (self.mode == "operator"):
			current_token.append(self.last_char)
			character = self.nextChar()
		if (self.last_char == ""):
			character = self.nextChar()
		else:
			character = self.last_char
		self.mode = "name"
		while (character != ""):
			if (not current_token.isValid(character)):
				if (current_token.data_type == "base85"):
					self.mode = "operator"
				if ((len(current_token.name) > 0)
						or ((current_token.data_type == "string")
							or (current_token.data_type == "hex")
							or (current_token.data_type == "base85"))
						or ((self.last_token != None)
							and (self.last_token.data_type == "operator")
							and ((self.last_token.name == "/")
								or (self.last_token.name == "//")))):
					self.last_token = current_token
					return current_token
				if character == "%":
					current_token.data_type = "comment"
					while ((character != "") and not (character in NEWLINE)):
						current_token.append(character)
						character = self.nextChar()
					return current_token
				if (character in SPECIAL_CHARACTERS):
					self.mode = "operator"
					break
				character = self.nextChar()
				break
			else:
				current_token.append(character)
			character = self.nextChar()
		if (character == ""):
			self.mode = "EOF"
		if (len(current_token.name) > 0):
			self.last_token = current_token
			return current_token
		return self.next()

