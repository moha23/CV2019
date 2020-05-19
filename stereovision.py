# Used data from http://vision.middlebury.edu/stereo/data/
# For 2-view example this code uses, http://vision.middlebury.edu/stereo/data/scenes2006/FullSize/zip-2views/Aloe-2views.zip
# We have two views, and the disparity map relates them as "a value of 10 in disp1.png means 
# that the corresponding pixel in view5.png is 10 pixels to the left"
# So the code below uses disp1.png and view5.png to get view1.png.
# Similarly, the other disparity map (disp5.png) can be used to get view5.png from view1.png (t = j + d2[i,j])

import cv2
import numpy as np

im1 = cv2.imread("view1.png")
im2 = cv2.imread("view5.png")

d1 = cv2.imread("disp1.png",cv2.IMREAD_GRAYSCALE)

new = np.zeros(np.shape(im1))


for i in range(np.shape(im1)[0]):
    for j in range(np.shape(im1)[1]):
        if d1[i,j] != 0 :
            # opencv reads the image as [column, row, channel]
            t = j - d1[i,j]
            if(t>=0 and t<np.shape(im1)[1]):
                new[i,j,:] = im2[i,t,:]

cv2.imwrite("new.png",new)
