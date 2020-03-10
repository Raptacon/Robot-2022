from robotMap import XboxMap
from components.shooterMotors import ShooterMotorCreation, Direction
from components.breakSensors import Sensors, State
from components.feederMap import FeederMap, Type
from magicbot import StateMachine, state, timed_state, tunable, feedback
import logging

class ShooterLogic(StateMachine):
    """StateMachine-based shooter. Has both manual and automatic modes."""
    compatString = ["doof"]

    # Component/module related things
    shooterMotors: ShooterMotorCreation
    feeder: FeederMap
    logger: logging
    sensors: Sensors
    xboxMap: XboxMap
    speedTolerance = tunable(50)
    # Tunables
    loaderMotorSpeed = tunable(.4)
    intakeMotorMinSpeed = tunable(.5)
    intakeMotorMaxSpeed = tunable(.7)
    shootingSpeed = tunable(5300)
    # Other variables
    isSetup = False
    isAutonomous = False
    shooterStoppingDelay = 3

    def on_enable(self):
        """Called when bot is enabled."""
        self.isAutonomous = False
        self.isSetup = True

    def autonomousEnabled(self):
        """Indicates the robot is in autonomous mode."""
        self.isAutonomous = True

    def autonomousDisabled(self):
        """Indicates the robot is not in autonomous mode."""
        self.isAutonomous = False

    def shootBalls(self):
        """Executes smart shooter."""
        if self.shooterMotors.isLoaderRunning() or self.shooterMotors.isShooterRunning():
            return False
        self.next_state('initShooting')
        return True

    def doneShooting(self):
        """Finishes shooting process and reverts back to appropriate mode."""
        self.next_state('finishShooting')

    @feedback
    def isShooterUpToSpeed(self):
        """Determines if the shooter is up to speed, then rumbles controller and publishes to NetworkTables."""
        autoLoadingSpeed = self.shootingSpeed - self.speedTolerance
        if not self.isSetup:
            return False
        atSpeed = bool(self.shooterMotors.shooterMotor.getEncoder().getVelocity() >= autoLoadingSpeed)
        rumble  = 0
        if atSpeed and not self.isAutonomous:
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
            self.next_state('alignToTarget')

    @state
    def alignToTarget(self):
        """Aligns turret and/or drive train to the goal."""
        self.next_state('runShooter')
        #NOTE: This is a temporary placeholder until we can get limelight alignment successfully implemented.
        #      Useful logic would include: determining if the limelight can see the target before attempting
        #      alignment, especially for autonomous.

    @state
    def runShooter(self):
        """
        Runs shooter to a certain speed, then lets drivers control loading if in teleop.
        If in autonomous, run shooter automatically.
        """
        self.shooterMotors.runShooter(self.shootingSpeed)
        if not self.isAutonomous:
            self.feeder.run(Type.kLoader)

        elif self.isShooterUpToSpeed() and self.isAutonomous:
            self.next_state('autonomousShoot')

    @timed_state(duration = shooterStoppingDelay, next_state = 'finishShooting')
    def autonomousShoot(self):
        """Shoot balls when shooter is up to speed. Strictly for autonomous use."""
        self.shooterMotors.runLoader(self.loaderMotorSpeed, Direction.kForwards)

    @state
    def finishShooting(self):
        """Stops shooter-related motors and moves to idle state."""
        self.shooterMotors.stopLoader()
        self.shooterMotors.stopShooter()
        self.next_state('idling')

    @state(first = True)
    def idling(self):
        """First state. Does nothing here. StateMachine returns to this state when not shooting."""
        pass

    def execute(self):
        """Constantly runs state machine. Necessary for function."""
        self.engage()
        super().execute()
