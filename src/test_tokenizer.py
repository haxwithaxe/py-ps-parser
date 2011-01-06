#!/usr/bin/python

# main.py - Entry point for testing the library.

import sys
import tokenizer

def main():
	tokens = tokenizer.Tokenizer(sys.stdin)

	for token in tokens:
		if (token.data_type != "type1"):
			print(token.data_type + ":\t" + token.name)
		else:
			print("type1 binary omitted")
		if (token.name == "eexec"):
			tokens.mode = "type1"

if __name__=="__main__":
	main()

