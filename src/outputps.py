#!/usr/bin/python

import re

OOPS = ('[','{','(','<')

EOPS = {'[':']','{':'}','(':')','<':'>'}

AOPS = ('/','[',']','{','}','(',')','<','>')

EXTOPS = ('pdfmark')

OPLABEL = 'operator'

white_space = re.compile('\s')

eps_begin = re.compile('%!PS-Adobe-[0-9]*.[0-9]* EPSF-[0-9]*.[0-9]*.*')

font_type1_begin = re.compile("%!PS-AdobeFont-[0-9]+.[0-9]+[^\n\r]*")

font_rename_alias = re.compile("Type[0-9]_AH[0-9]{4}")

font_rename_name = re.compile("AH[0-9]{4}-[\S]")

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

		soutput = ''

		t2fonts = {}

		drop = False

		dropuntil = None

		dropnext = False

		dropthis = False

		font = None

		checknextname = False

		for tok in self.tokens:

			# check to see if we're gonna be getting binary data and tell the tokenizer that it needs to be ready
			if tok.name == 'eexec':

				self.tokens.mode = 'type1'

			# predrop/append changes

			if checknextname and tok.data_type == 'name':


				if font_rename_name.match(tok.name):

					font = re.sub("AH[0-9]{4}-","",tok.name)

				if tok.name == 'if':

					dropthis = True					

				if checknextname <= 0:

					checknextname = False

				else:

					checknextname -= 1

			if tok.name == 'CIDFontName':

				checknextname = 1

			if font_rename_alias.match(tok.name) and font:

				t2fonts[tok.name] = font

				font = False

			if font_rename_alias.match(tok.name) and not font:

				tok.name = t2fonts[tok.name]

			if tok.name == 'CIDFontType':

				output.pop(-1)

				output.pop(-1)

				output.pop(-1)

				output.pop(-1)

				drop = True

				dropuntil = 'composefont'

			if font_type1_begin.match(tok.name):

				drop = True

				dropuntil = 'cleartomark'

			# drop and set/reset mode variables

			if not drop and not dropnext and not dropthis:

				output.append(tok.name)

			if dropnext:

				dropnext = False

			if dropthis:

				dropthis = False

			if tok.name == dropuntil:

				drop = False

				dropuntil = None

				if tok.name == 'cleartomark':

					checknextname = 2


			# post drop/apend changes

		
			if tok.name == 'composefont':

				dropnext = True

		nonewlines = 0

		for x in output:

			if str(x) in ('/'):

				soutput += str(x)

			elif str(x) == '(':

				soutput += str(x)

				nonewlines += 1

			elif nonewlines > 0 and str(x) != ')':

				soutput += str(x)+' '

			elif str(x) == ')':

				if soutput[-1] == ' ':

					soutput = soutput[:-1]+str(x)+' '
				else:

					soutput += str(x)+' '

				nonewlines -= 1

			else:

				soutput += str(x)+'\n'

		return soutput

	def ps_to_tree(self):

		self._find_nodes()

		while self.curr_node.parent: # get to the top of the tree

			self.curr_node = self.curr_node.parent

		return self.curr_node
