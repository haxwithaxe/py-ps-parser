#!/usr/bin/python

# main.py - Entry point for testing the library.

import sys, pprint
import tokenizer, outputps

def print_pstree(treeobj):

	for i in treeobj.children:

		print(i.token.name)
		print_pstree(i)

def main():
	tokens = tokenizer.Tokenizer(sys.stdin)
	t = outputps.pstree(tokens)

	psobj = t.ps_to_tree()

	print_pstree(psobj)

if __name__=="__main__":
	main()

