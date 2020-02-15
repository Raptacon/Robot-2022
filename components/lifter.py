import motorHelper

class Lifter:
    motorsList: dict

    def on_enable(self):
        self.upSpeed = 0
        self.motors = {}

        for motorDescKey in self.motorsList:
            currentMotor = self.motorsList[motorDescKey]
            print("{}".format(currentMotor))
            self.motors[motorDescKey] = motorHelper.createMotor(currentMotor)

        self.winchMotor = self.motors["winchMotor"]
        self.winchFollower = self.motors["winchFollower"]

        print("Lifter Enabled")
    
    def setSpeed(self, speed):
        self.upSpeed = speed
    
    def execute(self):
        self.winchMotor.set(self.upSpeed)