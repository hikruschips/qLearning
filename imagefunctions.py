import numpy as np
import cv2
xk = np.full((1,2),0,dtype = np.int8)
xk[0][0] = 1
xk[0][1] = -1

yk = np.full((2,1),0,dtype = np.int8)
yk[0][0] = 1
yk[1][0] = -1

boxblurk = np.full((3,3),1/9,dtype = np.float_)

prewitk = np.full((3,3),0,dtype = np.int8)
for x in range(0,3):
	prewitk[x][0] = -2
	prewitk[x][2] = 2

def applykernel(image,k):
	height,width = image.shape
	array = np.full((height,width),0,dtype = np.uint8)
	kheight,kwidth = k.shape
	for x in range(0,height-kheight):
		for y in range(0,width-kwidth):
			for u in range(0,kheight):
				for v in range(0,kwidth):
					array[x][y] =array[x][y]+(image[x+u][y+v]*k[u][v])
	return array
def gradient(image,k1,k2):
	height,width = image.shape
	array = np.full((height,width),0,dtype = np.uint8)
	k1array = applykernel(image,k1)
	k2array = applykernel(image,k2)
	for x in range(0,height):
		for y in range(0,width):
			array[x][y] = np.sqrt(np.power(k1array[x][y],2)+np.power(k2array[x][y],2))
	return array
def getuserimage():
	name = raw_input("Enter picture name with extension: ")
	image = cv2.imread("/Users/hikaruinoue/Desktop/python/linearfilterpics/"+name,0)
	return image
def showimage(image,name = 'image'):
	cv2.imshow(name,image)
	cv2.waitKey(0)
	cv2.destroyAllWindows
def ssd(image1,image2):
	height1,width1 = image1.shape
	height2,width2 = image2.shape
	array = np.full((height2-height1,width2-width1),0,dtype = np.uint8)
	image3 = cv2.cvtColor(image2,cv2.COLOR_GRAY2RGB)

	for x2 in range(height2-height1-1):
		for y2 in range(width2-width1-1):
			temp = 0
			for x1 in range(height1):
				for y1 in range(width1):
					temp+=int(np.power(int(int(image1[x1][y1]) - int(image2[x2+x1][y2+y1])),2))
			array[x2][y2] = np.sqrt(temp)
			cv2.imshow('ssd',array)
			cv2.waitKey(1)
			cv2.destroyAllWindows
				
	return image3
def getmapfromimage(image,pathcolor = 'white'):
	height,width = image.shape
	array = [[0]*width for _ in range(height)]
	for x in range(height):
		for y in range(width):
			if image[x][y]<150:
				if pathcolor == 'black':
					array[x][y]='0'
				elif pathcolor == 'white':
					array[x][y]='w'
			elif image[x][y]>=150:
				if pathcolor == 'black':
					array[x][y]='w'
				elif pathcolor == 'white':
					array[x][y] = '0'
	return array

