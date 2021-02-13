from robotMap import XboxMap
from components.shooterMotors import ShooterMotorCreation, Direction
from components.breakSensors import Sensors, State
from components.feederMap import FeederMap, Type
from magicbot import StateMachine, state, timed_state, tunable, feedback
import logging

class LoaderLogic(StateMachine):
    """StateMachine-based loader. Has both automatic and manual modes."""
    compatString = ["doof"]

    # Component/module related things
    shooterMotors: ShooterMotorCreation
    feeder: FeederMap
    logger: logging
    sensors: Sensors
    xboxMap: XboxMap

    # Tunable
    automaticLoaderSpeed = tunable(.4)

    # Other variables
    isAutomatic = True
    loaderStoppingDelay = .16

    def on_enable(self):
        self.isAutomatic = True

    def setAutoLoading(self):
        """Runs sensor-based loading."""
        self.isAutomatic = True
        self.next_state('checkForBall')

    def setManualLoading(self):
        """Runs trigger-based loading."""
        self.isAutomatic = False
        self.next_state('runLoaderManually')

    def stopLoading(self):
        if self.shooterMotors.isLoaderRunning():
            return
        self.next_state('shooting')

    def determineNextAction(self):
        self.next_state('nextAction')

    @feedback
    def isRunningAutomatic(self):
        return self.isAutomatic

    def runIntake(self):
        """Universal function for running the intake. Used in both manual and automatic."""
        self.feeder.run(Type.kIntake)

    @state
    def runLoaderManually(self):
        """Trigger-based manual loader."""
        self.feeder.run(Type.kLoader)

    @state(first = True)
    def checkForBall(self):
        """Checks for ball to enter the loader, runs the loader if entry sensor is broken."""
        self.shooterMotors.stopLoader()
        if self.sensors.loadingSensor(State.kTripped):
            self.next_state('loadBall')

    @state
    def loadBall(self):
        """Loads ball if ball has entered."""
        self.shooterMotors.runLoader(self.automaticLoaderSpeed, Direction.kForwards)
        self.next_state('waitForBallIntake')

    @state
    def waitForBallIntake(self):
        """Checks for intake to be completed."""
        if self.sensors.loadingSensor(State.kNotTripped):
            self.next_state('stopBall')

    @timed_state(duration = loaderStoppingDelay, next_state = 'checkForBall')
    def stopBall(self):
        """Stops ball after a short delay."""
        pass

    @state
    def shooting(self):
        """While shooting, do nothing with the loader."""
        pass

    @state
    def nextAction(self):
        """Determine what to do after shooting."""
        if self.isAutomatic:
            self.next_state('checkForBall')
        elif not self.isAutomatic:
            self.next_state('runLoaderManually')

    def execute(self):
        """Constantly runs state machine and intake. Necessary for function."""
        self.engage()
        self.runIntake()
        super().execute()
