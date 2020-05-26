# First assignment: Backward map (affine)
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

affine_array = np.array(((1,0.2,0), (0, 1,0),(0,0,1)))
inv_affine_array = np.linalg.inv(affine_array)

new_image = np.zeros([rows,columns,ch])
new_image = new_image.astype(int)
 
#affine
for c in range(ch):
	for px in range(rows):
		for py in range(columns):
			
			op_vector = np.array([px,py,1])
			op_vector.shape=(3,1)
			ip_vector = np.dot(inv_affine_array,op_vector)
			[px_dash,py_dash,w]=ip_vector
			px_dash=px_dash/w
			py_dash=py_dash/w
			
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

cv2.imwrite('bwd_map_affine.png',new_image)
