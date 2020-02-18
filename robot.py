
"""
Team 3200 Robot base class
"""
from wpilib import XboxController
from wpilib import DigitalInput as dio
import wpilib
from magicbot import MagicRobot
from robotMap import RobotMap

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

    SensorShooter: sensors

    # Comment out if needed
    # ManualShooter: ManualControl

    driveTrain: DriveTrain
    lifter: Lifter

    Motors: ShooterMotorCreation

    buttonManager: ButtonManager

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
        
        # Drive Train

        self.sensorObjects = dio
        # self.sensor = dio(0)

    def teleopInit(self):
        #register button events
        self.createObjects()
        self.mult = .5 #Multiplier for values. Should not be over 1.

    def teleopPeriodic(self):
        """
        Must include. Called running teleop.
        """
        self.XboxMap.controllerInput()
        self.driveTrain.setArcade(self.XboxMap.getDriveLeft() * self.mult, -self.XboxMap.getDriveRightHoriz() * self.mult)
        self.ShooterMotors.runIntake(self.XboxMap.getMechRightTrig())

        # Comment out if needed
        """
        self.ManualShooter.RunLoader(self.XboxMap.getDriveRightTrig())
        self.ManualShooter.reverseLoader(self.XboxMap.getDriveLeftTrig())
        self.ManualShooter.runShooter(self.XboxMap.getDriveRightBump())
        """

        if self.XboxMap.getMechAButton():
            self.SensorShooter.fireShooter()
        # print(self.sensor.get())

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
        self.driveA = self.driveController.getAButton()
        self.driveB = self.driveController.getBButton()

if __name__ == '__main__':
    wpilib.run(MyRobot)
