
"""
Team 3200 Robot base class
"""
from wpilib import XboxController
import wpilib
from magicbot import MagicRobot

from robotMap import RobotMap
from components.driveTrain import DriveTrain
# from components.shooterMotors import ShooterMotorCreation
from components.sensor import SensorClass
from components.loader import LoaderClass

dio = wpilib.DigitalInput

class MyRobot(MagicRobot):
    """
    Base robot class of Magic Bot Type
    """

    driveTrain: DriveTrain

    Sensors: SensorClass
    Loader: LoaderClass

    #driveTrain: DriveTrain
    # ShooterMotors: ShooterMotorCreation


    def createObjects(self):
        """
        Robot-wide initialization code should go here. Replaces robotInit
        """
        self.map = RobotMap()

        # Drive Train
        self.left = 0
        self.right = 0
        self.stick = XboxController(0)

        self.driveTrain_motorsList = dict(self.map.motorsMap.driveMotors)
        self.mult = 1 #Multiplier for values. Should not be over 1.

        # Shooter
        # self.shooter_MotorsList = dict(self.map.motorsMap.driveMotors)

        self.sensorObjects = dio
        # self.loaderlogicSensors = dio

    def teleopPeriodic(self):
        """
        Must include. Called running teleop.
        """
        self.controllerInput()

        self.driveTrain.setArcade(self.left, -self.leftHoriz)

    def testInit(self):
        """
        Function called when testInit is called. Crashes on 2nd call right now
        """
       
        print("testInit was Successful")

    def testPeriodic(self):
        """
        Called during test mode alot
        """
        # print("testPeriodic is called")
        self.Sensors.setCurrentSensorProperties()
        #self.Sensors.execute()

    def controllerInput(self):
        """
        Collects all controller values and puts them in an easily readable format
        """
        self.left = self.stick.getRawAxis(1) *self.mult
        self.right = self.stick.getRawAxis(5) *self.mult
        self.leftHoriz = self.stick.getRawAxis(0)  *self.mult
        self.rightHoriz = self.stick.getRawAxis(4) *self.mult


if __name__ == '__main__':
    wpilib.run(MyRobot)
