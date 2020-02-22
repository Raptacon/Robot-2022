"""
Team 3200 Robot base class
"""
# Module imports:
import wpilib
from wpilib import XboxController
from wpilib import DigitalInput as dio
from magicbot import MagicRobot

# Component imports:
from components.driveTrain import DriveTrain
from components.pneumatics import Pneumatics
from components.buttonManager import ButtonManager, ButtonEvent
from examples.buttonManagerCallback import actionCallback, crashCallback, exampleCallback, simpleCallback
from components.lifter import Lifter
from components.ShooterMotors import ShooterMotorCreation
from components.ShooterLogic import ManualShooter, AutomaticShooter

# Other imports:
from robotMap import RobotMap, XboxMap

class MyRobot(MagicRobot):
    """
    Base robot class of Magic Bot Type
    """
    shootManual: ManualShooter
    shootAutomatic: AutomaticShooter
    ShooterMotors: ShooterMotorCreation
    driveTrain: DriveTrain
    lifter: Lifter
    buttonManager: ButtonManager
    pneumatics: Pneumatics

    def createObjects(self):
        """
        Robot-wide initialization code should go here. Replaces robotInit
        """
        # Motors/controllers:
        self.map = RobotMap()
        self.xboxMap = XboxMap(XboxController(0), XboxController(1))
        self.motorsList = dict(self.map.motorsMap.driveMotors)
        # Sensor object
        self.sensorObjects = dio

    def teleopInit(self):
        #register button events
        self.buttonManager.registerButtonEvent(self.stick, XboxController.Button.kA, ButtonEvent.kOnPress, exampleCallback)
        self.buttonManager.registerButtonEvent(self.stick, XboxController.Button.kBack, ButtonEvent.kOnPress | ButtonEvent.kOnRelease, crashCallback)
        self.buttonManager.registerButtonEvent(self.stick, XboxController.Button.kStart,  ButtonEvent.kWhilePressed, simpleCallback)
        self.buttonManager.registerButtonEvent(self.stick, XboxController.Button.kY,  ButtonEvent.kOnPress, actionCallback)
        self.buttonManager.registerButtonEvent(self.stick, XboxController.Button.kX, ButtonEvent.kOnPress, self.pneumatics.enableSolenoid)
        self.buttonManager.registerButtonEvent(self.stick, XboxController.Button.kX, ButtonEvent.kOnRelease, self.pneumatics.disableSolenoid)
        self.mult = .5 # Multiplier for drive values. Should not be over 1.

    def teleopPeriodic(self):
        """
        Must include. Called running teleop.
        """
        self.xboxMap.controllerInput()
        
        self.driveTrain.setArcade(self.xboxMap.getDriveLeft() * self.mult, self.xboxMap.getDriveRightHoriz() * self.mult)

        # Enables automatic control (Toggle)
        if self.xboxMap.getMechYButton() and not self.shootManual.getAutomaticStatus():
            self.shootManual.stopManual()
            self.shootAutomatic.runLoaderAutomatically()

        # Enables manual control (Toggle)
        elif self.xboxMap.getMechYButton() and self.shootAutomatic.getAutomaticStatus():
            self.shootAutomatic.stopAutomatic()
            self.shootManual.runLoaderManually()

        # Needs to run periodically (calls self.engage if automatic enabled)
        self.shootAutomatic.initAutoLoading()

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
