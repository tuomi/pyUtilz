#!/usr/bin/python
import os, sys, re

def findMatchingF(root, function):
	l = []
	for dirpath, dirnames, fnames in os.walk(root):
		for f in fnames:
			fullF = os.path.join(dirpath, f)
			if function(fullF):
				l.append(fullF)
	return l

# lists all files that contain declaration of variable of a type firstCrit, and then that variable appears with secondCrit on a line
# assumes that the variable name is of the form firstCrit varName = ...
def checkFile(fname, criteria):
	wss = "[ \t]*"
	varEx = re.compile('.*' + criteria[0] + wss + "([^= \t]*)" + wss + "=.*")
	varNames = []
	
	for line in open(fname, 'r').readlines():
		m = varEx.match(line)
		if(m):
			# print 'found variable ' + m.groups()[0]
			varNames.append(re.compile(".*" + m.groups()[0] + ".*" + criteria[1] + ".*"))
		for var in varNames:
			m = var.match(line)
			if(m):
				return True
			# QUE: possibly return list of all matching lines

if __name__ == "__main__":
	result = findMatchingF(sys.argv[1], lambda fname : checkFile(fname, sys.argv[2:]))
	if not result:
		print 'nothing found'
	else:
		for f in result:
			print 'found match in ' + f
