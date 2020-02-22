"""
Team 3200 Robot base class
"""
# Module imports:
import wpilib
from wpilib import XboxController
from magicbot import MagicRobot, tunable

# Component imports:
from components.driveTrain import DriveTrain
from components.pneumatics import Pneumatics
from components.buttonManager import ButtonManager, ButtonEvent
from components.lifter import Lifter
from components.ShooterMotors import ShooterMotorCreation
from components.ShooterLogic import ManualShooter, AutomaticShooter
from components.elevator import Elevator

# Other imports:
from robotMap import RobotMap, XboxMap

class MyRobot(MagicRobot):
    """
    Base robot class of Magic Bot Type
    """
    shootManual: ManualShooter
    shootAutomatic: AutomaticShooter
    shooterMotors: ShooterMotorCreation
    driveTrain: DriveTrain
    lifter: Lifter
    buttonManager: ButtonManager
    pneumatics: Pneumatics
    driveMutli = tunable(.5)
    elevator: Elevator

    def createObjects(self):
        """
        Robot-wide initialization code should go here. Replaces robotInit
        """
        self.map = RobotMap()
        self.xboxMap = XboxMap(XboxController(0), XboxController(1))
        self.motorsList = dict(self.map.motorsMap.driveMotors)
        self.auto = False

    def teleopInit(self):
        #register button events
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kX, ButtonEvent.kOnPress, self.pneumatics.toggleSolenoid)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kY, ButtonEvent.kOnPress, self.autoSwitch)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kA, ButtonEvent.kOnPress, self.shootAutomatic.switchToReverse)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kA, ButtonEvent.kOnPress, self.shootManual.fireShooter)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kA, ButtonEvent.kOnRelease, self.shootManual.shooterMotors.stopShooter)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kBumperRight, ButtonEvent.kOnPress, self.elevator.setRaise())
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kBumperRight, ButtonEvent.kOnRelease, self.elevator.stop())

    def teleopPeriodic(self):
        """
        Must include. Called running teleop.
        """
        self.xboxMap.controllerInput()
        
        self.driveTrain.setArcade(self.xboxMap.getDriveLeft() * self.driveMutli, self.xboxMap.getDriveRightHoriz() * self.driveMutli)

        if self.auto:
            self.autoRun()
        else:
            self.manualRun()

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

    def autoSwitch(self):
        if self.auto:
            self.auto = False
        else:
            self.auto = True

    def autoRun(self):
        if not self.shootManual.getAutomaticStatus():
            self.shootManual.stopManual()
            self.shootAutomatic.runLoaderAutomatically()
    
    def manualRun(self):
        if self.shootManual.getAutomaticStatus():
            self.shootAutomatic.stopAutomatic()
            self.shootManual.runLoaderManually()

if __name__ == '__main__':
    wpilib.run(MyRobot)
