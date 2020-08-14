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
from components.breakSensors import Sensors
from components.winch import Winch
from components.shooterMotors import ShooterMotorCreation
from components.shooterLogic import ShooterLogic
from components.loaderLogic import LoaderLogic
from components.elevator import Elevator
from components.scorpionLoader import ScorpionLoader
from components.feederMap import FeederMap

###EMH - Adding Autoaim
from components.autoAim import AutoAim
###EMH - End Adding Autoaim
# Other imports:
from robotMap import RobotMap, XboxMap
from utils.componentUtils import testComponentCompatibility
from utils.motorHelper import createMotor
from utils.sensorFactories import gyroFactory, breaksensorFactory
from utils.acturatorFactories import compressorFactory, solenoidFactory
import utils.math

class MyRobot(MagicRobot):
    """
    Base robot class of Magic Bot Type
    """
    shooter: ShooterLogic
    loader: LoaderLogic
    feeder: FeederMap
    sensors: Sensors
    shooterMotors: ShooterMotorCreation
    driveTrain: DriveTrain
    winch: Winch
    buttonManager: ButtonManager
    pneumatics: Pneumatics
    elevator: Elevator
    scorpionLoader: ScorpionLoader
    sensitivityExponent = tunable(1.8)
    ###EMH - Adding AutoAim
    autoAim: AutoAim
    ###EMH - End Adding AutoAim

    def createObjects(self):
        """
        Robot-wide initialization code should go here. Replaces robotInit
        """
        self.map = RobotMap()
        self.xboxMap = XboxMap(XboxController(1), XboxController(0))

        self.instantiateSubsystemGroup("motors", createMotor)
        self.instantiateSubsystemGroup("gyros", gyroFactory)
        self.instantiateSubsystemGroup("digitalInput", breaksensorFactory)
        self.instantiateSubsystemGroup("compressors", compressorFactory)
        self.instantiateSubsystemGroup("solenoids", solenoidFactory)

        # Check each componet for compatibility
        testComponentCompatibility(self, ShooterLogic)
        testComponentCompatibility(self, ShooterMotorCreation)
        testComponentCompatibility(self, DriveTrain)
        testComponentCompatibility(self, Winch)
        testComponentCompatibility(self, ButtonManager)
        testComponentCompatibility(self, Pneumatics)
        testComponentCompatibility(self, Elevator)
        testComponentCompatibility(self, ScorpionLoader)

    def autonomousInit(self):
        """Run when autonomous is enabled."""
        self.shooter.autonomousEnabled()
        self.loader.stopLoading()

    def teleopInit(self):
        # Register button events for doof
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kX, ButtonEvent.kOnPress, self.pneumatics.toggleLoader)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kY, ButtonEvent.kOnPress, self.loader.setAutoLoading)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kB, ButtonEvent.kOnPress, self.loader.setManualLoading)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kA, ButtonEvent.kOnPress, self.shooter.shootBalls)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kA, ButtonEvent.kOnPress, self.loader.stopLoading)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kA, ButtonEvent.kOnRelease, self.shooter.doneShooting)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kA, ButtonEvent.kOnRelease, self.loader.determineNextAction)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kBumperRight, ButtonEvent.kOnPress, self.elevator.setRaise)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kBumperRight, ButtonEvent.kOnRelease, self.elevator.stop)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kBumperLeft, ButtonEvent.kOnPress, self.elevator.setLower)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kBumperLeft, ButtonEvent.kOnRelease, self.elevator.stop)
        self.buttonManager.registerButtonEvent(self.xboxMap.drive, XboxController.Button.kBumperLeft, ButtonEvent.kOnPress, self.driveTrain.enableCreeperMode)
        self.buttonManager.registerButtonEvent(self.xboxMap.drive, XboxController.Button.kBumperLeft, ButtonEvent.kOnRelease, self.driveTrain.disableCreeperMode)
        ###EMH - Adding autoaim
        self.buttonManager.registerButtonEvent(self.xboxMap.drive, XboxController.Button.kA, ButtonEvent.kOnPress, self.autoAim.start)
        ###EMH - End Adding autoaim

        self.shooter.autonomousDisabled()

    def teleopPeriodic(self):
        """
        Must include. Called running teleop.
        """
        self.xboxMap.controllerInput()



        driveLeft = utils.math.expScale(self.xboxMap.getDriveLeft(), self.sensitivityExponent) * self.driveTrain.driveMotorsMultiplier
        driveRight = utils.math.expScale(self.xboxMap.getDriveRight(), self.sensitivityExponent) * self.driveTrain.driveMotorsMultiplier

        self.driveTrain.setTank(driveLeft, driveRight)

        if self.xboxMap.getMechDPad() == 0:
            self.winch.setRaise()
        else:
            self.winch.stop()

        self.scorpionLoader.checkController()

    def testInit(self):
        """
        Function called when testInit is called.
        """
        print("testInit was Successful")

    def testPeriodic(self):
        """
        Called during test mode alot
        """
        pass

    def instantiateSubsystemGroup(self, groupName, factory):
        """
        For each subsystem find all groupNames and call factory.
        Each one is saved to groupName_subsystem and subsystem_groupName
        """
        config = self.map.configMapper
        containerName = "subsystem" + groupName[0].upper() + groupName[1:]
        
        if not hasattr(self, containerName):
            setattr(self, containerName, {})
            self.subsystemGyros = {}

        #note this is a dicontary refernce, so changes to it
        #are changes to self.<containerName>
        container = getattr(self, containerName)

        subsystems = config.getSubsystems()
        createdCount = 0
        for subsystem in subsystems:
            items = {key:factory(descp) for (key, descp) in config.getGroupDict(subsystem, groupName).items()}
            if(len(items) == 0):
                continue
            container[subsystem] = items
            createdCount += len(container[subsystem])
            groupName_subsystem = "_".join([groupName,subsystem])
            self.logger.info("Creating %s", groupName_subsystem)
            setattr(self, groupName_subsystem, container[subsystem])

        self.logger.info(f"Created {createdCount} items for {groupName} groups with `{factory.__name__}` into `{containerName}")


if __name__ == '__main__':
    wpilib.run(MyRobot)
