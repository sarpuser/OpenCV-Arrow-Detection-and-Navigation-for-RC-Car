# Arrow direction detection using Python OpenCV, integrated with Adafruit PCA9685 PWM controller

## Requirements
pipenv (`pi3 install pipenv`)

## Setup
1. Clone this repo
2. Enter directory
3. Run `pipenv install`: This will install the Python 3.10 (locally) as well as the required packages (also locally).
4. Run `pipenv shell` to enter the pipenv environment
5. If you run `python -V` you should now see 3.10

## Calibration
1. Run the `testPWM.py` file
2. Select 1 for testing steering PWM values and 2 for throttle PWM values
3. Enter values. These values should be less than 4069 will result in the value/4096 being set as the duty cycle.
4. Save your values in `config.py`

## Running the car
- Run `signDetection.py` to process images in real time and send according PWM values.
- Run `stopCar.py` at anytime to send a neutral to the ESC and get the steering back to normal. The `KeyboardInterrupt` exception in the `signDetection.py` also calls this file to stop the car.

## Credits
The image processing pipeline here has been taken from https://github.com/VyomGarg47/Arrow-Angle-detector. Code has been slightly modified.