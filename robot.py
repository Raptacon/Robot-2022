"""
Team 3200 Robot base class
"""
from wpilib import XboxController
import wpilib
from magicbot import MagicRobot
import robotMap

import components.dtFxTest
import components.driveTrain

class MyRobot(MagicRobot):
    """
    Base robot class of Magic Bot Type
    """

    driveTrain: components.driveTrain.DriveTrain

    def createObjects(self):
        """
        Robot-wide initialization code should go here. Replaces robotInit
        """
        self.left = 0
        self.right = 0
        self.stick = XboxController(0)
        self.map = robotMap.RobotMap()
        self.driveTrain_motorsList = self.map.motorsMap.driveMotors

    def teleopPeriodic(self):
        """
        Must include. Called ruing teleop.
        """
        self.left = self.stick.getRawAxis(1)
        self.rot = self.stick.getRawAxis(0)
        self.driveTrain.setArcade(self.left, self.rot)

    def testInit(self):
        """
        Function called when testInit is called. Crashes on 2nd call right now
        """
        pass
        #print("Stick %s, left %s, right %s", self.stick, self.left, self.right)

    def testPeriodic(self):
        """
        Called during test mode alot
        """
        pass


if __name__ == '__main__':
    wpilib.run(MyRobot)