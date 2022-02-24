import logging as log

class ShooterMotors:
    """
    Allows you to run motors in the shooter
    Relies on a config with 2 shooter motors
    """
    compatString = ["teapot"]

    motors_shooter: dict

    def setup(self):
        self.shooterMotor1 = self.motors_shooter["shooterMotor1"]
        self.shooterMotor2 = self.motors_shooter["shooterMotor2"]
        self.shooterMotor1Encoder = self.shooterMotor1.encoder
        self.shooterMotor2Encoder = self.shooterMotor2.encoder

    def on_enable(self):
        """
        Sets up shooter motors
        """
        self.shooterSpeed1 = 0
        self.shooterSpeed2 = 0
        self.shooter = False

        log.info("Shooter Motor Component Created")

    def runShooter(self, sSpeed1, sSpeed2):
        """
        Sets the shooter motors to sSpeed1 and 2
        :param sSpeed1: RPMs if we're using PID. OR
        double/float 0 to 1, where 0 is nothing and 1 is full speed
        if we're not using PID.
        :param sSpeed2: The speed for the second motor.
        Follows the same convention as the first.
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
        """
        Returns True if the shooter is running.
        """
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
