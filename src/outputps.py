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

		output = []

		checknext = False

		drop = False

		font_rename_type = re.compile("Type[0-9]_AH[0-9]{4}")

		font_rename_fu = re.compile("CMap_AH[0-9]{4}-[\S]")

		for tok in self.tokens:

			trash = None

			if checknext and ( font_rename_fu.match(tok.name) or tok.name == '/' ):

				if tok.name != '/':

					output.pop(-1)

					output.pop(-1)

					drop = True

			if tok.name.startswith('%!PS-AdobeFont-1.0'):

				drop = True

			if tok.name == 'eexec':

				trash = self.tokens.mode = "type1"

			if tok.name == 'cleartomark':

				drop = False

			if font_rename_type.match(tok.name):

				checknext = True

			if not drop:

				output.append(tok.name)

		soutput = ''
	
		for x in output:

			if str(x) == '/':

				soutput += str(x)

			else:

				soutput += str(x)+'\n'

		return soutput

	def ps_to_tree(self):

		self._find_nodes()

		while self.curr_node.parent: # get to the top of the tree

			self.curr_node = self.curr_node.parent

		return self.curr_node
