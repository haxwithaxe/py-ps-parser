#!/usr/bin/python

OOPS = ('/','[','{','(','<')

OPLABEL = 'operator'

class node:

	def __init__(self,token):

		self.children = []

		self.token = token	

def find_nodes(pos,items,tree):

	if items[pos].name in OOPS and items[pos].data_type == OPLABEL:

		while not items[pos].data_type == OPLABEL:

			pos += 1

			curr_node.children.append([items[pos]])

		if items[pos].name in OOPS:

			

			

	return pos, tree

def outputps(input):

	i = 0

	while i < len(input):

		find_nodes(i,input)
			

		else:

			curr_node.children.append([input[i]])

		i += 1

