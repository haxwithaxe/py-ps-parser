#!/usr/bin/python

import re

OOPS = ('[','{','(','<')

EOPS = {'[':']','{':'}','(':')','<':'>'}

OPLABEL = 'operator'

white_space = re.compile('\s')

class psnode:

	def __init__(self,token,parent = None):

		self.children = []

		self.token = token # the token associated with this PS node

		self.parent = parent # pointer to the parent node


class pstree:

	def __init__(self, tokens):

		self.curr_node = psnode(None)

		self.tokens = tokens

	def _find_nodes(self):

		tok = self.tokens.next()

		for tok in self.tokens:

			print(tok.name)		

			if tok.name in OOPS:

				self.curr_node.children.append(psnode(tok,self.curr_node))

				self.curr_node = self.curr_node.children[-1]

				self._find_nodes()

			elif self.curr_node.token and tok.name == EOPS[self.curr_node.token.name]:

				self.curr_node.children.append(psnode(tok,self.curr_node))

				self.curr_node = self.curr_node.parent

				self._find_nodes()

			elif tok.name == '/':

				self.curr_node.children.append(psnode(tok,self.curr_node))

				tok = self.tokens.next()

				self.curr_node.children[-1].children.append(psnode(tok,self.curr_node))

				self._find_nodes()

			else:

				self.curr_node.children.append(psnode(tok,self.curr_node))


	def ps_to_tree(self):

		run = True

		while run:

			try:

				self._find_nodes()

			except StopIteration:

				run = False

		while self.curr_node.parent: # get to the top of the tree

			self.curr_node = self.curr_node.parent

		return self.curr_node
