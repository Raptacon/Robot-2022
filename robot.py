
"""
Team 3200 Robot base class
"""
from wpilib import XboxController
from wpilib import DigitalInput as dio
import wpilib
from magicbot import MagicRobot
from robotMap import RobotMap, XboxMap
from components.driveTrain import DriveTrain
from components.lifter import Lifter
from components.towerMotors import ShooterMotorCreation
from components.sensor import sensors
from components.buttonManager import ButtonManager, ButtonEvent
from examples.buttonManagerCallback import exampleCallback, simpleCallback, crashCallback

class MyRobot(MagicRobot):
    """
    Base robot class of Magic Bot Type
    """

    Sensors: sensors

    driveTrain: DriveTrain
    lifter: Lifter

    ShooterMotors: ShooterMotorCreation

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

        self.sensorObjects = dio

    def teleopInit(self):
        """
        Controller map is here for now
        """
        self.buttonManager.registerButtonEvent(self.XboxMap.getDriveController(), XboxController.Button.kStart, ButtonEvent.kOnPress, self.driveTrain.stop)
        self.buttonManager.registerButtonEvent(self.XboxMap.getMechController(), XboxController.Button.kStart, ButtonEvent.kOnPress, self.driveTrain.stop)
        self.buttonManager.registerButtonEvent(self.XboxMap.getMechController(), XboxController.Button.kA, ButtonEvent.kOnPress, exampleCallback)

        self.mult = 1 #Multiplier for values. Should not be over 1.

    def teleopPeriodic(self):
        """
        Must include. Called running teleop.
        """
        self.XboxMap.controllerInput()
        self.driveTrain.setArcade(self.XboxMap.getDriveLeft() * self.mult, -self.XboxMap.getDriveRightHoriz() * self.mult)

        if self.mechA:
            self.lifter.setSpeed(1)
        else:
            self.lifter.setSpeed(0)

        self.driveTrain.setArcade(self.left, -self.driveLeftHoriz)

        if self.shootExec:
            self.Sensors.fireShooter()
            print("Shooting:", self.shootExec)

        if self.RunIntake > 0:
            self.ShooterMotors.runIntake(self.RunIntake)
            print("Intake running:", self.RunIntake)
        else:
            self.ShooterMotors.runIntake(0)

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
      
    def controllerInput(self):
        """
        Collects all controller values and puts them in an easily readable format
        """
        self.driveLeft = self.driveController.getRawAxis(1) *self.mult
        self.driveRight = self.driveController.getRawAxis(5) *self.mult
        self.driveLeftHoriz = self.driveController.getRawAxis(0)  *self.mult
        self.driveRightHoriz = self.driveController.getRawAxis(4) *self.mult
        self.shootExec = self.driveController.getRawButton(self.driveController.Button.kBumperRight)
        self.RunIntake = self.driveController.getRawAxis(self.driveController.Axis.kRightTrigger)
        self.mechA = self.mechController.getAButton()

if __name__ == '__main__':
    wpilib.run(MyRobot)
