from adafruit_pca9685 import PCA9685
from Library import config as cfg
from board import SDA, SCL
import busio
from Library.PWMCalculator import valToDuty

def stopCar():
	i2c = busio.I2C(SCL, SDA)
	pca = PCA9685(i2c)

	throttle_channel = pca.channels[cfg.THROTTLE_PWM_CHANNEL]
	steering_channel = pca.channels[cfg.STEERING_PWM_CHANNEL]

	pca.frequency = cfg.PWM_FREQ_HZ

	throttle_channel.duty_cycle = valToDuty(cfg.THROTTLE_NEUTRAL)
	steering_channel.duty_cycle = valToDuty(cfg.STEERING_STRAIGHT_PWM)

if __name__ == "__main__":
	stopCar()