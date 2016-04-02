import cv2
import sys
import os

if len(sys.argv) <= 1:
    print "Usage: greyscale Path/to/Image"
    sys.exit(-1)
elif not os.path.exists(sys.argv[1]):
    print "File not found"
    sys.exit(-1)

filename = sys.argv[1]

img = cv2.imread(filename);
img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

cv2.imwrite("grey.png", img)
