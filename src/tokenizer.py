#!/usr/bin/python

# tokenizer.py - Functions for tokenizing the input stream.

import string, sys
import token

sys.setrecursionlimit(200000)
SPECIAL_CHARACTERS = "()<>[]{}/%"
BLOCK_START = "(<[{"
WHITE_SPACE = "\x00\t\x0a\x0c\x0d "
NEWLINE = "\x0a\x0c\x0d"
HEX = "0123456789abcdefABCDEF"
ZERO_PAD = "0000000000000000000000000000000000000000000000000000000000000000"
SHORT_ZERO_PAD = "00000000000000000000000000000000"

class Tokenizer:
	def __init__(self, instream):
		self.instream = instream
		self.mode = "name"
		self.last_char = ""
		self.last_token = None
		self.depth = 0

	def __iter__(self):
		return self

	def _nextChar(self):
		self.last_char = self.instream.read(1)
		return self.last_char

	def _nextLine(self):
		line = self._nextChar()
		while (not (self.last_char in NEWLINE)):
			line += self._nextChar()
		return line

	def nextType1(self):
		self.mode = "name"
		current_token = token.Token(data_type="type1")
		count = 0
		short_count = 0
		while ((count < 8) and (short_count < 16)):
			line = self._nextLine()
			if (line == ""):
				raise StopIteration
			current_token.append(line)
			if (ZERO_PAD in line):
				count += 1
			elif (SHORT_ZERO_PAD in line):
				short_count += 1
			elif (count):
				count = 0
				short_count = 0
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
		current_token = token.Token(data_type=self.mode)
		if (self.mode == "operator"):
			current_token.append(self.last_char)
			character = self._nextChar()
		if (self.last_char == ""):
			character = self._nextChar()
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
					while (character != ""): # and not (character in NEWLINE)):
						current_token.append(character)
						if character in NEWLINE:
							return current_token
						character = self._nextChar()
					return current_token
				if (character in SPECIAL_CHARACTERS):
					self.mode = "operator"
					break
				character = self._nextChar()
				break
			else:
				current_token.append(character)
			character = self._nextChar()
		if (character == ""):
			self.mode = "EOF"
		if (len(current_token.name) > 0):
			self.last_token = current_token
			return current_token
		return self.next()

	def __next__(self):
		return self.next()

