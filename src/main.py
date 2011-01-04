#!/usr/bin/python

# main.py - Entry point for testing the library.

import sys
import tokenizer

def main():
	tokens = tokenizer.tokenize(sys.stdin)
	print tokens
	print ""
	print "Number of tokens:", len(tokens)

if __name__=="__main__":
	main()

