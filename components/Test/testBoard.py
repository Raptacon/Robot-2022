
class TestBoard:
    compatString = ["testBoard"]
    motors_testMotors: dict
    upSpeed = .1
    downSpeed = .1

    def on_enable(self):
        self.motor = self.motors_testMotors["testMotor1"]
        self.speed = 0
        self.motor.set(self.speed)

    def setRaise(self):
        self.speed = self.upSpeed

    def setLower(self):
        self.speed = self.downSpeed

    def stop(self):
        self.speed = 0

    def execute(self):
        self.motor.set(self.speed)
