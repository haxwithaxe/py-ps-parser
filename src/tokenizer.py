#!/usr/bin/python

# tokenizer.py - Functions for tokenizing the input stream.

import string
import token

SPECIAL_CHARACTERS = "()<>[]{}/%"
BLOCK_START = "(<[{"
WHITE_SPACE = "\x00\t\x0a\x0c\x0d "
NEWLINE = "\x0a\x0c\x0d"
HEX = "0123456789abcdefABCDEF"
ZERO_PAD = "0000000000000000000000000000000000000000000000000000000000000000"

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

	def nextType1(self):
		self.mode = "name"
		current_token = Token(data_type="type1")
		count = 0
		while (count < 8):
			line = self.instream.readline()
			if (line == ""):
				raise StopIteration
			current_token.append(line)
			if (ZERO_PAD in line):
				count += 1
			elif (count):
				count = 0
		self.last_char = line[-1]
		return current_token

	def next(self):
		if (self.mode == "type1"):
			return self.nextType1()
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

