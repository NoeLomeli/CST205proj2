# The goal of this project is to take a photograph using the webcam and then compare the
# face of the person in the photograph with the database of people and try to find a match.

# This project takes an image with the webcam.  Once the image is captured it is converted,
# cropped and saved as a .gif
# The gif file can be selected to be compared with a database of different people by selecting
# the parsed folder
# Once the folder is selected, the user will be asked to enter the amount of faces to create the eigenface
# and the threshold value.  The program will then compare the new image with the eigenface and try to find a match.
import  sys
import numpy as np
import cv2
from cv2 import *
from faceReco import *
from PIL import Image
import Tkinter, tkFileDialog
from string import split
from os.path import join,basename
from eigenfaces import egface
root = Tkinter.Tk()


class PyFaces:
    def __init__(self,testimg,imgsdir,egfnum,thrsh):
        self.testimg=testimg
        self.imgsdir=imgsdir
        self.threshold=thrsh
        self.egfnum=egfnum
        extn=split(basename(testimg),'.')[1]
        print "to match:",self.testimg," to all ",extn," images in directory:",dirname
        self.facet=egface()
        self.egfnum=self.setselectedeigenfaces(self.egfnum,extn)
        print "num of eigenfaces used:",self.egfnum
        try:
            self.facet.checkCache(self.imgsdir,extn,self.imgnamelist,self.egfnum,self.threshold)
        except Exception, inst:
            print "failed :",inst.message
        else:
            mindist,matchfile=self.facet.findmatchingimage(self.testimg,self.egfnum,self.threshold)
            if not matchfile:
                print "NOMATCH! try higher threshold"
            else:
                img = Image.open(matchfile)
                img.show()

                print "matches :"+matchfile+" dist :"+str(mindist)




    def setselectedeigenfaces(self,selectedeigenfaces,ext):
        #call eigenfaces.parsefolder() and get imagenamelist
        self.imgnamelist=self.facet.parsefolder(self.imgsdir,ext)
        numimgs=len(self.imgnamelist)
        if(selectedeigenfaces >= numimgs  or selectedeigenfaces == 0):
            selectedeigenfaces=numimgs/2
        return selectedeigenfaces


if __name__ == "__main__":
    try:

        # Camera 0 is the integrated web cam on my macbook
        camera_port = 0

        #Number of frames to throw away while the camera adjusts to light levels
        ramp_frames = 30

        # Now we can initialize the camera capture object with the cv2.VideoCapture class.
        # All it needs is the index to a camera port.
        camera = VideoCapture(camera_port)

        # Captures a single image from the camera and returns it in PIL format
        def get_image():
         # read is the easiest way to get a full image out of a VideoCapture object.
         retval, im = camera.read()
         return im

        # Ramp the camera - these frames will be discarded and are only used to allow v4l2
        # to adjust light levels, if necessary
        for i in xrange(ramp_frames):
         temp = get_image()
        print("Taking image...")
        # Take the actual image we want to keep
        camera_capture = get_image()
        cv2.imwrite("test_image.jpg", camera_capture)
        file = cv2.imread("test_image.jpg")
        print file
        # A nice feature of the imwrite method is that it will automatically choose the
        # correct format based on the file extension you provide. Convenient!
        # Load a color image

        img = file
        #convert RGB image to Gray
        img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        #Display the gray image
        cv2.imshow('gray_image',img)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
        facedata = "haarcascade_frontalface_default.xml"
        cascade = cv2.CascadeClassifier(facedata)
        DetectFace(img, cascade)

        cv2.imwrite("test_image.jpg", img)
        img = Image.open("test_image.jpg")
        img.save('/Users/Sinistro/Documents/CST205/Eigenfaces/pyfaces/Images/probes/test_image.gif', 'GIF')
        img.show()

        # You'll want to release the camera, otherwise you won't be able to create a new
        # capture object until your script exits
        del(camera)
        # Once the image is saved into the probes directory, this window will allow you to select it
        imgname=tkFileDialog.askopenfilename()
        # The gallery directory holds the faces database and you will need to select it to be able to make an Eigenface
        # and compare the new image to the Eigenface
        dirname=tkFileDialog.askdirectory(parent=root, initialdir="/",title='Please select a directory')
        egfaces = raw_input("Number of faces: ")
        thrshld = raw_input("Threshold: ")
        pyf=PyFaces(imgname,dirname,egfaces,thrshld)
    except Exception,detail:
        print detail
        print "usage:python pyfaces.py imgname dirname numofeigenfaces threshold "
root.mainloop()
