
"""
Team 3200 Robot base class
"""
from wpilib import XboxController
import wpilib
from magicbot import MagicRobot
from robotMap import RobotMap
from components.driveTrain import DriveTrain


class MyRobot(MagicRobot):
    """
    Base robot class of Magic Bot Type
    """


    driveTrain: DriveTrain

    def createObjects(self):
        """
        Robot-wide initialization code should go here. Replaces robotInit
        """
        self.map = RobotMap()
        self.left = 0
        self.right = 0
        self.stick = XboxController(0)
        self.driveTrain_motorsList = dict(self.map.motorsMap.driveMotors)

    def teleopPeriodic(self):
        """
        Must include. Called running teleop.
        """
        self.controllerInput()
        self.driveTrain.setArcade(self.left / 2, -self.rightHoriz / 2)

    def testInit(self):
        """
        Function called when testInit is called. Crashes on 2nd call right now
        """
        pass
        
    def testPeriodic(self):
        """
        Called during test mode alot
        """
        pass

    def controllerInput(self):
        """
        Collects all controller values and puts them in an easily readable format
        """
        self.left = self.stick.getRawAxis(1)
        self.right = self.stick.getRawAxis(5)
        self.leftHoriz = self.stick.getRawAxis(0)
        self.rightHoriz = self.stick.getRawAxis(4)


if __name__ == '__main__':
    wpilib.run(MyRobot)
