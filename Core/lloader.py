# -*- coding: utf-8 -*-
##
# Library loader
##

from glob import glob
from os import path, remove
from imp import load_source

def main(connection):
	libraries = {}
	if "libraries" in connection.config.paths.keys():
		lpath = connection.config.paths["libraries"]
		if not path.isdir(lpath):
			return {}
	else:
		if path.isdir("Libraries"):
			lpath = "Libraries/"
		elif path.isdir("libraries"):
			lpath = "libraries/"
		else:
			return {}
	for l in glob(lpath + "*.py"):
		fixed = l.replace(lpath, "").replace(".py", "")
		libraries[fixed] = load_source(fixed, l)
	return libraries