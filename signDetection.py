from adafruit_pca9685 import PCA9685
import busio
from board import SCL, SDA
import cv2
from time import sleep
from Library import config as cfg
from Library.imageProcessor import processFrame
from Library.PWMCalculator import valToDuty
from stopCar import stopCar
import os, shutil

i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)

throttle_channel = pca.channels[cfg.THROTTLE_PWM_CHANNEL]
steering_channel = pca.channels[cfg.STEERING_PWM_CHANNEL]

pca.frequency = cfg.PWM_FREQ_HZ

cap=cv2.VideoCapture(0)

if not os.path.exists("./Frames/"):
	os.mkdir("./Frames")
	print("Created new directory for logging frames")
else:
	shutil.rmtree('./Frames')
	os.mkdir('./Frames')
	print ('Re-created frames directory')

frames = 0

print ('Init ESC')
throttle_channel.duty_cycle = valToDuty(200)
sleep(0.1)
throttle_channel.duty_cycle = valToDuty(410)
sleep(0.1)
throttle_channel.duty_cycle = valToDuty(cfg.THROTTLE_NEUTRAL)
sleep(1)
print ('ESC init complete')

try:
	throttle_channel.duty_cycle = valToDuty(cfg.THROTTLE_REGULAR)

	while(1):
		# _,frame=cap.read()

		detectedAngle = processFrame()

		if detectedAngle != None:
			if (detectedAngle < 0):
				print ('Detected right arrow, turning right')
				steering_channel.duty_cycle = valToDuty(cfg.STEERING_RIGHT_PWM)
			elif (detectedAngle > 0):
				print ('Detected left arrow, turning left')
				steering_channel.duty_cycle = valToDuty(cfg.STEERING_LEFT_PWM)
		else:
			print ('No arrow detected, going straight')
			steering_channel.duty_cycle = valToDuty(cfg.STEERING_STRAIGHT_PWM)

		frames += 1

except KeyboardInterrupt:
	cap.release()	
	print ('Stopping car')
	stopCar()


	# if (cv2.countNonZero(red_only) == 0 and cv2.countNonZero(blue_only) != 0):
	# 	print ('Detected blue arrow, turning right')
	# 	steering_channel.duty_cycle = valToDuty(cfg.STEERING_RIGHT_PWM)
	# elif (cv2.countNonZero(blue_only) == 0 and cv2.countNonZero(red_only) != 0):
	# 	print ('Detected red arrow, turning left')
	# 	steering_channel.duty_cycle = valToDuty(cfg.STEERING_LEFT_PWM)
	# else:
	# 	print ('No arrow detected, going straight')
	# 	steering_channel.duty_cycle = valToDuty(cfg.STEERING_STRAIGHT_PWM)
