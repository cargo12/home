#!/usr/bin/env python

# Baavgai's Openbox Pipemenus (BOP)
# BOP All: gathers up all other pipe menus using BOP design, for one stop testing or lazy menu inclusion.
#
# current version at http://chaingang.org/code/linux/obscripts/bop_all.py
# requires boplib.py found at http://chaingang.org/code/linux/obscripts/boplib.py
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

from boplib import MenuWriter, PrintFileHeadFoot, PrintEmptyItem
import os, re, sys

# note, -1 means it's not showing up in this list
def GetMenuSequence(): return -1

def GetMenuName(): return 'All Menus'

def ShowMenu():
	mw = MenuWriter('all')
	cwd = os.path.realpath(os.path.dirname(sys.argv[0]))
	modules = []
	
	def ProcessDir(fileName):
		m = re.search('^(bop_.*).py$',fileName)
		if m:
			modName = m.group(1)
			try: 
				mod = __import__(modName)
				try:
					seq = mod.GetMenuSequence()
					if seq>0:
						modules.append([mod.GetMenuSequence(), mod.GetMenuName(), fileName])
				except:
					pass
			except ImportError: 
				pass
				
	def ProcessModule(item):
		(label, fileName) = item[1:]
		execute = os.path.join(cwd, fileName)
		mw.PrintExecMenu(label, execute)
		
	def CmpModules(x, y): return cmp(x[0], y[0])
		
	map(ProcessDir, os.listdir(cwd))
	modules.sort(CmpModules)
	map(ProcessModule, modules)
	
if __name__ == '__main__': PrintFileHeadFoot(ShowMenu)
