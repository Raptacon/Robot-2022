import logging
from robotMap import XboxMap
from components.Actuators.LowLevel.shooterMotors import ShooterMotors
from components.Actuators.HighLevel.hopperMotor import HopperMotor
from components.Actuators.LowLevel.intakeMotor import IntakeMotor
from utils.DirectionEnums import Direction
from magicbot import StateMachine, state, timed_state, tunable, feedback

class ShooterLogic(StateMachine):
    """StateMachine-based shooter. Has both manual and automatic modes."""
    compatString = ["teapot"]

    # Component/module related things
    shooterMotors: ShooterMotors
    hopperMotor: HopperMotor
    intakeMotor: IntakeMotor
    xboxMap: XboxMap

    # Tunables
    backDownLoaderSpeed = tunable(.02)
    backsideShootingLoaderSpeed = tunable(.4)
    foresideShootingLoaderSpeed = tunable(.5)
    autoShootingSpeed1 = tunable(1150)
    autoShootingSpeed2 = tunable(3100)
    teleShootingSpeed1 = tunable(1500)
    teleShootingSpeed2 = tunable(3350)
    manualShootingSpeed1 = 1400
    manualShootingSpeed2 = 3300
    shootTolerance = 25

    # Other variables
    isSetup = False
    isAutonomous = False
    isManual = False
    shooting = False
    shooterStoppingDelay = 3

    def on_enable(self):
        """Called when bot is enabled."""
        self.running = False
        self.start = False
        self.isAutonomous = False
        self.isManual = False
        self.isSetup = True

        self.shooterMotor1Encoder = self.shooterMotors.shooterMotor1Encoder
        self.shooterMotor2Encoder = self.shooterMotors.shooterMotor2Encoder

    def autonomousEnabled(self):
        """Indicates if the robot is in autonomous mode."""
        self.isAutonomous = True

    def autonomousDisabled(self):
        """Indicates if the robot is not in autonomous mode."""
        self.isAutonomous = False

    def setManualShooting(self):
        """Indicates if the bot will be set to a dumb speed"""
        self.isManual = True

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
        if self.hopperMotor.isHopperBacksideRunning() or self.shooterMotors.isShooterRunning():
            return False
        self.next_state('runShooter')

    def doneShooting(self):
        """Finishes shooting process and reverts back to appropriate mode."""
        self.start = False
        self.running = False
        self.next_state('finishShooting')

    @feedback
    def isShooterUpToSpeed(self):
        """Determines if the shooter is up to speed, then rumbles controller and publishes to NetworkTables."""
        if self.isAutonomous:
            shootSpeed1 = self.autoShootingSpeed1
            shootSpeed2 = self.autoShootingSpeed2
        elif self.isManual:
            shootSpeed1 = self.manualShootingSpeed1
            shootSpeed2 = self.manualShootingSpeed2
        elif not self.isAutonomous:
            shootSpeed1 = self.teleShootingSpeed1
            shootSpeed2 = self.teleShootingSpeed2
        if not self.isSetup:
            return False
        atSpeed = (abs(self.shooterMotor1Encoder.getVelocity() - shootSpeed1) <= abs(self.shootTolerance)
                and abs(self.shooterMotor2Encoder.getVelocity() - shootSpeed2) <= abs(self.shootTolerance))
        rumble  = 0
        if atSpeed and not self.isAutonomous:
            rumble = 1
        self.xboxMap.drive.setRumble(self.xboxMap.mech.RumbleType.kLeftRumble, rumble)
        self.xboxMap.drive.setRumble(self.xboxMap.mech.RumbleType.kRightRumble, rumble)
        self.xboxMap.mech.setRumble(self.xboxMap.mech.RumbleType.kLeftRumble, rumble)
        self.xboxMap.mech.setRumble(self.xboxMap.mech.RumbleType.kRightRumble, rumble)
        return atSpeed

    @state
    def runShooter(self):
        """
        Runs shooter to a certain speed, then lets drivers control loading if in teleop.
        If in autonomous, run shooter automatically.
        """
        self.shooting = True
        if not self.isAutonomous:
            if self.isManual:
                self.shooterMotors.runShooter(self.manualShootingSpeed1, self.manualShootingSpeed2)
            else:
                self.shooterMotors.runShooter(self.teleShootingSpeed1, self.teleShootingSpeed2)
            if self.isShooterUpToSpeed():
                self.hopperMotor.runHopperMotorBackside(self.backsideShootingLoaderSpeed, Direction.kForwards)
                self.hopperMotor.runHopperMotorForeside(self.foresideShootingLoaderSpeed, Direction.kForwards)
            else:
                self.next_state('runShooter')

        elif self.isAutonomous:
            self.shooterMotors.runShooter(self.autoShootingSpeed1, self.autoShootingSpeed2)
            self.next_state('autonomousShoot')

    @timed_state(duration = shooterStoppingDelay, next_state = 'finishShooting')
    def autonomousShoot(self):
        """Shoot balls when shooter is up to speed. Strictly for autonomous use."""
        if self.isShooterUpToSpeed():
            self.hopperMotor.runHopperMotorBackside(self.backsideShootingLoaderSpeed, Direction.kForwards)
            self.hopperMotor.runHopperMotorForeside(self.foresideShootingLoaderSpeed, Direction.kForwards)
        else:
            self.hopperMotor.runHopperMotorBackside(self.backDownLoaderSpeed, Direction.kBackwards)
            self.hopperMotor.runHopperMotorForeside(self.backDownLoaderSpeed, Direction.kBackwards)
            self.next_state('autonomousShoot')

    @state
    def finishShooting(self):
        """Stops shooter-related motors and moves to idle state."""
        self.running = False
        self.isManual = False
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
