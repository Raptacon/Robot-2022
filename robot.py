
"""
Team 3200 Robot base class
"""
from wpilib import XboxController
import wpilib
from magicbot import MagicRobot

from robotMap import RobotMap, XboxMap
from components.driveTrain import DriveTrain
from components.buttonManager import ButtonManager, ButtonEvent
from examples.buttonManagerCallback import exampleCallback, simpleCallback, crashCallback

class MyRobot(MagicRobot):
    """
    Base robot class of Magic Bot Type
    """

    driveTrain: DriveTrain
    buttonManager: ButtonManager

    def createObjects(self):
        """
        Robot-wide initialization code should go here. Replaces robotInit
        """
        self.map = RobotMap()
        self.XboxMap = XboxMap(XboxController(0), XboxController(1))
        # Drive Train
        self.left = 0
        self.right = 0
        self.driveTrain_motorsList = dict(self.map.motorsMap.driveMotors)
        self.mult = 1 #Multiplier for values. Should not be over 1.

    def teleopInit(self):
        """
        Controller map is here for now
        """
        ButtonManager.registerButtonEvent(self.XboxMap.getDriveController(), XboxController.Button.kStart, ButtonEvent.kOnPress, self.DriveTrain.stop)
        ButtonManager.registerButtonEvent(self.XboxMap.getMechController(), XboxController.Button.kStart, ButtonEvent.kOnPress, self.DriveTrain.stop)

    def teleopPeriodic(self):
        """
        Must include. Called running teleop.
        """
        self.XboxMap.controllerInput()
        self.driveTrain.setArcade(self.XboxMap.getLeft() * self.mult, -self.XboxMap.getRightHorizontal() * self.mult)

    def testInit(self):
        """
        Function called when testInit is called. Crashes on 2nd call right now
        """
        print("testInit was Successful")

    def testPeriodic(self):
        """
        Called during test mode alot
        """
        pass


if __name__ == '__main__':
    wpilib.run(MyRobot)
