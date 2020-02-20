# Module imports:
import wpilib
from wpilib import XboxController
from wpilib import DigitalInput as dio
from magicbot import MagicRobot
# Component imports:
from components.driveTrain import DriveTrain
from components.lifter import Lifter
from components.towerMotors import ShooterMotorCreation
from components.sensor import sensors, ManualControl
from components.buttonManager import ButtonManager, ButtonEvent

# Other imports:
from robotMap import RobotMap, XboxMap
from examples.buttonManagerCallback import exampleCallback, simpleCallback, crashCallback

class MyRobot(MagicRobot):
    """
    Base robot class of Magic Bot Type
    """
    ShooterSensors: ShooterLogic
    ShooterMotors: ShooterMotorCreation
    driveTrain: DriveTrain
    lifter: Lifter
    buttonManager: ButtonManager

    def createObjects(self):
        """
        Robot-wide initialization code should go here. Replaces robotInit
        """
        self.map = RobotMap()
        self.XboxMap = XboxMap(XboxController(0), XboxController(1))
        self.motorsList = dict(self.map.motorsMap.driveMotors)

        self.sensorObjects = dio

    def teleopInit(self):
        self.mult = .5 #Multiplier for values. Should not be over 1.

    def teleopPeriodic(self):
        """
        Must include. Called running teleop.
        """
        self.XboxMap.controllerInput()
        
        self.driveTrain.setArcade(self.XboxMap.getDriveLeft() * self.mult, -self.XboxMap.getDriveRightHoriz() * self.mult)

        # Enables automatic control
        if self.XboxMap.getMechYButton():
            self.ShooterSensors.runLoaderAutomatically()
            if self.XboxMap.getMechAButton():
                self.ShooterSensors.fireShooter()
        # Enables manual control
        else:
            self.ShooterSensors.runLoaderManually()

        #TODO: Look at drive station for proper button syntax

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
