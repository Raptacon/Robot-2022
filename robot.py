# Module imports:
import wpilib
from wpilib import XboxController
from wpilib import DigitalInput as dio
from magicbot import MagicRobot

# Component imports:
from components.driveTrain import DriveTrain
from components.lifter import Lifter
from components.ShooterMotors import ShooterMotorCreation
from components.ShooterLogic import ManualShooter, AutomaticShooter
from components.buttonManager import ButtonManager, ButtonEvent

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

    def createObjects(self):
        """
        Robot-wide initialization code should go here. Replaces robotInit
        """
        # Motors/controllers:
        self.map = RobotMap()
        self.xboxMap = XboxMap(XboxController(0), XboxController(1))
        self.motorsList = dict(self.map.motorsMap.driveMotors)

        # Sensor object
        self.sensorObjects = 
        self.auto = False

    def teleopInit(self):
        self.mult = .5 # Multiplier for drive values. Should not be over 1.
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kY, ButtonEvent.kOnPress, self.autoSwitch)

    def teleopPeriodic(self):
        """
        Must include. Called running teleop.
        """
        self.xboxMap.controllerInput()
        
        self.driveTrain.setArcade(self.xboxMap.getDriveLeft() * self.mult, self.xboxMap.getDriveRightHoriz() * self.mult)

        # Enables automatic control (Toggle)
        

        # Enables manual control (Toggle)
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
        if self.xboxMap.getMechYButton():
            self.shootAutomatic.stopAutomatic()
            self.shootManual.runLoaderManually()

if __name__ == '__main__':
    wpilib.run(MyRobot)
