import re
from somefunctions import *
changesys()
import numpy as np
import cv2
import random
import copy
import time
diagonal = False
playercolor = [201,136,94]
wallcolor = [75,153,242]
goalcolor = [99,218,81]
fallcolor = [81,81,218]
statecolor = [150,50,255]
showaftersometime = True;
showafter = 100;
totaliteration = 200000;


fname = raw_input('Enter file name: ')
f = open('/Users/hikaruinoue/desktop/python/text/'+fname,'r')
if f.mode == 'r':
	contents = f.read()
	tokens = re.findall(r'\S+',contents)
	height = toint(tokens[0],'w')
	width = toint(tokens[1],'w')
	tokenint = 2
	r = [[0]*(width*height) for _ in range(height*width)]
	q = [[0]*(width*height) for _ in range(height*width)]
	array = [[0]*width for _ in range(height)]
	tempa = 0
	temprarray = [[0]*width for _ in range(height)]
	states = []
	statecount = width*height
	temprlist = []
	map = [[[0]*3 for _ in range(width)] for _ in range(height)]
	mapdash = [[[0]*3 for _ in range(width)] for _ in range(height)]
	
	for x in range(height):
		for y in range(width):
			array[x][y] = tempa
			states = tempa
			temprlist.append(tokens[tokenint])
			tempa+=1
			temprarray[x][y] = tokens[tokenint]
			
			map[x][y] = [153,255,255]

			if temprarray[x][y] == 'w':
				map[x][y] = wallcolor
			elif temprarray[x][y]=='100':
				map[x][y] = goalcolor
			elif representsint(temprarray[x][y]):
				if int(temprarray[x][y])<0:
					
					map[x][y] = fallcolor
			 

			tokenint+=1
	mapdash = copy.deepcopy(map)

	tokenint =2

	

	stateactions = [0]*(height*width)

	for x in range(height*width):
		tempaction = []
		for y in range(width*height):
			xrow = getrow(x,array,height,width)
			xcol = getcolumn(x,array,height,width)
			yrow = getrow(y,array,height,width)
			ycol = getcolumn(y,array,height,width)

			if np.absolute(xrow-yrow)<=1 and np.absolute(xcol-ycol)<=1 and np.absolute(xrow-yrow)!=np.absolute(xcol-ycol) and temprarray[yrow][ycol]!='w':

				
				tempaction.append(y)
		stateactions[x] = tempaction

	goalstate = temprlist.index('100')

	tempx=0
	for actions in stateactions:
		
		for action in actions:
			r[tempx][action] = toint(temprlist[action],'w')
			if action == goalstate:
				r[tempx][goalstate] = 100
		tempx+=1
	
	def maxq(state):
		maxvalue = 2.2250738585072014e-308
		for i in stateactions[state]:
			value = q[state][i]
			if value>maxvalue:
				maxvalue = value
		return maxvalue
	def policy(state):
		maxvalue = 2.2250738585072014e-308
		policy = state
		for i in stateactions[state]:
			value = q[state][i]
			if value>maxvalue:
				maxvalue = value
				policy = i
		return policy



	alpha = 0.1
	gamma = 0.9
	player = temprlist.index('0')
	state = 0

	y = 0

	def changeplayeranddisplay():
		global player
		global mapdash
		global map
		if player==goalstate:
			player = temprlist.index('0')
		#time.sleep(0.1)

		mapdash[getrow(player,array,height,width)][getcolumn(player,array,height,width)] = playercolor
		mapdash[getrow(state,array,height,width)][getcolumn(state,array,height,width)] = statecolor

		cv2.imshow('image',np.array(mapdash,dtype = np.uint8))
		cv2.waitKey(1)
		mapdash = copy.deepcopy(map)


		if player == policy(player):
			player = stateactions[player][random.randint(0,len(stateactions[player])-1)]
		else:
			player = policy(player)
		return
		if policy(policy(player))==player:
			player = temprlist.index('0')
	

	for x in range(0,totaliteration):

		print x
		

		if showaftersometime:
			if x>showafter:
				changeplayeranddisplay()
		else:
			changeplayeranddisplay()
		
		
		state = random.randint(0,statecount-1)

		
		if temprlist[state]!='w' and len(stateactions[state])!=0:
			while(state!=goalstate) and len(stateactions[state])!=0:
				
				action = stateactions[state][random.randint(0,len(stateactions[state])-1)]
				
				nextstate = action
				value = q[state][action] + alpha*(r[state][action] +maxq(nextstate)*gamma - q[state][action])
				q[state][action] = value
					
				if showaftersometime:
					if x>showafter:
						changeplayeranddisplay()
				else:
					changeplayeranddisplay()
				
				state = nextstate
	
	print actions
	for x in range(0,statecount):
		if temprlist[x]!='w':
			fromm = x
			to = policy(x)
			print 'from '+str(fromm)+' go to '+str(to)