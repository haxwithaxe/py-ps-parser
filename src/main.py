#!/usr/bin/python

# main.py - Entry point for testing the library.

import sys
import tokenizer, outputps

def print_pstree(treeobj,c = None):

	dots = ''

	if c == None:
		c = 0

	else:
		c += 1
	
	#print('//'+str(c)+'//')

	a = 0

	while a < c:

		dots += ' .'	

		a += 1

	for i in treeobj.children:

		print(dots+i.token.name)

		print_pstree(i,c)

def main():
	tokens = tokenizer.Tokenizer(sys.stdin)

	t = outputps.pstree(tokens)

	psobj = t.strip_font_data()

	print(psobj)

if __name__=="__main__":
	main()

