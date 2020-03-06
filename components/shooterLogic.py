from robotMap import XboxMap
from components.shooterMotors import ShooterMotorCreation, Direction
from components.breakSensors import Sensors, SensorKey
from magicbot import StateMachine, state, timed_state, tunable
import logging

class ShooterLogic(StateMachine):
    """StateMachine-based shooter. Has both manual and automatic modes."""
    compatString = ["doof"]

    # Component/module related things
    shooterMotors: ShooterMotorCreation
    logger: logging
    sensors: Sensors
    xboxMap: XboxMap

    # Tunables
    loaderMotorSpeed = tunable(.4)
    intakeMotorMinSpeed = tunable(.5)
    intakeMotorMaxSpeed = tunable(.7)
    targetShootingSpeed = tunable(5300)

    # Other variables
    shooterStoppingDelay = 2

    def on_enable(self):
        """Called when bot is enabled."""
        self.isAutonomous = False

        # self.logger.setLevel(logging.DEBUG)

    def setAutoLoading(self):
        """Runs sensor-based loading."""
        self.isAutomatic = True
        self.next_state('checkForBall')

    def setManualLoading(self):
        """Runs trigger-based loading."""
        self.isAutomatic = False
        self.next_state('runLoaderManually')

    def shootBalls(self):
        """Executes smart shooter."""
        if self.shooterMotors.isLoaderRunning() or self.shooterMotors.isShooterRunning():
            return False
        else:
            self.next_state('initShooting')
            return True

    @state
    def initShooting(self):
        """Smart shooter initialization (reversing if necessary)."""
        if not self.sensors[SensorKey.kShootingSensor].get():
            self.shooterMotors.runLoader(self.loaderMotorSpeed, Direction.kBackwards)

        elif self.sensors[SensorKey.kShootingSensor].get():
            self.shooterMotors.stopLoader()
            self.next_state('runShooter')

    @state
    def runShooter(self):
        """Runs shooter to a certain speed, then lets drivers control loading."""
        self.shooterMotors.runShooter(1)
        if self.shooterMotors.shooterMotor.getEncoder().getVelocity() >= self.targetShootingSpeed:
            if self.xboxMap.getMechRightTrig() > 0 and self.xboxMap.getMechLeftTrig() == 0:
                self.shooterMotors.runLoader(self.loaderMotorSpeed, Direction.kForwards)
                self.logger.debug("right trig manual", self.xboxMap.getMechRightTrig())

            elif self.xboxMap.getMechLeftTrig() > 0 and self.xboxMap.getMechRightTrig() == 0:
                self.shooterMotors.runLoader(self.loaderMotorSpeed, Direction.kBackwards)
                self.logger.debug("left trig manual", self.xboxMap.getMechLeftTrig())

            else:
                self.shooterMotors.stopLoader()

    @state
    def stopShooter(self):
        """Halts all shooter-related tasks and resets to 'checkForBall' state."""
        self.shooterMotors.stopLoader()
        self.shooterMotors.stopShooter()

    def nextAction(self):
        """Determines next loading type."""
        if self.isAutomatic:
            self.next_state_now('checkForBall')
        else:
            self.next_state_now('runLoaderManually')

    def execute(self):
        """Constantly runs state machine. Necessary for function."""
        self.engage()
        super().execute()

class AutonomousShooting(StateMachine):
    """Used only for running the shooter in autonomous."""
    compatString = ["doof"]

    # Component/module related things
    shooterMotors: ShooterMotorCreation
    sensors: Sensors

    # Tunables
    loaderMotorSpeed = tunable(.4)
    targetShootingSpeed = tunable(5300)

    # Other variables
    shooterStoppingDelay = 2

    def on_enable(self):
        """Called when bot is enabled."""
        pass

    def shootBalls(self):
        """Begins shooting process."""
        self.next_state('initShooting')

    @state
    def initShooting(self):
        """Smart shooter initialization (reversing if necessary)."""
        if not self.sensors[SensorKey.kShootingSensor].get():
            self.shooterMotors.runLoader(self.loaderMotorSpeed, Direction.kBackwards)

        elif self.sensors[SensorKey.kShootingSensor].get():
            self.shooterMotors.stopLoader()
            self.next_state('runShooter')

    @state
    def runShooter(self):
        """Runs shooter to a certain speed, then shoots."""
        self.shooterMotors.runShooter(1)
        if self.shooterMotors.shooterMotor.getEncoder().getVelocity() >= self.targetShootingSpeed:
            self.next_state('shoot')

    @timed_state(duration = shooterStoppingDelay, next_state = 'finished')
    def shoot(self):
        """Shoot balls when shooter is up to speed."""
        self.shooterMotors.runLoader(self.loaderMotorSpeed, Direction.kForwards)

    @state
    def finished(self):
        """Called when autonomous finishes shooting."""
        self.done()

    @state(first = True)
    def idling(self):
        """First state. Does nothing here."""
        pass

    def execute(self):
        """Constantly runs state machine. Necessary for function."""
        self.engage()
        super().execute()
