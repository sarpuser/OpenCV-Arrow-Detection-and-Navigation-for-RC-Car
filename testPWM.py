from adafruit_pca9685 import PCA9685
import busio
from board import SCL, SDA
from time import sleep
from Library.PWMCalculator import valToDuty
from Library import config as cfg
from stopCar import stopCar

i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)

throttle_channel = pca.channels[cfg.THROTTLE_PWM_CHANNEL]
steering_channel = pca.channels[cfg.STEERING_PWM_CHANNEL]

pca.frequency = cfg.PWM_FREQ_HZ

print ('Init ESC')
throttle_channel.duty_cycle = valToDuty(200)
sleep(0.1)
throttle_channel.duty_cycle = valToDuty(410)
sleep(0.1)
throttle_channel.duty_cycle = valToDuty(cfg.THROTTLE_NEUTRAL)
sleep(1)
print ('ESC init complete')

try:
	selection = int(input('Please select 1 to calibrate steering and 2 to calibrate throttle: '))
	while (1):
		value = int(input('Enter PWM value (out of 4096) to test: '))

		if selection == 1:
			steering_channel.duty_cycle = valToDuty(value)
		elif selection == 2:
			throttle_channel.duty_cycle = valToDuty(value)

except KeyboardInterrupt:
	print ('Stopping car')
	stopCar()