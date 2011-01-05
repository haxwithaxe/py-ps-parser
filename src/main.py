#!/usr/bin/python

# main.py - Entry point for testing the library.

import sys
import tokenizer, outputps

def main():
	tokens = tokenizer.Tokenizer(sys.stdin)
	t = outputps.pstree(tokens)

	print t.ps_to_tree()

if __name__=="__main__":
	main()

