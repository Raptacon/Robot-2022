
class Elevator:
    motorsList: dict

    def on_enable(self):
        self.upSpeed = 0
        self.elevatorMotor = self.motorsList['elevatorMotor']

        print("Elevator Enabled")
    
    def setSpeed(self, speed):
        self.upSpeed = speed

    def setRaise(self):
        self.upSpeed = .7

    def setLower(self):
        self.upSpeed = -.4

    def stop(self):
        self.upSpeed = 0
    
    def execute(self):
        self.elevatorMotor.set(self.upSpeed)
