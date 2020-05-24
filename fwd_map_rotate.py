# First assignment: Forward map (rotation)
# Apply rotation matrix to each pixel vector [x y] to find it's new position vextor [x' y']
# in the rotated image. Since it's a forward map, a position in output image may have been addressed
# multiple times or not at all. Hence, overlap / 'holes' in the output image is expected.

import numpy as np
import cv2
import math


image = cv2.imread('/path/to/image.png')
image = image.astype(int)
rows,columns,ch = np.shape(image)

angle = 30
theta = np.radians(angle)
c, s = np.cos(theta), np.sin(theta)
rotation_array = np.array(((c,-s), (s, c)))
print(rotation_array)

new_image = np.zeros([rows,columns,ch])
new_image = new_image.astype(int)
 

#rotation
for c in range(ch):
	for px in range(rows):
		for py in range(columns):
			ip_vector = np.array([px,py])
			ip_vector.shape=(2,1)
			op_vector = np.dot(rotation_array,ip_vector)
			[px_dash,py_dash]=op_vector
			if np.logical_and(np.logical_and(np.logical_and(px_dash >= 0, px_dash < rows),py_dash >= 0 ),py_dash<columns):
					new_image[int(px_dash),int(py_dash),c]=image[px,py,c]

cv2.imwrite('fwd_map_rotate.png',new_image)
