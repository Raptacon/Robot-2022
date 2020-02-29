
class Lifter:
    compatString = ["doof"]
    motors_lifter: dict

    def on_enable(self):
        self.upSpeed = 0
        self.winchMotor = self.motors_lifter["winchMotor"]

        self.logger.info("Lifter Component Created")
    
    def setRaise(self):
        """
        Sets the motor speed to .5 in order to reel in the winch
        """
        self.upSpeed = .5

    def stop(self):
        """
        Sets the motor speed to 0 in order to stop the winch
        """
        self.upSpeed = 0

    def execute(self):
        self.winchMotor.set(self.upSpeed)
