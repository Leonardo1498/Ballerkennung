import time

from board import SCL, SDA
import busio

from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

i2c_bus = busio.I2C(SCL, SDA)

pca = PCA9685(i2c_bus, address=0x41)

pca.frequency = 60

servo0 = servo.Servo(pca.channels[0], min_pulse=300, max_pulse=2600)

for i in range(180):
	servo0.angle = i
	time.sleep(0.02)

servo0.angle=90

pca.deinit()

