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
from components.scorpionLoader import ScorpionLoader

# Other imports:
from robotMap import RobotMap, XboxMap
from utils.componentUtils import testComponentCompatibility
from utils.motorHelper import createMotor

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
    elevator: Elevator
    scorpionLoader: ScorpionLoader
    
    driveMotorsMutliplier = tunable(.5)

    def createObjects(self):
        """
        Robot-wide initialization code should go here. Replaces robotInit
        """
        self.map = RobotMap()
        self.xboxMap = XboxMap(XboxController(0), XboxController(1))

        #self.motorsList = dict(self.map.motorsMap.driveMotors)
        self.instantiateSubsystemsMotors()
        self.runShooterAutomatically = False


        #check each componet for compatibility
        testComponentCompatibility(self, ManualShooter)
        testComponentCompatibility(self, AutomaticShooter)
        testComponentCompatibility(self, ShooterMotorCreation)
        testComponentCompatibility(self, DriveTrain)
        testComponentCompatibility(self, Lifter)
        testComponentCompatibility(self, ButtonManager)
        testComponentCompatibility(self, Pneumatics)
        testComponentCompatibility(self, Elevator)
        

    def teleopInit(self):
        #register button events
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kX, ButtonEvent.kOnPress, self.pneumatics.toggleSolenoid)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kY, ButtonEvent.kOnPress, self.autoSwitch)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kA, ButtonEvent.kOnPress, self.shootAutomatic.initAutoShooting)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kA, ButtonEvent.kWhilePressed, self.shootManual.fireShooter)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kA, ButtonEvent.kOnRelease, self.shootManual.shooterMotors.stopShooter)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kBumperRight, ButtonEvent.kOnPress, self.elevator.setRaise)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kBumperRight, ButtonEvent.kOnRelease, self.elevator.stop)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kBumperLeft, ButtonEvent.kOnPress, self.elevator.setLower)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kBumperLeft, ButtonEvent.kOnRelease, self.elevator.stop)

    def teleopPeriodic(self):
        """
        Must include. Called running teleop.
        """
        self.xboxMap.controllerInput()
        
        self.driveTrain.setArcade(self.xboxMap.getDriveLeft() * self.driveMotorsMutliplier, self.xboxMap.getDriveRightHoriz() * self.driveMotorsMutliplier)

        if self.runShooterAutomatically:
            self.autoRun()
        else:
            self.manualRun()

        # Needs to run periodically (calls self.engage if automatic enabled)
        self.shootAutomatic.initAutoLoading()

        #Scoprion Code
        self.scorpionLoader.checkController()

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

    # Automatic loading toggle
    def autoSwitch(self):
        if self.runShooterAutomatically:
            self.runShooterAutomatically = False
        else:
            self.runShooterAutomatically = True

    def autoRun(self):
        if not self.shootManual.getAutomaticStatus():
            self.shootManual.stopManual()
            self.shootAutomatic.runLoaderAutomatically()
    
    def manualRun(self):
        if self.shootManual.getAutomaticStatus():
            self.shootAutomatic.stopAutomatic()
            self.shootManual.runLoaderManually()

    def instantiateSubsystemsMotors(self):
        """
        For each subsystem, find all motors and create them. Save them to the motors_subsystem variable and subsystemsMotor
        """
        config = self.map.configMapper
        
        if not hasattr(self, 'subsystemMotors'):
            self.subsystemMotors = {}

        subsystems = config.getSubsystems()

        for subsystem in subsystems:
            self.subsystemMotors[subsystem] = {key:createMotor(descp) for (key, descp) in config.getGroupDict(subsystem, "motors").items()}
            motors_subsystem = 'motors_'+subsystem
            self.logger.info("Creating %s", motors_subsystem)
            setattr(self, motors_subsystem, self.subsystemMotors[subsystem])


if __name__ == '__main__':
    wpilib.run(MyRobot)
