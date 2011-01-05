#!/usr/bin/python

import re

OOPS = ('[','{','(','<')

EOPS = {'[':']','{':'}','(':')','<':'>'}

EXTOPS = ('pdfmark')

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

		match_name = None

		child_of_last_node = False

		for tok in self.tokens:

			#print(tok.name)

			if child_of_last_node or match_name:

				self.curr_node.children[-1].children.append(psnode(tok,self.curr_node.children[-1]))

				child_of_last_node = False

				if tok.name in EXTOPS:

					print(tok.name,'matched EXTOPS')

					match_name = tok.name

				if match_name == tok.name:

					match_name == None

			elif tok.name in OOPS:

				self.curr_node.children.append(psnode(tok,self.curr_node))

				self.curr_node = self.curr_node.children[-1]

				self._find_nodes()

			elif self.curr_node.token and tok.name == EOPS[self.curr_node.token.name]:

				self.curr_node.children.append(psnode(tok,self.curr_node))

				self.curr_node = self.curr_node.parent

			elif tok.name == '/':

				self.curr_node.children.append(psnode(tok,self.curr_node))

				child_of_last_node = True

			else:

				self.curr_node.children.append(psnode(tok,self.curr_node))


	def ps_to_tree(self):

		self._find_nodes()

		while self.curr_node.parent: # get to the top of the tree

			self.curr_node = self.curr_node.parent

		return self.curr_node
