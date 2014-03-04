#!/usr/bin/env python

# Baavgai's Openbox Pipemenus (BOP)
# BOP Gnome Menu
#
# current version at http://chaingang.org/code/linux/obscripts/bop_gmenu.py
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


from boplib import *
import gtk, gmenu

def GetMenuSequence(): return 1000

def GetMenuName(): return 'Gnome Menu'

def ShowMenu():
	mw = MenuWriter('menu')
	
	def WalkMenuTreeBranch(node):
		for child in node.contents:
			if isinstance (child, gmenu.Directory):
				WalkMenuTree(child)

			if not isinstance (child, gmenu.Entry):
				continue

			if child.type == gmenu.TYPE_ENTRY:
				PrintExecItem(child.name, child.get_exec())

	def WalkMenuTree(node):
		mw.PrintMenuBegin(node.name)
		WalkMenuTreeBranch(node)
		mw.PrintMenuEnd()
	WalkMenuTreeBranch(gmenu.lookup_tree("applications.menu", gmenu.FLAGS_INCLUDE_EXCLUDED).root)

if __name__ == '__main__': PrintFileHeadFoot(ShowMenu)