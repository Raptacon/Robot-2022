from robotMap import XboxMap
from components.shooterMotors import ShooterMotorCreation, Direction
from components.loaderLogic import LoaderLogic
from components.breakSensors import Sensors, State
from magicbot import StateMachine, state, timed_state, tunable, feedback
import logging

class ShooterLogic(StateMachine):
    """StateMachine-based shooter. Has both manual and automatic modes."""
    compatString = ["doof"]

    # Component/module related things
    shooterMotors: ShooterMotorCreation
    loader: LoaderLogic
    logger: logging
    sensors: Sensors
    xboxMap: XboxMap

    # Tunables
    loaderMotorSpeed = tunable(.3)
    targetShootingSpeed = tunable(5600)

    # Other variables
    isSetup = False

    def on_enable(self):
        """Called when bot is enabled."""
        self.isSetup = True

        # self.logger.setLevel(logging.DEBUG)

    def shootBalls(self):
        """Executes smart shooter."""
        if self.shooterMotors.isLoaderRunning() or self.shooterMotors.isShooterRunning():
            return False
        self.loader.next_state('shooting')
        self.next_state('initShooting')
        return True

    def doneShooting(self):
        """Finishes shooting process and reverts back to appropriate mode."""
        self.loader.next_state('nextAction')
        self.next_state('finishShooting')

    def runShooterMotor(self):
        """Specifically runs shooter motor."""
        self.shooterMotors.runShooter(1)

    @feedback
    def isShooterUpToSpeed(self):
        if not self.isSetup:
            return False
        atSpeed = bool(self.shooterMotors.shooterMotor.getEncoder().getVelocity() >= self.targetShootingSpeed)
        rumble  = 0
        if atSpeed:
            rumble = .3
        self.xboxMap.mech.setRumble(self.xboxMap.mech.RumbleType.kLeftRumble, rumble)
        self.xboxMap.mech.setRumble(self.xboxMap.mech.RumbleType.kRightRumble, rumble)
        return atSpeed

    @state
    def initShooting(self):
        """Smart shooter initialization (reversing if necessary)."""
        if self.sensors.shootingSensor(State.kTripped):
            self.shooterMotors.runLoader(self.loaderMotorSpeed, Direction.kBackwards)

        else:
            self.shooterMotors.stopLoader()
            self.next_state('runShooter')

    @state
    def runShooter(self, state_tm):
        """Runs shooter to a certain speed, then lets drivers control loading."""
        if self.isShooterUpToSpeed() or state_tm > 3:
            if self.xboxMap.getMechRightTrig() > 0 and self.xboxMap.getMechLeftTrig() == 0:
                self.shooterMotors.runLoader(self.loaderMotorSpeed, Direction.kForwards)
                self.logger.debug("right trig manual", self.xboxMap.getMechRightTrig())

            elif self.xboxMap.getMechLeftTrig() > 0 and self.xboxMap.getMechRightTrig() == 0:
                self.shooterMotors.runLoader(self.loaderMotorSpeed, Direction.kBackwards)
                self.logger.debug("left trig manual", self.xboxMap.getMechLeftTrig())

    @state
    def finishShooting(self):
        """Stops shooter-related motors and moves to idle state."""
        self.shooterMotors.stopLoader()
        self.shooterMotors.stopShooter()
        self.next_state('idling')

    @state(first = True)
    def idling(self):
        """First state. Does nothing here."""
        pass

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
    loaderMotorSpeed = tunable(.3)
    targetShootingSpeed = tunable(5600)

    # Other variables
    shooterStoppingDelay = 3

    def on_enable(self):
        """Called when bot is enabled."""
        pass

    def shootBalls(self):
        """Begins shooting process."""
        self.next_state_now('initShooting')

    def runShooterMotor(self):
        """Specifically runs shooter motor."""
        self.shooterMotors.runShooter(1)

    @state
    def initShooting(self):
        """Smart shooter initialization (reversing if necessary)."""
        if self.sensors.shootingSensor(State.kTripped):
            self.shooterMotors.runLoader(self.loaderMotorSpeed, Direction.kBackwards)

        else:
            self.shooterMotors.stopLoader()
            self.next_state('runShooter')

    @state
    def runShooter(self, state_tm):
        """Runs shooter to a certain speed, then shoots."""
        if self.shooterMotors.shooterMotor.getEncoder().getVelocity() >= self.targetShootingSpeed or state_tm > 3:
            self.next_state('shoot')

    @timed_state(duration = shooterStoppingDelay, next_state = 'finished')
    def shoot(self):
        """Shoot balls when shooter is up to speed."""
        self.shooterMotors.runLoader(self.loaderMotorSpeed, Direction.kForwards)

    @state
    def finished(self):
        """Called when autonomous finishes shooting."""
        self.shooterMotors.stopLoader()
        self.shooterMotors.stopShooter()
        self.done()

    @state(first = True)
    def idling(self):
        """First state. Does nothing here."""
        pass

    def execute(self):
        """Constantly runs state machine. Necessary for function."""
        self.engage()
        super().execute()
