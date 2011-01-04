#!/usr/bin/python

# main.py - Entry point for testing the library.

import sys
import tokenizer, outputps

def main():
	tokens = tokenizer.tokenize(sys.stdin)
	outputps.outputps(tokens)

if __name__=="__main__":
	main()

