import cv2
import numpy as np
import os, shutil
from time import sleep

def preprocess(img, frames):
	img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	img_blur = cv2.GaussianBlur(img_gray, (5, 5), 1)
	# img_thresh = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 2)
	img_canny = cv2.Canny(img_blur, 50, 50)
	kernel = np.ones((3, 3))
	img_dilate = cv2.dilate(img_canny, kernel, iterations=2)
	img_erode = cv2.erode(img_dilate, kernel, iterations=1)
	cv2.imwrite(f'./Frames/pre_{frames}.png', img_erode)
	return img_erode

def find_tip(points, convex_hull):
	length = len(points)
	indices = np.setdiff1d(range(length), convex_hull)
	for i in range(2):
		j = indices[i] + 2
		if j > length - 1:
			j = length - j
		if np.all(points[j] == points[indices[i - 1] - 2]):
			return tuple(points[j])
		if j > length - 1:
			j = length - j
		

def extractContours(img, frames):
	contours, hierarchy = cv2.findContours(preprocess(img, frames), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

	for cnt in contours:
		peri = cv2.arcLength(cnt, True)
		approx = cv2.approxPolyDP(cnt, 0.025 * peri, True)
		hull = cv2.convexHull(approx, returnPoints=False)
		sides = len(hull)

	if 6 > sides > 3 and sides + 2 == len(approx):
		print('found arrow')
		arrow_tip = find_tip(approx[:,0,:], hull.squeeze())
		if arrow_tip:
			cv2.drawContours(img, [cnt], -1, (0, 255, 0), 3)
			cv2.circle(img, arrow_tip, 3, (0, 0, 255), cv2.FILLED)
			print('found tip')
			cv2.imwrite(f'./Frames/post_{frames}.png', img)

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
			print('Reading image...')
			_,frame = cap.read()
			extractContours(frame, frames)
			frames += 1
			sleep(10)
	except KeyboardInterrupt:
		pass