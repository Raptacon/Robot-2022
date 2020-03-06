from robotMap import XboxMap
from components.shooterMotors import ShooterMotorCreation, Direction
from components.breakSensors import Sensors, State
from magicbot import StateMachine, state, timed_state, tunable, feedback
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

    # Other variables
    isAutomatic = False

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

    @feedback
    def isRunningAutomatic(self):
        return self.isAutomatic

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
        if self.xboxMap.getMechRightTrig() > 0 and self.xboxMap.getMechLeftTrig() == 0:
            self.shooterMotors.runLoader(self.loaderMotorSpeed, Direction.kForwards)
            self.logger.debug("right trig manual", self.xboxMap.getMechRightTrig())

        elif self.xboxMap.getMechLeftTrig() > 0 and self.xboxMap.getMechRightTrig() == 0:
            self.shooterMotors.runLoader(self.loaderMotorSpeed, Direction.kBackwards)
            self.logger.debug("left trig manual", self.xboxMap.getMechLeftTrig())
            self.shooterMotors.runShooter(-1)

        else:
            self.shooterMotors.stopShooter()
            self.shooterMotors.stopLoader()

    @state
    def checkForBall(self):
        """Checks for ball to enter the loader, runs the loader if entry sensor is broken."""
        self.shooterMotors.stopLoader()
        if self.sensors.loadingSensor(State.kTripped):
            self.next_state('loadBall')

    @state
    def loadBall(self):
        """Loads ball if ball has entered."""
        self.shooterMotors.runLoader(self.loaderMotorSpeed, Direction.kForwards)
        self.next_state('waitForBallIntake')

    @state
    def waitForBallIntake(self):
        """Checks for intake to be completed."""
        if self.sensors.loadingSensor(State.kNotTripped):
            self.next_state('stopBall')

    @timed_state(duration = .13, next_state = 'checkForBall')
    def stopBall(self):
        """Stops ball after a short delay."""
        pass

    @state
    def shooting(self):
        """Prevent loading actions if shooter is running."""
        pass

    @state
    def nextAction(self):
        """Determine what to do after shooting."""
        if self.isAutomatic:
            self.next_state('checkForBall')
        elif not self.isAutomatic:
            self.next_state('runLoaderManually')

    def execute(self):
        """Constantly runs state machine. Necessary for function."""
        self.engage()
        self.runIntake()
        super().execute()
