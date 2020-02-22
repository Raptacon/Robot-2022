import wpilib.drive


class DriveTrain:
    # Note - The way we will want to do this will be to give this component motor description dictionaries from robotmap and then creating the motors with motorhelper. After that, we simply call wpilib' differential drive
    motorsList: dict

    def setup(self):
        self.tankLeftSpeed = 0
        self.tankRightSpeed = 0
        self.arcadeSpeed = 0
        self.arcadeRotation = 0
        self.controllingOverArcade = False
        self.controllingOverTank = False
        self.motors = self.motorsList
        self.leftMotor = self.motors["leftMotor"]
        self.rightMotor = self.motors["rightMotor"]
        self.driveTrain = wpilib.drive.DifferentialDrive(self.leftMotor, self.rightMotor)

        print("DriveTrain component setup")

    def getLeft(self):
        return self.leftMotor.get()

    def getRight(self):
        return self.rightMotor.get()

    def isStopping(self):
        pass

    def setTank(self, leftSpeed, rightSpeed):
        self.controllingOverArcade = False
        self.controllingOverTank = True
        self.tankLeftSpeed = leftSpeed
        self.tankRightSpeed = rightSpeed

    def setArcade(self, speed, rotation):
        self.controllingOverTank = False
        self.controllingOverArcade = True
        self.arcadeSpeed = speed
        self.arcadeRotation = rotation

    def stop(self, coast=False):
        self.controllingOverTank = False
        self.controllingOverArcade = False

    def getMeasuredSpeed(self):
        pass

    def execute(self):
        if self.controllingOverTank:
            self.driveTrain.tankDrive(self.tankLeftSpeed, self.tankRightSpeed, False)

        elif self.controllingOverArcade:
            self.driveTrain.arcadeDrive(self.arcadeSpeed, self.arcadeRotation, False)
