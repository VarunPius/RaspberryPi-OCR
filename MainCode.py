#!/usr/bin/python

# Author: Varun Pius Rodrigues
# Credits: Patrick Emami
# Code was apart of HackerU event at University of Florida; Patrick helped me out with parts of code.

# Get access to all of Adafruit's printer python modules
from Adafruit_Thermal import *
# Import OpenCV python modules
import cv2
# Import the python-tesseract modules
import tesseract
# For sleeping the process
import time 

# Loops infinitely until the user presses 'q'
# at which time an image will be snapped
def capture():

	while(True):	
		# Capture frame-by-frame
        	ret, frame = cap.read()

       		# Convert the captured frame to grayscale
        	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        	# Display the resulting frame
        	cv2.imshow('frame',gray)

		# When the user presses q, return the current frame
        	if cv2.waitKey(1) & 0xFF == ord('q'):
        		return gray

if __name__ == '__main__':
	# new videocapture object
	cap = cv2.VideoCapture(0)

	# Create a Adafruit_Thermal object that we can use for printing
	printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)		

	# python-tesseract initialization
	api = tesseract.TessBaseAPI()
	api.SetOutputName("hacker_u")
	api.Init(".","eng",tesseract.OEM_DEFAULT)
	api.SetPageSegMode(tesseract.PSM_AUTO)

	printer.boldOn()	# Make text bold
	printer.setSize('L')    # Set type size, accepts 'S', 'M', 'L'
	printer.justify('C')	# Center the text to leave lots of whitespace 

	while(True):
		''' Prompt the user to enter some text to be recognized by python-tesseract '''
		text_to_print = raw_input("Enter text: ")	
		
		# Alert user that we are printing
		print("Printing...")	
	
		''' Print the user's text out '''
		printer.println(text_to_print)
		
		time.sleep(1)	
		
		print "Tear off the printed text from printer and show it to the webcam!"
		print "Press 'q' to snap the picture"

		# store frame in variable img
		img = capture()

		# scale the image up to twice its size to assist with OCR
		scaled_img = cv2.resize(img,None,fx=2,fy=2,interpolation=cv2.INTER_CUBIC)

		# Intermediate step to convert the image into a format usable by py-tesseract
		cv2.imwrite("tmp.jpg", scaled_img)
		cv_image = cv2.cv.LoadImage("tmp.jpg", cv2.cv.CV_LOAD_IMAGE_GRAYSCALE)

		''' Call python-teseract and attempt to decode text in image '''
		tesseract.SetCvImage(cv_image, api)
		result = api.GetUTF8Text()
		conf = api.MeanTextConf()
	
		# Remove unecessary whitespace from output text
		result.strip()
		if result: 
			''' Print out result '''
			printer.println("You said")
			printer.println(result)
			print "OCR success: ", result
			print "Confidence level: %d %%"%conf
		else: 
			print "OCR failed, please try again!"
	
	tess.End()
	# When everythings done, release the capture
	cap.release()
	cv2.destroyAllWindows()
