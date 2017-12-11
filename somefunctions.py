def representsint(s):
	try:
		int(s)
		return True
	except ValueError:
		return False
def toint(s,exceptstr):
	if representsint(s):
		return int(s)
	if s == exceptstr:
		return -1
	return 0
def getrow(a,b,height,width):
	for x in range(height):
		for y in range(width):
			try:
				arow = b[x].index(a)
				return x
			except:
				arow = 666
	return arow

def getcolumn(a,b,height,width):
	for x in range(height):
		for y in range(width):
			try:
				arow = b[x].index(a)
				return arow
			except:
				arow = 666
	return arow

def changesys():
	import sys
	sys.path.insert(0, '/Users/hikaruinoue/Library/Python/2.7/lib/python/site-packages')
	return