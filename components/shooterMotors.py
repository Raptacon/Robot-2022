import logging as log
from enum import Enum, auto

class ShooterMotors:
    """
    Allows you to run motors in the shooter
    """
    compatString = ["doof"]

    motors_shooter: dict

    def on_enable(self):
        """
        Sets up shooter motors
        """
        self.shooterSpeed = 0
        self.shooter = False

        self.shooterMotor = self.motors_shooter["shooterMotor"]

        log.info("Shooter Motor Component Created")

    def runShooter(self, sSpeed):
        """
        Sets the shooter to speed sSpeed
        """
        self.shooterSpeed = sSpeed
        self.shooter = True

    def stopShooter(self):
        """
        Turns the shooter off
        """
        self.shooter = False

    def isShooterRunning(self):
        return self.shooter

    def execute(self):
        """
        Sets all the motors to previously defined values. If not set by methods, set to 0.
        """
        if self.shooter:
            self.shooterMotor.set(self.shooterSpeed)
        elif self.shooter == False:
            self.shooterMotor.set(0)
