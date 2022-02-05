"""
Team 3200 Robot base class
"""
# Module imports:
import wpilib
from wpilib import XboxController
from wpilib import SerialPort
from magicbot import MagicRobot, tunable

# Component imports:
from components.driveTrain import DriveTrain
from components.pneumatics import Pneumatics
from components.buttonManager import ButtonManager, ButtonEvent
from components.breakSensors import Sensors
from components.winch import Winch
from components.shooterMotors import ShooterMotors
from components.hopperMotor import HopperMotor
from components.intakeMotor import IntakeMotor
from components.shooterLogic import ShooterLogic
from components.loaderLogic import LoaderLogic
from components.elevator import Elevator
from components.scorpionLoader import ScorpionLoader
from components.feederMap import FeederMap
from components.autoAlign import AutoAlign
from components.autoShoot import AutoShoot
from components.lidar import Lidar
from components.navx import Navx
from components.turnToAngle import TurnToAngle
from components.driveTrainGoToDist import GoToDist
from components.ballCounter import BallCounter
from components.colorSensor import ColorSensor

# Other imports:
from robotMap import RobotMap, XboxMap
from networktables import NetworkTables
from utils.componentUtils import testComponentListCompatibility
from utils.motorHelper import createMotor
from utils.sensorFactories import gyroFactory, breaksensorFactory
from utils.acturatorFactories import compressorFactory, solenoidFactory
import utils.math

# Test imports:
from components.testBoard import TestBoard


