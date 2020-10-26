import os
import sys
import time
import smbus

# Import the servo control libraries and dependencies
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

# Import the sensor fusion library to work with absolute angles
from imusensor.MPU9250 import MPU9250

# Create an i2c instance
i2c = busio.I2C(SCL,SDA)

# Create a board instance
pca = PCA9685(i2c)

# Establish board frequency
pca.frequency = 50

# Create the servo object with tuned min and max pulses to allow for
# full 180 degrees of movement. 
servo0 = servo.Servo(pca.channels[0], min_pulse =700, max_pulse=2700)

# Create an instance of the MPU9250 imu
address = 0x68
bus = smbus.SMBus(1)
imu = MPU9250.MPU9250(bus, address)
imu.begin()

# Calibrate the IMU in order to 
imu.caliberateGyro()
imu.caliberateAccelerometer()

# Establish a for calculating the direction of motion
a_previous = 0
a_current = 0

# Reference for control
reference = 90

# Set the initial servo angle to reference and allow for the 
# position. 
servo0.angle = reference
time.sleep(3)

# Establishing a proportional gain 
kp =1.1


# Main operating loop
while True:
	imu.readRawSensor()
	
	a_current = imu.RawAccelVals[1]
	delA = a_current-a_previous
	
	imu.readSensor()
	imu.computeOrientation() 
	
	error = (reference-imu.pitch)
	
	error = kp*error
	
	
	if delA >0 and a_current  >0:
		servo0.angle = 90 + error
	elif delA <0 and a_current  >0:
		servo0.angle = 90 + error
	elif delA >0 and a_current  <0:
	    servo0.angle = 90-error
	elif delA <0 and a_current  <0:
		servo0.angle = 90 - error
	
	a_previous = a_current
	
	time.sleep(0.1)

