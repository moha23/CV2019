# First assignment: Backward map (rotation)
# Iterate over each pixel in output image and apply inverse transformation
# to determine position in input image from which values are sampled.
# Since inverse transformation can give non integer numbers, we use bilinear 
# interpolation for sampling the value. Compared with forward mapping, there 
# should be no 'holes' since each output pixel is accounted for.

import numpy as np
import cv2
from numpy.linalg import inv
import math


image = cv2.imread('image.png')
image = image.astype(int)

rows,columns,ch = np.shape(image)

angle = -20
theta = np.radians(angle)
c, s = np.cos(theta), np.sin(theta)
rotation_array = np.array(((c,-s), (s, c)))
inv_rotation_array = np.linalg.inv(rotation_array)

new_image = np.zeros([rows,columns,ch])
new_image = new_image.astype(int)
	
#rotation
for c in range(ch):
	for px in range(rows):
		for py in range(columns):
			
			op_vector = np.array([px,py])
			op_vector.shape=(2,1)
			ip_vector = np.dot(inv_rotation_array,op_vector)
			[px_dash,py_dash]=ip_vector
			
			#bilinear interpolation
			x = math.floor(px_dash)
			y = math.floor(py_dash)
			if x >= 0 and x <rows and y >= 0 and y < columns:
				x1 =  x+1
				y1 = y+1
				if x1 >= 0 and x1 <rows and y1 >= 0 and y1 < columns:
					alpha = y - py_dash
					beta = px_dash - x
					value = ((1-alpha)*(1-beta)*image[x,y,c]) + ((1-alpha)*(beta)*image[x1,y,c]) + ((alpha)*(1-beta)*image[x,y1,c]) + ((alpha)*(beta)*image[x1,y1,c])
					new_image[px,py,c] = value
				elif x1 >= rows:
					alpha = y - py_dash
					beta = px_dash - x
					value = ((1-alpha)*(1-beta)*image[x,y,c]) + ((alpha)*(1-beta)*image[x,y1,c])
					new_image[px,py,c] = value
				elif y1 >= columns:
					alpha = y - py_dash
					beta = px_dash - x
					value = ((1-alpha)*(1-beta)*image[x,y,c]) + ((1-alpha)*(beta)*image[x1,y,c])
					new_image[px,py,c] = value
			else:
				new_image[px,py,c] = 0
				
cv2.imwrite('bwd_map_rotate.png',new_image)
