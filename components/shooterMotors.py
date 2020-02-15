# git stage -p
# git commit
# git push

import wpilib
import motorHelper
from components.sensor import sensors

class ShooterMotorCreation:

    shooter_MotorsList: dict

    def on_enable(self):
        self.loaderSpeed = 1
        self.intakeSpeed = 1
        self.shooterSpeed = 0
        self.motors = {}

        # shooter_MotorsList is the 'config.yml' dictionary
        for motorDescKey in self.shooter_MotorsList: # 'motorDescKey' is the key to look up within 'driveMotors'
            currentMotor = self.shooter_MotorsList[motorDescKey] # Actual value of key (like 'rightMotor')
            print("{}".format(currentMotor)) # Prints actual value of key (like 'rightMotor')
            self.motors[motorDescKey] = motorHelper.createMotor(currentMotor)

        self.loaderMotor = self.motors["loaderMotor"]
        self.intakeMotor = self.motors["intakeMotor"]
        self.shooterMotor = self.motors["shooterMotor"]

    def getLoaderMotor(self):
        self.loaderMotor.get()

    def getIntakeMotor(self):
        self.intakeMotor.get()

    def getShooterMotor(self):
        self.shooterMotor.get()

    def setLoaderMotor(self, lSpeed):
        self.loaderSpeed = lSpeed
        lSpeed = 1
        self.loaderMotor.set(lSpeed)

    def setIntakeSpeed(self, iSpeed):
        self.intakeSpeed = iSpeed
        self.intakeMotor.set(iSpeed)

    def setShooterSpeed(self, sSpeed):
        self.shooterSpeed = sSpeed
        self.shooterMotor.set(sSpeed)

    def execute(self):
        pass
