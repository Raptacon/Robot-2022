from magicbot import tunable

class Elevator:
    compatString = ["doof"]
    motors_loader: dict

    def on_enable(self):
        self.upSpeed = 0
        self.elevatorMotor = self.motors_loader['elevatorMotor']
        self.downSpeed = tunable(-.4)
        self.upSpeed = tunable(.7)
        self.speed = 0
        print("Elevator Enabled")
    
    def setSpeed(self, speed):
        self.speed = speed

    def setRaise(self):
        self.speed = self.upSpeed

    def setLower(self):
        self.speed = self.downSpeed

    def stop(self):
        self.speed = 0
    
    def execute(self):
        self.elevatorMotor.set(self.speed)
