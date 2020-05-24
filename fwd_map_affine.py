# First assignment: Forward map (affine)
# Apply affine transformation matrix to each pixel vector [x y] to find it's new position vextor [x' y']
# in the transformed image. Since it's a forward map, a position in output image may have been addressed
# multiple times or not at all. Hence, overlap / 'holes' in the output image is expected.

import numpy as np
import cv2
import math


image = cv2.imread('image.png')
image = image.astype(int)
rows,columns,ch = np.shape(image)

# elements in transformation array are responsible for
# types of transformation, e.g. t_x gives shear in x direction
# Example parameters:
# translation e.g. 1 0 15 0 1 15
# shear e.g. 1 0.2 0 0 1 0 shear in x,
# scale  0.5 0 0 0 1 0 halves in x dir

a=1
b=0.2
t_x=0
c=0.2
d=1
t_y=0

affine_array = np.array(((a,b,t_x), (c, d,t_y),(0,0,1)))

new_image = np.zeros([rows,columns,ch])
new_image = new_image.astype(int)
 
#affine
for c in range(ch):
	for px in range(rows):
		for py in range(columns):
			ip_vector = np.array([px,py,1])
			ip_vector.shape=(3,1)
			op_vector = np.dot(affine_array,ip_vector)
			[px_dash,py_dash,w]=op_vector
			px_dash=px_dash/w
			py_dash=py_dash/w
			if np.logical_and(np.logical_and(np.logical_and(px_dash >= 0, px_dash < rows),py_dash >= 0 ),py_dash<columns):
					new_image[int(px_dash),int(py_dash),c]=image[px,py,c]
					
cv2.imwrite('fwd_map_affine.png',new_image)
