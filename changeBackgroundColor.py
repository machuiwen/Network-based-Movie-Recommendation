import cv2
from cv2 import *

if __name__ == '__main__':
	im = imread('ug.png')

	# cv2.imshow("",im)
	# cv2.waitKey()

	t = 30
	for i in range(im.shape[0]):
		for j in range(im.shape[1]):
			if im[i][j][0] <= t and im[i][j][1] <= t and im[i][j][2] <= t:
				im[i][j][0] = 255
				im[i][j][1] = 255
				im[i][j][2] = 255
	imwrite("newug.png", im)