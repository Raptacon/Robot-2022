from robotMap import XboxMap
from components.Actuators.LowLevel.shooterMotors import ShooterMotors
from components.Actuators.LowLevel.hopperMotor import HopperMotor
from components.Actuators.LowLevel.intakeMotor import IntakeMotor
from components.Input.breakSensors import Sensors, State
from utils.DirectionEnums import Direction
from magicbot import StateMachine, state, timed_state, tunable, feedback

class ShooterLogic(StateMachine):
    """StateMachine-based shooter. Has both manual and automatic modes."""
    compatString = []

    # Component/module related things
    shooterMotors: ShooterMotors
    hopperMotor: HopperMotor
    intakeMotor: IntakeMotor
    sensors: Sensors
    xboxMap: XboxMap
    speedTolerance = tunable(75)

    # Tunables
    shootingLoaderSpeed = tunable(.4)
    autoShootingSpeed1 = tunable(2200)
    autoShootingSpeed2 = tunable(2200)
    teleShootingSpeed1 = tunable(2350)
    teleShootingSpeed2 = tunable(1900)

    # Other variables
    isSetup = False
    isAutonomous = False
    shooting = False
    shooterStoppingDelay = 3

    def on_enable(self):
        """Called when bot is enabled."""
        self.running = False
        self.start = False
        self.isAutonomous = False
        self.isSetup = True

    def autonomousEnabled(self):
        """Indicates if the robot is in autonomous mode."""
        self.isAutonomous = True

    def autonomousDisabled(self):
        """Indicates if the robot is not in autonomous mode."""
        self.isAutonomous = False

    def setRPM(self, rpm1, rpm2=0):
        self.teleShootingSpeed1 = rpm1
        if rpm2 != 0:
            self.teleShootingSpeed2 = rpm2
        else:
            self.teleShootingSpeed2 = rpm1

    @state
    def shootBalls(self):
        """Executes smart shooter."""
        self.start = False
        self.running = True
        if self.hopperMotor.isHopperRunning() or self.shooterMotors.isShooterRunning():
            return False
        self.next_state('initShooting')
        return True

    def doneShooting(self):
        """Finishes shooting process and reverts back to appropriate mode."""
        self.start = False
        self.running = False
        self.next_state('finishShooting')

    @feedback
    def isShooterUpToSpeed(self):
        """Determines if the shooter is up to speed, then rumbles controller and publishes to NetworkTables."""
        if self.isAutonomous:
            shootSpeed1 = self.autoShootingSpeed1 - self.speedTolerance
            shootSpeed2 = self.autoShootingSpeed2 - self.speedTolerance
        elif not self.isAutonomous:
            shootSpeed1 = self.teleShootingSpeed1 - self.speedTolerance
            shootSpeed2 = self.teleShootingSpeed2 - self.speedTolerance
        if not self.isSetup:
            return False
        atSpeed = (bool(self.shooterMotors.shooterMotor1.getEncoder().getVelocity() >= shootSpeed1)
                and bool(self.shooterMotors.shooterMotor2.getEncoder().getVelocity() >= shootSpeed2))
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
            self.hopperMotor.runHopper(self.shootingLoaderSpeed, Direction.kBackwards)
            self.next_state('initShooting')

        else:
            self.hopperMotor.stopHopper()
            self.next_state('runShooter')

    @state
    def runShooter(self):
        """
        Runs shooter to a certain speed, then lets drivers control loading if in teleop.
        If in autonomous, run shooter automatically.
        """
        self.shooting = True
        if not self.isAutonomous:
            self.shooterMotors.runShooter(self.teleShootingSpeed1, self.teleShootingSpeed2)
            if self.isShooterUpToSpeed():
                self.hopperMotor.runHopper(self.shootingLoaderSpeed, Direction.kForwards)
            else:
                self.hopperMotor.runHopper(0, Direction.kForwards)
                self.next_state('runShooter')

        elif self.isAutonomous:
            self.shooterMotors.runShooter(self.autoShootingSpeed1, self.autoShootingSpeed2)
            if self.isShooterUpToSpeed():
                self.next_state('autonomousShoot')

    @timed_state(duration = shooterStoppingDelay, next_state = 'finishShooting')
    def autonomousShoot(self):
        """Shoot balls when shooter is up to speed. Strictly for autonomous use."""
        if self.isShooterUpToSpeed():
            self.hopperMotor.runHopper(self.shootingLoaderSpeed, Direction.kForwards)
        else:
            self.hopperMotor.runHopper(0, Direction.kForwards)
            self.next_state('autonomousShoot')

    @state
    def finishShooting(self):
        """Stops shooter-related motors and moves to idle state."""
        self.running = False
        self.hopperMotor.stopHopper()
        self.shooterMotors.stopShooter()
        self.next_state('idling')

    @state(first = True)
    def idling(self):
        """First state. Does nothing here. StateMachine returns to this state when not shooting."""
        self.shooting = False
        if self.start == True:
            self.next_state('shootBalls')

    def execute(self):
        """Constantly runs state machine. Necessary for function."""
        self.engage()
        super().execute()

    def startShooting(self):
        self.start = True
