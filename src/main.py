#!/usr/bin/python

# main.py - Entry point for testing the library.

import sys
import tokenizer

def main():
	tokens = []
	for token in tokenizer.Tokenizer(sys.stdin):
		tokens.append(token)
		print "Token:" + token.data_type + ": >" + token.name + "<"
	print ""
	print "Number of tokens:", len(tokens)

if __name__=="__main__":
	main()

