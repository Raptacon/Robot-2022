from magicbot import MagicRobot
from wpilib import DigitalInput as dio
import wpilib

class MyRobot(MagicRobot):

    def createObjects(self):

        self.sensor = dio(0)

    def teleopPeriodic(self):

        print(self.sensor.get())

if __name__ == '__main__':
    wpilib.run(MyRobot)
