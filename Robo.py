import time
import asyncio

from board import SCL, SDA
import busio

from adafruit_pca9685 import PCA9685
from adafruit_motor import servo


class Joint:

    def __init__(self, nr, min_angle, rest_angle, max_angle):
        i2c_bus = busio.I2C(SCL, SDA)
        pca = PCA9685(i2c_bus, address=0x41)
        pca.frequency = 60

        self.servo = servo.Servo(pca.channels[nr], min_pulse=500, max_pulse=2400)
        self.angle = 0

        self.restpoint = rest_angle
        self.max_angle = max_angle
        self.min_angle = min_angle

    def get_angle(self):
        return self.angle

    def move_to_rest(self):
        self.set_angle(self.restpoint)

    def set_angle(self, ang):
        self.servo.angle = ang
        self.angle = ang

    def set_angle_rel(self, rel):
        if rel == -1:
            self.angle -= 1
            self.servo.angle = self.angle
        elif rel == +1:
            self.angle += 1
            self.servo.angle = self.angle


class Robo:
    def __init__(self):

        self.l_foot = Joint(0, 0, 100, 180)
        self.l_hip = Joint(1, 0, 97, 180)
        self.r_foot = Joint(2, 0, 100, 180)
        self.r_hip = Joint(3, 0, 97, 180)

        self.joints = [self.l_foot, self.l_hip, self.r_foot, self.r_hip]

    # -----------------------------------------------------

    def pose_default_start(self):
        self.l_foot.move_to_rest()
        self.l_hip.move_to_rest()
        self.r_foot.move_to_rest()
        self.r_hip.move_to_rest()

        time.sleep(0.5)

    # ------------------------------------------------------

    def move_joint_vel(self, jnt, ang, vel):  # could make this async
        if vel > 0 and vel <= 10 and jnt >= 0 and jnt < 4:
            while (ang != self.joints[jnt].get_angle()):
                if ang < self.joints[jnt].get_angle():
                    self.joints[jnt].set_angle_rel(-1)
                elif ang > self.joints[jnt].get_angle():
                    self.joints[jnt].set_angle_rel(+1)
                time.sleep((11 - vel) / 100)

    def move_joint_resting(self, jnt, vel):
        if vel > 0 and vel <= 10 and jnt >= 0 and jnt < 4:
            self.move_joint_vel(jnt, self.joints[jnt].restpoint, vel)

    def move_joint_rel_vel(self, jnt, ang, vel):
        if vel > 0 and vel <= 10 and jnt >= 0 and jnt < 4:
            self.move_joint_vel(jnt, self.joints[jnt].get_angle() + ang, vel)


def raise_r_leg():
    robo.move_joint_rel_vel(2, 40, 10)
    robo.move_joint_rel_vel(0, 25, 9)
    robo.move_joint_resting(2, 10)


def move_r_leg():  # this should not be rel
    robo.move_joint_rel_vel(3, -30, 9)
    robo.move_joint_rel_vel(1, -30, 9)


def lower_r_leg():
    robo.move_joint_resting(0, 6)


def raise_l_leg():
    robo.move_joint_rel_vel(0, -40, 10)
    robo.move_joint_rel_vel(2, -25, 9)
    robo.move_joint_resting(0, 10)


def move_l_leg():  # this should not be rel
    robo.move_joint_rel_vel(1, 30, 9)
    robo.move_joint_rel_vel(3, 30, 9)


def lower_l_leg():
    robo.move_joint_resting(2, 6)


def robo_step_l():
    raise_r_leg()
    move_r_leg()
    lower_r_leg()

    raise_l_leg()

    robo.move_joint_resting(3, 10)
    robo.move_joint_resting(1, 10)

    lower_l_leg()


def robo_step_r():
    raise_l_leg()
    move_l_leg()
    lower_l_leg()

    raise_r_leg()

    robo.move_joint_resting(3, 10)
    robo.move_joint_resting(1, 10)

    lower_r_leg()


def robo_turn_r():
    raise_r_leg()

    robo.move_joint_rel_vel(1, -15, 9)
    robo.move_joint_rel_vel(3, 15, 9)

    lower_r_leg()
    raise_l_leg()

    robo.move_joint_resting(3, 10)
    robo.move_joint_resting(1, 10)

    lower_l_leg()


def robo_shoot_r():
    raise_r_leg()
    move_l_leg()
    robo.move_joint_rel_vel(0, 5, 5)

    robo.move_joint_rel_vel(2, 30, 5)
    time.sleep(1)
    robo.move_joint_rel_vel(3, 10, 5)
    time.sleep(1)
    robo.move_joint_rel_vel(1, -40, 10)
    time.sleep(1)
    robo.move_joint_rel_vel(2, -50, 10)
    time.sleep(1)
    robo.move_joint_resting(3, 7)
    robo.move_joint_resting(3, 5)
    lower_r_leg()


if __name__ == '__main__':
    robo = Robo()

    robo.pose_default_start()

    time.sleep(1)

    robo_shoot_r()
    time.sleep(1)

    robo.pose_default_start()

