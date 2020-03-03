from robotMap import XboxMap
from components.shooterMotors import ShooterMotorCreation, Direction
from magicbot import StateMachine, state, timed_state, tunable
import logging

class ShooterLogic(StateMachine):
    """StateMachine-based shooter. Has both manual and automatic modes."""
    compatString = ["doof"]

    # Component/module related things
    logger: logging
    shooterMotors: ShooterMotorCreation
    # breakSensors: BreakSensors
    xboxMap: XboxMap

    # Tunables
    loaderMotorSpeed = tunable(.4)
    intakeMotorMinSpeed = tunable(.5)
    intakeMotorMaxSpeed = tunable(.7)
    targetShootingSpeed = tunable(5600)

    # Other variables
    shooterStoppingDelay = 2

    # VERBOSE_LOGGING = True

    def on_enable(self):
        """
        Called when bot is enabled.
        NOTE: States with prefix 'auto' are part of automatic loading, and states with prefix 'shoot'
        are involved in the shooting process.
        """
        # self.logger.setLevel(logging.DEBUG)
        self.isAutomatic = False

    def setAutoLoading(self):
        """Runs sensor-based loading."""
        self.next_state('autoIdling')
        self.isAutomatic = True
        return True

    def setManualLoading(self):
        """Runs trigger-based loading."""
        if self.shooterMotors.isLoaderRunning() or self.shooterMotors.isShooterRunning():
            return False
        else:
            self.next_state('runLoaderManually')
            self.isAutomatic = False
            return True

    def shootBalls(self):
        """Executes smart shooter."""
        if self.shooterMotors.isLoaderRunning() or self.shooterMotors.isShooterRunning():
            return False
        else:
            self.next_state('shootInitShooting')
            return True

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

    # Beginning of manual
    @state(first = True)
    def runLoaderManually(self):
        """Trigger-based manual loader."""
        if self.xboxMap.getMechRightTrig() > 0 and self.xboxMap.getMechLeftTrig() == 0:
            self.shooterMotors.runLoader(self.loaderMotorSpeed, Direction.kForwards)
            self.logger.debug("right trig manual", self.xboxMap.getMechRightTrig())

        elif self.xboxMap.getMechLeftTrig() > 0 and self.xboxMap.getMechRightTrig() == 0:
            self.shooterMotors.runLoader(self.loaderMotorSpeed, Direction.kBackwards)
            self.logger.debug("left trig manual", self.xboxMap.getMechLeftTrig())

        else:
            self.shooterMotors.stopLoader()

    @timed_state(duration = .135, next_state = 'autoStopLoader')
    def autoIdling(self):
        """
        Stops ball after a short delay and idles until loading sensor is broken.
        This state calls the private state 'stopLoader', which stops the loader.
        This state is refreshed every .15 seconds, inducing a delay when stopping the
        loader. This is necessary for proper ball intake.
        """
        pass

    @state
    def autoLoadBall(self):
        """Loads ball if ball has entered the hopper and intake was successful."""
        self.shooterMotors.runLoader(self.loaderMotorSpeed, Direction.kForwards)

    @state
    def autoStopLoader(self):
        """Private state, simply stops the loader."""
        self.shooterMotors.stopLoader()

    @state
    def shootInitShooting(self):
        """Smart shooter initialization."""
        pass

    @state
    def shootReverseLoader(self):
        """Reverses loader if shooter is blocked."""
        self.shooterMotors.runLoader(self.loaderMotorSpeed, Direction.kBackwards)

    @state
    def shootRunShooter(self, state_tm):
        """Runs shooter to a certain speed or until a set time."""
        self.shooterMotors.stopLoader()
        self.shooterMotors.runShooter(1)
        if self.shooterMotors.shooterMotor.getEncoder().getVelocity() >= self.targetShootingSpeed or state_tm > 3:
            self.next_state('shootFire')

    @timed_state(duration = shooterStoppingDelay, next_state = 'shootStopShooter')
    def shootFire(self):
        """Runs loader for a set time after shooter is at speed."""
        self.shooterMotors.runLoader(self.loaderMotorSpeed, Direction.kForwards)

    @state
    def shootStopShooter(self):
        """Halts all shooter-related tasks and resets to 'checkForBall' state."""
        self.shooterMotors.stopLoader()
        self.shooterMotors.stopShooter()
        if self.isAutomatic:
            self.next_state('autoIdling')
        elif not self.isAutomatic:
            self.next_state('runLoaderManually')

    def execute(self):
        """Constantly runs state machine. Necessary for function."""
        self.engage()
        self.runIntake()
        super().execute()
