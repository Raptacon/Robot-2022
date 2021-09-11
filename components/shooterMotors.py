import logging as log
from enum import Enum, auto

class Direction(Enum):
    """Enum for intake direction."""
    kForwards = auto()
    kBackwards = auto()
    kDisabled = auto()

class ShooterMotorCreation:
    """
    Allows you to run motors in the shooter
    """
    compatString = ["doof"]

    motors_shooter: dict
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

    def runLoader(self, lSpeed, direction):
        """
        Sets the hopper motor to speed lSpeed
        """
        if direction == Direction.kForwards: # Forwards
            self.loaderSpeed = lSpeed
        elif direction == Direction.kBackwards: # Backwards
            self.loaderSpeed = -lSpeed

        self.loader = True

    def runShooter(self, sSpeed):
        """
        Sets the shooter to speed sSpeed
        """
        self.shooterSpeed = sSpeed
        self.shooter = True

    def stopIntake(self):
        """
        Turns the intake off
        """
        self.intake = False

    def stopLoader(self):
        """
        Turns the loader off
        """
        self.loader = False

    def stopShooter(self):
        """
        Turns the shooter off
        """
        self.shooter = False

    def isIntakeRunning(self):
        return self.intake

    def isLoaderRunning(self):
        return self.loader

    def isShooterRunning(self):
        return self.shooter

    def execute(self):
        """
        Sets all the motors to previously defined values. If not set by methods, set to 0.
        """
        if self.intake:
            self.intakeMotor.set(self.intakeSpeed)
        elif self.intake == False:
            self.intakeMotor.set(0)

        if self.loader:
            self.hopperMotor1.set(self.loaderSpeed)
        elif self.loader == False:
            self.hopperMotor1.set(0)

        if self.shooter:
            self.shooterMotor.set(self.shooterSpeed)
        elif self.shooter == False:
            self.shooterMotor.set(0)