class MyRobot(MagicRobot):
    """
    Base robot class of Magic Bot Type
    """
    shooter: ShooterLogic
    loader: LoaderLogic
    feeder: FeederMap
    sensors: Sensors
    shooterMotors: ShooterMotors
    intakeMotor: IntakeMotor
    hopperMotor: HopperMotor
    driveTrain: DriveTrain
    winch: Winch
    buttonManager: ButtonManager
    pneumatics: Pneumatics
    elevator: Elevator
    scorpionLoader: ScorpionLoader
    autoAlign: AutoAlign
    autoShoot: AutoShoot
    navx: Navx
    turnToAngle: TurnToAngle
    lidar: Lidar
    goToDist: GoToDist
    ballCounter: BallCounter
    colorSensor: ColorSensor

    # Test code:
    testBoard: TestBoard

    sensitivityExponent = tunable(1.8)
    arcadeMode = tunable(True)

    def createObjects(self):
        """
        Robot-wide initialization code should go here. Replaces robotInit
        """
        self.map = RobotMap()
        self.xboxMap = XboxMap(XboxController(1), XboxController(0))

        ReadBufferValue = 18

        self.MXPserial = SerialPort(115200, SerialPort.Port.kMXP, 8,
        SerialPort.Parity.kParity_None, SerialPort.StopBits.kStopBits_One)
        self.MXPserial.setReadBufferSize(ReadBufferValue)
        self.MXPserial.setWriteBufferSize(2 * ReadBufferValue)
        self.MXPserial.setWriteBufferMode(SerialPort.WriteBufferMode.kFlushOnAccess)
        self.MXPserial.setTimeout(.1)

        self.smartDashboardTable = NetworkTables.getTable('SmartDashboard')

        self.instantiateSubsystemGroup("motors", createMotor)
        self.instantiateSubsystemGroup("gyros", gyroFactory)
        self.instantiateSubsystemGroup("digitalInput", breaksensorFactory)
        self.instantiateSubsystemGroup("compressors", compressorFactory)
        self.instantiateSubsystemGroup("solenoids", solenoidFactory)

        # Check each component for compatibility
        componentList = [GoToDist, Winch, ShooterLogic, ShooterMotors, DriveTrain,
                         ButtonManager, Pneumatics, Elevator, ScorpionLoader, TurnToAngle,
                         AutoAlign, TestBoard, AutoShoot, FeederMap, Lidar, Sensors,
                         LoaderLogic, BallCounter, ColorSensor, HopperMotor, IntakeMotor]
        testComponentListCompatibility(self, componentList)


    def autonomousInit(self):
        """Run when autonomous is enabled."""
        self.shooter.autonomousEnabled()
        self.loader.stopLoading()


    def teleopInit(self):
        # Register button events for doof
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kX, ButtonEvent.kOnPress, self.pneumatics.toggleLoader)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kY, ButtonEvent.kOnPress, self.loader.setAutoLoading)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kB, ButtonEvent.kOnPress, self.loader.setManualLoading)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kA, ButtonEvent.kOnPress, self.shooter.startShooting)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kA, ButtonEvent.kOnPress, self.loader.stopLoading)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kA, ButtonEvent.kOnRelease, self.shooter.doneShooting)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kA, ButtonEvent.kOnRelease, self.loader.determineNextAction)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kRightBumper, ButtonEvent.kOnPress, self.elevator.setRaise)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kRightBumper, ButtonEvent.kOnRelease, self.elevator.stop)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kLeftBumper, ButtonEvent.kOnPress, self.elevator.setLower)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kLeftBumper, ButtonEvent.kOnRelease, self.elevator.stop)
        self.buttonManager.registerButtonEvent(self.xboxMap.drive, XboxController.Button.kLeftBumper, ButtonEvent.kOnPress, self.driveTrain.enableCreeperMode)
        self.buttonManager.registerButtonEvent(self.xboxMap.drive, XboxController.Button.kA, ButtonEvent.kOnPress, self.loader.stopLoading)
        self.buttonManager.registerButtonEvent(self.xboxMap.drive, XboxController.Button.kA, ButtonEvent.kOnRelease, self.shooter.doneShooting)
        self.buttonManager.registerButtonEvent(self.xboxMap.drive, XboxController.Button.kA, ButtonEvent.kOnRelease, self.loader.determineNextAction)
        self.buttonManager.registerButtonEvent(self.xboxMap.drive, XboxController.Button.kA, ButtonEvent.kOnRelease, self.autoShoot.stop)
        self.buttonManager.registerButtonEvent(self.xboxMap.drive, XboxController.Button.kLeftBumper, ButtonEvent.kOnRelease, self.driveTrain.disableCreeperMode)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kRightBumper, ButtonEvent.kOnPress, self.navx.reset)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kLeftBumper, ButtonEvent.kOnPress, self.goToDist.start)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kLeftBumper, ButtonEvent.kOnRelease, self.goToDist.stop)


        self.driveTrain.setBraking(True)
        self.driveTrain.resetDistTraveled()

        self.shooter.autonomousDisabled()
        self.prevAState = False

        self.turnToAngle.engage()

    def teleopPeriodic(self):
        """
        Must include. Called repeatedly while running teleop.
        """
        self.xboxMap.controllerInput()

        #This variable determines whether to use controller input for the drivetrain or not.
        #If we are using a command (such as auto align) that uses the drivetrain, we don't want to use the controller's input because it would overwrite
        #what the component is doing.
        executingDriveCommand = False

        driveLeftY = utils.math.expScale(self.xboxMap.getDriveLeft(), self.sensitivityExponent) * self.driveTrain.driveMotorsMultiplier
        driveRightY = utils.math.expScale(self.xboxMap.getDriveRight(), self.sensitivityExponent) * self.driveTrain.driveMotorsMultiplier
        # unused for now # driveLeftX = utils.math.expScale(self.xboxMap.getDriveLeftHoriz(), self.sensitivityExponent) * self.driveTrain.driveMotorsMultiplier
        driveRightX = utils.math.expScale(self.xboxMap.getDriveRightHoriz(), self.sensitivityExponent) * self.driveTrain.driveMotorsMultiplier

        self.goToDist.engage()
        self.autoShoot.engage()
        self.turnToAngle.engage()
        if self.xboxMap.getDriveA() == True:
            executingDriveCommand = True
            self.autoAlign.setShootAfterComplete(False)
            self.autoAlign.engage()
        if self.xboxMap.getDriveA() == False and self.prevAState == True:
            self.autoAlign.stop()
            self.autoShoot.stop()
            self.shooterMotors.stopShooter()
            self.hopperMotor.stopHopper()
        self.prevAState = self.xboxMap.getDriveA()

        if not executingDriveCommand:
            if self.arcadeMode:
                self.driveTrain.setArcade(-1 *driveLeftY, driveRightX)
            else:
                self.driveTrain.setTank(driveLeftY, driveRightY)
            self.autoAlign.reset_integral()

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

        # note this is a dictionary reference, so changes to it
        # are changes to self.<containerName>
        container = getattr(self, containerName)

        subsystems = config.getSubsystems()
        createdCount = 0
        for subsystem in subsystems:
            items = {key: factory(descp) for (key, descp) in config.getGroupDict(subsystem, groupName).items()}
            if(len(items) == 0):
                continue
            container[subsystem] = items
            createdCount += len(container[subsystem])
            groupName_subsystem = "_".join([groupName,subsystem])
            self.logger.info("Creating %s", groupName_subsystem)
            setattr(self, groupName_subsystem, container[subsystem])

        self.logger.info(f"Created {createdCount} items for {groupName} groups with `{factory.__name__}` into `{containerName}")

    def disabledInit(self):
        """
        What the robot runs on disabled start
        NEVER RUN ANYTHING THAT MOVES ANYTHING HERE
        """
        self.driveTrain.setBraking(False)

    def disabledPeriodic(self):
        """
        Runs repeatedly while disabled
        NEVER RUN ANYTHING THAT MOVES ANYTHING HERE
        """
        pass

if __name__ == '__main__':
    wpilib.run(MyRobot)
