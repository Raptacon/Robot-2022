import wpilib
import motorHelper

class ShooterMotorCreation:

    motorsList: dict

    def on_enable(self):
        self.intakeSpeed = 0
        self.loaderSpeed = 0
        self.shooterSpeed = 0
        self.shooterEncoder = 0
        self.intake = False
        self.loader = False
        self.shooter = False

        self.motors = {}

        # shooter_MotorsList is the 'config.yml' dictionary
        for motorDescKey in self.motorsList: # 'motorDescKey' is the key to look up within 'driveMotors'
            currentMotor = self.motorsList[motorDescKey] # Actual value of key (like 'rightMotor')
            print("{}".format(currentMotor)) # Prints actual value of key (like 'rightMotor')
            self.motors[motorDescKey] = motorHelper.createMotor(currentMotor)

        self.loaderMotor = self.motors["loaderMotor"]
        self.intakeMotor = self.motors["intakeMotor"]
        self.shooterMotor = self.motors["shooterMotor"]

    def runLoader(self, lSpeed):
        self.loaderSpeed = lSpeed
        self.loader = True

    def runIntake(self, iSpeed):
        self.intakeSpeed = iSpeed

    def runShooter(self, sSpeed):
        self.shooterSpeed = sSpeed
        self.shooter = True

    def stopLoader(self):
        self.loader = False

    def stopShooter(self):
        self.shooter = False

    def isShooterAtSpeed(self):
        self.shooterEncoder = 1

    def execute(self):
        if self.intakeSpeed > 0:
            self.intakeMotor.set(self.intakeSpeed)
        elif self.intakeSpeed == 0:
            self.intakeMotor.set(0)

        if self.loader:
            self.loaderMotor.set(self.loaderSpeed)
        elif self.loader == False:
            self.loaderMotor.set(0)

        if self.shooter:
            self.shooterMotor.set(self.shooterSpeed)
        elif self.shooter == False:
            self.shooterMotor.set(0)
