
"""
Team 3200 Robot base class
"""
from wpilib import XboxController
import wpilib
from magicbot import MagicRobot
from robotMap import RobotMap
from components.driveTrain import DriveTrain
from components.lifter import Lifter


class MyRobot(MagicRobot):
    """
    Base robot class of Magic Bot Type
    """


    driveTrain: DriveTrain
    lifter: Lifter

    def createObjects(self):
        """
        Robot-wide initialization code should go here. Replaces robotInit
        """
        self.map = RobotMap()
        self.driveLeft = 0
        self.driveRight = 0
        self.driveController = wpilib.XboxController(0)
        self.mechController = wpilib.XboxController(1)
        self.motorsList = dict(self.map.motorsMap.driveMotors)
        self.mult = 1 #Multiplier for values. Should not be over 1.

    def teleopPeriodic(self):
        """
        Must include. Called running teleop.
        """
        self.controllerInput()
        self.driveTrain.setArcade(self.driveLeft, -self.driveLeftHoriz)
        if self.mechA:
            self.lifter.setSpeed(1)
        else:
            self.lifter.setSpeed(0)


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
        self.driveLeft = self.driveController.getRawAxis(1) *self.mult
        self.driveRight = self.driveController.getRawAxis(5) *self.mult
        self.driveLeftHoriz = self.driveController.getRawAxis(0)  *self.mult
        self.driveRightHoriz = self.driveController.getRawAxis(4) *self.mult
        self.mechA = self.mechController.getAButton()


if __name__ == '__main__':
    wpilib.run(MyRobot)
