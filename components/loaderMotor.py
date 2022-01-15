import logging as log
from enum import Enum, auto

class Direction(Enum):
    """Enum for intake direction."""
    kForwards = auto()
    kBackwards = auto()
    kDisabled = auto()

class ShooterMotorCreation:
    """
    Allows you to run motors in the loader
    """
    compatString = ["doof"]

    motors_loader: dict

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

        self.hopperMotor1 = self.motors_loader["hopperMotor1"]
        self.intakeMotor = self.motors_loader["intakeMotor"]
        self.shooterMotor = self.motors_shooter["shooterMotor"]

        log.info("Shooter Motor Component Created")

    def runLoader(self, lSpeed, direction):
        """
        Sets the hopper motor to speed lSpeed
        """
        if direction == Direction.kForwards: # Forwards
            self.loaderSpeed = lSpeed
        elif direction == Direction.kBackwards: # Backwards
            self.loaderSpeed = -lSpeed

        self.loader = True

    def stopLoader(self):
        """
        Turns the loader off
        """
        self.loader = False

    def isLoaderRunning(self):
        return self.loader

    def execute(self):
        if self.loader:
            self.hopperMotor1.set(self.loaderSpeed)
        elif self.loader == False:
            self.hopperMotor1.set(0)
