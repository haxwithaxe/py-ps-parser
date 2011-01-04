#!/usr/bin/python

# main.py - Entry point for testing the library.

import sys
import tokenizer, ouptputPS

def main():
	tokens = tokenizer.tokenize(sys.stdin)
	outputPS(tokens)

if __name__=="__main__":
	main()

