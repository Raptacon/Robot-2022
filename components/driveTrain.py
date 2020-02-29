import wpilib.drive

from magicbot import tunable

class DriveTrain():
    # Note - The way we will want to do this will be to give this component motor description dictionaries from robotmap and then creating the motors with motorhelper. After that, we simply call wpilib' differential drive
    motors_driveTrain: dict
    driveMotorsMultiplier = tunable(.5)
    def setup(self):
        self.tankLeftSpeed = 0
        self.tankRightSpeed = 0
        self.arcadeSpeed = 0
        self.arcadeRotation = 0
        self.controllingOverArcade = False
        self.controllingOverTank = False
        self.leftMotor = self.motors_driveTrain["leftMotor"]
        self.rightMotor = self.motors_driveTrain["rightMotor"]
        self.driveTrain = wpilib.drive.DifferentialDrive(self.leftMotor, self.rightMotor)
        self.logger.info("DriveTrain setup completed")
        

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

    def creeperMode(self):
        """set driveMotorMultiplier to .25"""
        self.prevMultiplier = .5
        self.driveMotorMutliplier = .25

    def disableCreeperMode(self):
        self.driveMotorMultiplier = self.prevMultiplier

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
