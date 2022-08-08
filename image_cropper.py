import cv2
import numpy as np
img = cv2.imread("lane.png")

top_row = img[100:500, 0:220]
cv2.imshow("top_row", top_row)
cv2.waitKey(0)