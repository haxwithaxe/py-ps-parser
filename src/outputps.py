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

			print(tok.name)

			if match_name == tok.name:

				print(tok.name, 'matched previous operator')

				match_name == None

				self.curr_node.children.append(psnode(tok,self.curr_node))

				print('one up')

				self.curr_node = self.curr_node.parent

			elif tok.name in EXTOPS:

				print(tok.name,'matched EXTOPS')

				match_name = tok.name

				self.curr_node.children.append(psnode(tok,self.curr_node))

				print('one down')

				self.curr_node = self.curr_node.children[-1]

			elif child_of_last_node:

				try:

					self.curr_node.children[-1].children.append(psnode(tok,self.curr_node.children[-1]))

				except IndexError:

					self.curr_node.children.append(psnode(tok,self.curr_node))

				child_of_last_node = False

			elif tok.name in OOPS:

				match = True

				if tok.name == '[':

					tmp = self.curr_node

					while tmp:

						tmp = tmp.parent

						if tmp == None:

							break

						elif tmp.token == None:

							break

						elif tmp.token.name in EXTOPS:

							print('stay here')

							match = False

							break

				self.curr_node.children.append(psnode(tok,self.curr_node))

				if match:

					print('one down')

					self.curr_node = self.curr_node.children[-1]

			elif self.curr_node.token and self.curr_node.token.name in OOPS and tok.name == EOPS[self.curr_node.token.name]:

				self.curr_node.children.append(psnode(tok,self.curr_node))

				print('one up')

				self.curr_node = self.curr_node.parent


			elif tok.name == '/':

				self.curr_node.children.append(psnode(tok,self.curr_node))

				child_of_last_node = True

			else:

				self.curr_node.children.append(psnode(tok,self.curr_node))

	def strip_font_data(self):

		drop = False

		for tok in self.tokens:

			if tok.name == 'eexec':

				self.tokens.binary = True

			elif tok.name == 'cleartomark'

				self.tokens.binary = False

				drop = False

			elif tok.name == '%!PS-AdobeFont-1.0':

				drop = True

			if not drop:

				output.append(tok.name)

				

		output = ''.join(for x in output)

		return output

	def ps_to_tree(self):

		self._find_nodes()

		while self.curr_node.parent: # get to the top of the tree

			self.curr_node = self.curr_node.parent

		return self.curr_node
