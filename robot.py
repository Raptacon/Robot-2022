# Module imports:
import wpilib
from wpilib import XboxController
from wpilib import DigitalInput as dio
from magicbot import MagicRobot
# Component imports:
from components.driveTrain import DriveTrain
from components.lifter import Lifter
from components.ShooterMotors import ShooterMotorCreation
from components.ShooterLogic import shooterLogic
from components.buttonManager import ButtonManager, ButtonEvent

# Other imports:
from robotMap import RobotMap, XboxMap
from examples.buttonManagerCallback import exampleCallback, simpleCallback, crashCallback

class MyRobot(MagicRobot):
    """
    Base robot class of Magic Bot Type
    """
    ShooterController: shooterLogic
    ShooterMotors: ShooterMotorCreation
    driveTrain: DriveTrain
    lifter: Lifter
    buttonManager: ButtonManager

    def createObjects(self):
        """
        Robot-wide initialization code should go here. Replaces robotInit
        """
        self.map = RobotMap()
        self.xboxMap = XboxMap(XboxController(0), XboxController(1))
        self.motorsList = dict(self.map.motorsMap.driveMotors)

        self.sensorObjects = dio

    def teleopInit(self):
        self.mult = .5 #Multiplier for values. Should not be over 1.

    def teleopPeriodic(self):
        """
        Must include. Called running teleop.
        """
        self.xboxMap.controllerInput()
        
        self.driveTrain.setArcade(self.xboxMap.getDriveLeft() * self.mult, self.xboxMap.getDriveRightHoriz() * self.mult)

        # Enables automatic control
        if self.xboxMap.getMechYButton():
            self.ShooterController.runLoaderAutomatically()
        # Enables manual control
        else:
            self.ShooterController.runLoaderManually()
            if self.xboxMap.getMechAButton():
                print("FIRE SHOOTER")
                self.ShooterController.fireShooter()
            else:
                self.ShooterController.ShooterMotors.stopShooter()
                self.ShooterController.ShooterMotors.stopLoader()

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
