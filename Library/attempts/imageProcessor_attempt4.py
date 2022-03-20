import cv2
import numpy as np
import os, shutil
from time import sleep

def processFrame(frame, frames):
	mask=np.ones((5,5),np.uint8)

	#convert to hsv deals better with lighting
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	
	#red is on upper and lower of the hsv scale. Requires 2 ranges 
	red_lower_one = np.array([0, 150, 20])
	red_upper_one = np.array([10, 255, 255])
	red_lower_two = np.array([160,100,20])
	red_upper_two = np.array([179,255,255])

	#masks input image with upper and lower red ranges
	red_part_one = cv2.inRange(hsv, red_lower_one, red_upper_one)
	red_part_two = cv2.inRange(hsv, red_lower_two , red_upper_two)
	red_only = red_part_one + red_part_two

	# HSV range for blue
	blue_lower = np.array([84,150,20])
	blue_upper = np.array([126,255,255])

	blue_only = cv2.inRange(hsv, blue_lower, blue_upper)

	mask=np.ones((5,5),np.uint8)
	
	#run an opening to get rid of any noise
	red_opening=cv2.morphologyEx(red_only,cv2.MORPH_CLOSE,mask)
	blue_opening=cv2.morphologyEx(blue_only,cv2.MORPH_CLOSE,mask)

	cv2.imwrite(f'./Frames/red_{frames}.png', red_opening)
	cv2.imwrite(f'./Frames/blue_{frames}.png', blue_opening)

	#run connected components algo to return all objects it sees.       
	red_num_labels, red_labels, red_stats, red_centroids = cv2.connectedComponentsWithStats(red_opening,4, cv2.CV_32S)
	blue_b=np.matrix(red_labels)

	#run connected components algo to return all objects it sees.       
	blue_num_labels, blue_labels, blue_stats, blue_centroids = cv2.connectedComponentsWithStats(blue_opening,4, cv2.CV_32S)
	blue_b=np.matrix(blue_labels)

	if (blue_num_labels > 1):
		print ('Found blue arrow, turning right')
		return 1
	elif (red_num_labels > 1):
		print ('Found red arrow, turning left')
		return -1
	else:
		print ('No arrow detected, going straight')
		return 0

if __name__ == "__main__":
	cap=cv2.VideoCapture(0)
	cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
	cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

	if not os.path.exists("./Frames/"):
		os.mkdir("./Frames")
		print("Created new directory for logging frames")
	else:
		shutil.rmtree('./Frames')
		os.mkdir('./Frames')
		print ('Re-created frames directory')

	frames = 0

	try:
		while(1):
			_,frame = cap.read()
			processFrame(frame, frames)
			frames += 1
			sleep(0.5)
	except KeyboardInterrupt:
		pass