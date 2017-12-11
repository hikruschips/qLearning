from somefunctions import changesys
changesys()
import numpy as np
import cv2
from imagefunctions import *

image = getuserimage()
array = getmapfromimage(image)
array = np.array(array)
height,width = array.shape
print height,width
for x in range(height):
	temp = ''
	for y in range(width):
		temp +=  array[x][y]+' '
	print temp

