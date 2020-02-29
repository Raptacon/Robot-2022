import wpilib.drive
from enum import Enum, auto

<<<<<<< HEAD
from magicbot import tunable
=======
class ControlMode(Enum):
    """
    Drive Train Control Modes
    """
    kArcadeDrive = auto()
    kTankDrive = auto()
    kAngleTurning = auto()
    kDisabled = auto()
>>>>>>> upstream/master

class DriveTrain():
    # Note - The way we will want to do this will be to give this component motor description dictionaries from robotmap and then creating the motors with motorhelper. After that, we simply call wpilib' differential drive
    motors_driveTrain: dict
<<<<<<< HEAD
    driveMotorsMultiplier = tunable(.5)
=======
    gyros_system: dict

>>>>>>> upstream/master
    def setup(self):
        self.tankLeftSpeed = 0
        self.tankRightSpeed = 0
        self.arcadeSpeed = 0
        self.arcadeRotation = 0
        self.controlMode = ControlMode.kDisabled
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
        self.controlMode = ControlMode.kTankDrive
        self.tankLeftSpeed = leftSpeed
        self.tankRightSpeed = rightSpeed

    def setArcade(self, speed, rotation):
        self.controlMode = ControlMode.kArcadeDrive
        self.arcadeSpeed = speed
        self.arcadeRotation = rotation

    def creeperMode(self):
        """set driveMotorMultiplier to .25"""
        self.prevMultiplier = .5
        self.driveMotorsMultiplier = .25

    def disableCreeperMode(self):
        self.driveMotorsMultiplier = self.prevMultiplier

    def stop(self, coast=False):
        self.controlMode = ControlMode.kDisabled

    def getMeasuredSpeed(self):
        pass

    def execute(self):
        if self.controlMode == ControlMode.kTankDrive:
            self.driveTrain.tankDrive(self.tankLeftSpeed, self.tankRightSpeed, False)

        elif self.controlMode == ControlMode.kArcadeDrive:
            self.driveTrain.arcadeDrive(self.arcadeSpeed, self.arcadeRotation, False)
        
