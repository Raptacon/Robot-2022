import logging as log
from enum import Enum, auto

class Direction(Enum):
    """Enum for intake direction."""
    kForwards = auto()
    kBackwards = auto()
    kDisabled = auto()

class ShooterMotorCreation:
    """
    Allows you to run motors in the intake
    """
    compatString = ["doof"]

    def on_enable(self):
        """
        Sets up shooter motors
        """
        self.intakeSpeed = 0
        self.loaderSpeed = 0
        self.shooterSpeed = 0
        self.intake = False
        self.loader = False
        self.shooter = False

        self.intakeMotor = self.motors_loader["intakeMotor"]
        self.shooterMotor = self.motors_shooter["shooterMotor"]

        log.info("Shooter Motor Component Created")

    motors_loader: dict

    def runIntake(self, iSpeed, direction):
        """
        Sets the intake to speed iSpeed
        """
        if direction == Direction.kForwards:  # Forwards
            self.intakeSpeed = iSpeed
        elif direction == Direction.kBackwards: # Backwards
            self.intakeSpeed = -iSpeed
        elif direction == Direction.kDisabled:
            self.intakeSpeed = 0

        self.intake = True

    def stopIntake(self):
        """
        Turns the intake off
        """
        self.intake = False

    def isIntakeRunning(self):
        return self.intake

    def execute(self):
        if self.intake:
            self.intakeMotor.set(self.intakeSpeed)
        elif self.intake == False:
            self.intakeMotor.set(0)
