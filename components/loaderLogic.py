from robotMap import XboxMap
from components.shooterMotors import ShooterMotorCreation, Direction
from components.breakSensors import Sensors, SensorKey
from magicbot import StateMachine, state, timed_state, tunable
from networktables import NetworkTables
import logging

class LoaderLogic(StateMachine):
    """StateMachine-based loader. Has both automatic and manual modes."""
    compatString = ["doof"]

    # Component/module related things
    shooterMotors: ShooterMotorCreation
    logger: logging
    sensors: Sensors
    xboxMap: XboxMap

    # Tunable
    loaderMotorSpeed = tunable(.4)
    intakeMotorMinSpeed = tunable(.5)
    intakeMotorMaxSpeed = tunable(.7)

    def on_enable(self):
        self.isAutomatic = False

    def setAutoLoading(self):
        """Runs sensor-based loading."""
        self.isAutomatic = True
        self.next_state('checkForBall')

    def setManualLoading(self):
        """Runs trigger-based loading."""
        self.isAutomatic = False
        self.next_state('runLoaderManually')

    def runIntake(self):
        """Universal function for running the intake. Used in both manual and automatic."""
        if self.xboxMap.getMechRightTrig() > 0 and self.xboxMap.getMechLeftTrig() == 0:
            self.shooterMotors.runIntake((self.xboxMap.getMechRightTrig()*(self.intakeMotorMaxSpeed-self.intakeMotorMinSpeed))+self.intakeMotorMinSpeed, Direction.kForwards)
            self.logger.debug("right trig intake", self.xboxMap.getMechRightTrig())

        elif self.xboxMap.getMechLeftTrig() > 0 and self.xboxMap.getMechRightTrig() == 0:
            self.shooterMotors.runIntake((self.xboxMap.getMechRightTrig()*(self.intakeMotorMaxSpeed-self.intakeMotorMinSpeed))+self.intakeMotorMinSpeed, Direction.kBackwards)
            self.logger.debug("left trig intake", self.xboxMap.getMechLeftTrig())

        else:
            self.shooterMotors.stopIntake()

    @state(first = True)
    def runLoaderManually(self):
        """Trigger-based manual loader."""
        self.shooterMotors.stopShooter()
        if self.xboxMap.getMechRightTrig() > 0 and self.xboxMap.getMechLeftTrig() == 0:
            self.shooterMotors.runLoader(self.loaderMotorSpeed, Direction.kForwards)
            self.logger.debug("right trig manual", self.xboxMap.getMechRightTrig())

        elif self.xboxMap.getMechLeftTrig() > 0 and self.xboxMap.getMechRightTrig() == 0:
            self.shooterMotors.runLoader(self.loaderMotorSpeed, Direction.kBackwards)
            self.logger.debug("left trig manual", self.xboxMap.getMechLeftTrig())

        else:
            self.shooterMotors.stopLoader()

    @state
    def checkForBall(self):
        """Checks for ball to enter the loader, runs the loader if entry sensor is broken."""
        self.shooterMotors.stopLoader()
        if not self.sensors[SensorKey.kLoadingSensor].get():
            self.next_state('loadBall')

    @state
    def loadBall(self):
        """Loads ball if ball has entered."""
        self.shooterMotors.runLoader(self.loaderMotorSpeed, Direction.kForwards)
        self.next_state('waitForBallIntake')

    @state
    def waitForBallIntake(self):
        """Checks for intake to be completed."""
        if self.sensors[SensorKey.kLoadingSensor]:
            self.next_state('stopBall')

    @timed_state(duration = .2, next_state = 'checkForBall')
    def stopBall(self):
        """Stops ball after a short delay."""
        pass

    def updateNetworkTables(self):
        table = NetworkTables.getTable('LoaderType')
        if self.isAutomatic:
            table.putString('type', 'automatic')
        else:
            table.putString('type', 'manual')

    def execute(self):
        """Constantly runs state machine. Necessary for function."""
        self.engage()
        self.runIntake()
        self.updateNetworkTables()
        super().execute()
