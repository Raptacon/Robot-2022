import logging
from enum import IntEnum

class Direction(IntEnum):
    """Enum for intake direction."""
    kForwards = 0
    kBackwards = 1
    kDisabled = 2

class ShooterMotorCreation:
    compatString = ["doof"]

    logger: logging
    motors_shooter: dict
    motors_loader: dict

    def on_enable(self):
        self.intakeSpeed = 0
        self.loaderSpeed = 0
        self.shooterSpeed = 0
        self.intake = False
        self.loader = False
        self.shooter = False

        self.loaderMotor = self.motors_loader["loaderMotor"]
        self.intakeMotor = self.motors_loader["intakeMotor"]
        self.shooterMotor = self.motors_shooter["shooterMotor"]

        self.logger.info("Shooter Motor Component Created")

    def runIntake(self, iSpeed, direction):
        if direction == Direction.kForwards:  # Forwards
            self.intakeSpeed = iSpeed
        elif direction == Direction.kBackwards: # Backwards
            self.intakeSpeed = -iSpeed

        self.intake = True

    def runLoader(self, lSpeed, direction):
        if direction == Direction.kForwards: # Forwards
            self.loaderSpeed = lSpeed
        elif direction == Direction.kBackwards: # Backwards
            self.loaderSpeed = -lSpeed

        self.loader = True

    def runShooter(self, sSpeed):
        self.shooterSpeed = sSpeed
        self.shooter = True

    def stopIntake(self):
        self.intake = False

    def stopLoader(self):
        self.loader = False

    def stopShooter(self):
        self.shooter = False

    def isIntakeRunning(self):
        return self.intake

    def isLoaderRunning(self):
        return self.loader

    def isShooterRunning(self):
        return self.shooter

    def execute(self):
        if self.intake:
            self.intakeMotor.set(self.intakeSpeed)
        elif self.intake == False:
            self.intakeMotor.set(0)

        if self.loader:
            self.loaderMotor.set(self.loaderSpeed)
        elif self.loader == False:
            self.loaderMotor.set(0)

        if self.shooter:
            self.shooterMotor.set(self.shooterSpeed)
        elif self.shooter == False:
            self.shooterMotor.set(0)
