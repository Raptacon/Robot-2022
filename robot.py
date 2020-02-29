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
from components.ShooterLogic import ShooterLogic
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
    shooter: ShooterLogic
    shooterMotors: ShooterMotorCreation
    driveTrain: DriveTrain
    lifter: Lifter
    buttonManager: ButtonManager
    pneumatics: Pneumatics
    elevator: Elevator
    scorpionLoader: ScorpionLoader
    
    

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
        testComponentCompatibility(self, ShooterLogic)
        testComponentCompatibility(self, ShooterMotorCreation)
        testComponentCompatibility(self, DriveTrain)
        testComponentCompatibility(self, Lifter)
        testComponentCompatibility(self, ButtonManager)
        testComponentCompatibility(self, Pneumatics)
        testComponentCompatibility(self, Elevator)
        testComponentCompatibility(self, ScorpionLoader)

    def teleopInit(self):
        #register button events for doof
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kX, ButtonEvent.kOnPress, self.pneumatics.toggleSolenoid)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kY, ButtonEvent.kOnPress, self.shooter.initAutomatic)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kB, ButtonEvent.kOnPress, self.shooter.initManual)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kA, ButtonEvent.kWhilePressed, self.shooter.fireManualShooter)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kA, ButtonEvent.kOnRelease, self.shooterMotors.stopShooter)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kA, ButtonEvent.kOnPress, self.shooter.fireAutomaticShooter)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kBumperRight, ButtonEvent.kOnPress, self.elevator.setRaise)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kBumperRight, ButtonEvent.kOnRelease, self.elevator.stop)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kBumperLeft, ButtonEvent.kOnPress, self.elevator.setLower)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kBumperLeft, ButtonEvent.kOnRelease, self.elevator.stop)
        self.buttonManager.registerButtonEvent(self.xboxMap.drive, XboxController.Button.kBumperLeft, ButtonEvent.kOnPress, self.driveTrain.creeperMode)
        self.buttonManager.registerButtonEvent(self.xboxMap.drive, XboxController.Button.kBumperLeft, ButtonEvent.kOnRelease, self.driveTrain.disableCreeperMode)

    def teleopPeriodic(self):
        """
        Must include. Called running teleop.
        """
        self.xboxMap.controllerInput()

        self.driveTrain.setArcade(self.xboxMap.getDriveLeft() * self.driveTrain.driveMotorsMultiplier, self.xboxMap.getDriveRightHoriz() * self.driveTrain.driveMotorsMultiplier)

        # Runs manual if self.isAutomatic == False
        self.shooter.startManual()

        # Runs automatic if self.isAutomaic == True
        self.shooter.startAutomatic()

        # Calls intake buttons for automatic
        self.shooter.runIntakeAutomatically()

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
