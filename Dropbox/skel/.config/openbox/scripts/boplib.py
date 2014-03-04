#!/usr/bin/env python

# Baavgai's Openbox Pipemenus (BOP)
# BOP Common Library: All "BOP" files need this
# current version at http://chaingang.org/code/linux/obscripts/boplib.py
#
# Copyright 2008 Baavgai (baavgai@chaingang.org)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re, binascii

FileManagerMask = "nautilus %s"

class MenuWriter:
	def __init__(self, menuPrefix):
		self.idCount = 0
		self.menuPrefix = menuPrefix

	def __GetNextMenuId(self):
		self.idCount += 1
		return 'bop_%s_%s' % (self.menuPrefix, self.idCount)

	def PrintMenuBegin(self, label):
		print '<menu id="%s" label="%s">' % (self.__GetNextMenuId(), EscEntity(label))

	def PrintMenuEnd(self):
		print '</menu>'

	def PrintMenu(self, label, func):
		self.PrintMenuBegin(label)
		func()
		self.PrintMenuEnd()

	def PrintExecMenu(self, label, execute):
		print '<menu id="%s" label="%s" execute="%s" />' % (self.__GetNextMenuId(), EscEntity(label), EscEntity(execute))


def EscEntity(text):
	for (k, v) in [['&','&amp;'],['<','&lt;'],['>','&gt;'],["'",'&apos;'],['"','&quot;'] ]:
		text = text.replace(k,v)
	return text


def EscUri(text):
	def UriRep(match):
		return binascii.unhexlify(match.group(0).replace('%',''))
	text = re.sub('\%..', UriRep, text)
	text = text.replace('_','__')
	return text

def PrintEmptyItem(label):
	print '<item label="%s"></item>' % EscEntity(label)

def PrintExecItem(label, cmd):
	print '<item label="%s">' % EscEntity(label)
	print '<action name="Execute"><execute>%s</execute></action>' % EscEntity(cmd)
	print '</item>'


def PrintFileManagerItem(label, uri):
	PrintExecItem(label, FileManagerMask % uri)


def PrintFileHeadFoot(func):
	print '<?xml version="1.0" encoding="UTF-8"?>'
	print '<openbox_pipe_menu>'
	func()
	print '</openbox_pipe_menu>'


def GetLabelPath(path):
	cmdBits = path.split('/')
	label = cmdBits[len(cmdBits)-1]
	if len(cmdBits)>2:
		server = cmdBits[2].strip()
		if (server):
			label += ' on ' + server
	return (EscUri(label), path)
