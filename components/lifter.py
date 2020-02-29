
class Lifter:
    compatString = ["doof"]
    motors_lifter: dict

    def on_enable(self):
        self.upSpeed = 0
        self.winchMotor = self.motors_lifter["winchMotor"]

        self.logger.info("Lifter Component Created")
    
    def setRaise(self):
        self.upSpeed = .5

    def stop(self):
        self.upSpeed = 0

    def execute(self):
        self.winchMotor.set(self.upSpeed)
