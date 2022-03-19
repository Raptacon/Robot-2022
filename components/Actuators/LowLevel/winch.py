
class Winch:
    compatString = ["teapot"]
    motors_winch: dict

    def on_enable(self):
        """
        Sets up the winch
        """
        self.upSpeed = 0
        self.winchMotor = self.motors_winch["winchMotor"]

        self.logger.info("Lifter Component Created")

    def setRaise(self):
        """
        Sets the motor speed to .5 in order to reel in the winch
        """
        self.upSpeed = .5

    def setLower(self):
        self.upSpeed = -.5

    def stop(self):
        """
        Sets the motor speed to 0 in order to stop the winch
        """
        self.upSpeed = 0

    def execute(self):
        self.winchMotor.set(self.upSpeed)
