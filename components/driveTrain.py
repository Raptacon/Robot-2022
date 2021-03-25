import wpilib.drive
from enum import Enum, auto
import logging as log
import ctre

from magicbot import tunable
class ControlMode(Enum):
    """
    Drive Train Control Modes
    """
    kArcadeDrive = auto()
    kTankDrive = auto()
    kAngleTurning = auto()
    kDisabled = auto()

class DriveTrain():
    compatString = ["doof","scorpion"]
    # Note - The way we will want to do this will be to give this component motor description dictionaries from robotmap and then creating the motors with motorhelper. After that, we simply call wpilib' differential drive
    motors_driveTrain: dict
    driveMotorsMultiplier = tunable(.5)
    gyros_system: dict

    def setup(self):
        self.tankLeftSpeed = 0
        self.tankRightSpeed = 0
        self.arcadeSpeed = 0
        self.arcadeRotation = 0
        self.creeperMode = False
        self.controlMode = ControlMode.kDisabled
        self.leftMotor = self.motors_driveTrain["leftMotor"]
        self.rightMotor = self.motors_driveTrain["rightMotor"]
        self.driveTrain = wpilib.drive.DifferentialDrive(self.leftMotor, self.rightMotor)
        log.info("DriveTrain setup completed")

    def setBraking(self, braking:bool):
        self.leftMotor.setBraking(braking)
        self.rightMotor.setBraking(braking)
        if braking:
            self.leftFollower.setNeutralMode(ctre.NeutralMode.Brake)
            self.rightFollower.setNeutralMode(ctre.NeutralMode.Brake)
        else:
            self.leftFollower.setNeutralMode(ctre.NeutralMode.Coast)
            self.rightFollower.setNeutralMode(ctre.NeutralMode.Coast)

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

    def enableCreeperMode(self):
        """when left bumper is pressed, it sets the driveMotorsMultiplier to .25"""
        if self.creeperMode:
            return
        self.prevMultiplier = self.driveMotorsMultiplier
        self.driveMotorsMultiplier = .25
        self.creeperMode = True

    def disableCreeperMode(self):
        """when left bumper is released, it sets the multiplier back to it's original value"""
        if not self.creeperMode:
            return
        self.driveMotorsMultiplier = self.prevMultiplier
        self.creeperMode = False

    def stop(self, coast=False):
        self.controlMode = ControlMode.kDisabled

    def getMeasuredSpeed(self):
        pass

    def execute(self):
        if self.controlMode == ControlMode.kTankDrive:
            self.driveTrain.tankDrive(self.tankLeftSpeed, self.tankRightSpeed, False)

        elif self.controlMode == ControlMode.kArcadeDrive:
            self.driveTrain.arcadeDrive(self.arcadeSpeed, self.arcadeRotation, False)
