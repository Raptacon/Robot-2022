import logging as log
from enum import Enum, auto

class ShooterMotors:
    """
    Allows you to run motors in the shooter
    Relies on a config with 2 shooter motors
    """
    compatString = []

    motors_shooter: dict

    def on_enable(self):
        """
        Sets up shooter motors
        """
        self.shooterSpeed1 = 0
        self.shooterSpeed2 = 0
        self.shooter = False

        self.shooterMotor1 = self.motors_shooter["shooterMotor1"]
        self.shooterMotor2 = self.motors_shooter["shooterMotor2"]

        log.info("Shooter Motor Component Created")

    def runShooter(self, sSpeed1, sSpeed2):
        """
        Sets the shooter to speed sSpeed
        """
        self.shooterSpeed1 = sSpeed1
        self.shooterSpeed2 = sSpeed2
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
            self.shooterMotor1.set(self.shooterSpeed1)
            self.shooterMotor2.set(self.shooterSpeed2)
        elif self.shooter == False:
            self.shooterMotor1.set(0)
            self.shooterMotor2.set(0)
