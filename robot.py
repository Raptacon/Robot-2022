
"""
Team 3200 Robot base class
"""
from wpilib import XboxController
import wpilib
from magicbot import MagicRobot
from robotMap import RobotMap
from components.driveTrain import DriveTrain
from components.shooterMotors import ShooterMotorClass


class MyRobot(MagicRobot):
    """
    Base robot class of Magic Bot Type
    """

    driveTrain: DriveTrain
    ShooterMotors: ShooterMotorClass

    def createObjects(self):
        """
        Robot-wide initialization code should go here. Replaces robotInit
        """
        # Drive Train
        self.map = RobotMap()
        self.left = 0
        self.right = 0
        self.stick = XboxController(0)
        self.driveTrain_motorsList = dict(self.map.motorsMap.driveMotors)

        # Shooter
        self.shooter_MotorsList = dict(self.map.motorsMap.driveMotors)

        self.loaderMotor = 0
        self.shooterMotor = 0
        self.intakeMotor = 0

        self.entrySensor = wpilib.DigitalInput(0)
        self.exitSensor = wpilib.DigitalInput(5)

        self.sensor1 = wpilib.DigitalInput(1) # Array: 0
        self.sensor2 = wpilib.DigitalInput(2) # Array: 1
        self.sensor3 = wpilib.DigitalInput(3) # Array: 2
        self.sensor4 = wpilib.DigitalInput(4) # Array: 3

    def teleopPeriodic(self):
        """
        Must include. Called running teleop.
        """
        self.controllerInput()
        self.driveTrain.setArcade(self.left / 2, -self.rightHoriz / 2)

        if self.controller.getTriggerAxis(1):
            self.ShooterMotors.setLoaderSpeed(self.controller.getTriggerAxis(1))

        print(self.ShooterMotors.getLoaderMotor())

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
