from utils.UnitEnums import positionUnits
from enum import Enum, auto
import ctre
import math
import wpilib.drive
import logging as log
from networktables import NetworkTables

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
    compatString = ["doof","scorpion", "greenChassis"]
    # Note - The way we will want to do this will be to give this component motor description dictionaries from robotmap and then creating the motors with motorhelper. After that, we simply call wpilib' differential drive
    motors_driveTrain: dict
    driveMotorsMultiplier = tunable(.5)
    creeperMotorsMultiplier = tunable(.25)
    gyros_system: dict
    gearRatio = 10
    wheelCircumference = 6 * math.pi

    smartDashTable = NetworkTables.getTable("SmartDashboard")

    # Encoder variables
    leftSideSensorInverted = True
    rightSideSensorInverted = False

    def setup(self):
        self.tankLeftSpeed = 0
        self.tankRightSpeed = 0
        self.arcadeSpeed = 0
        self.arcadeRotation = 0
        self.creeperMode = False
        self.controlMode = ControlMode.kDisabled
        self.leftMotor = self.motors_driveTrain["leftMotor"]
        self.rightMotor = self.motors_driveTrain["rightMotor"]
        self.leftFollower = self.motors_driveTrain["leftFollower"]
        self.rightFollower = self.motors_driveTrain["rightFollower"]
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
        self.driveMotorsMultiplier = self.creeperMotorsMultiplier
        self.creeperMode = True

    def disableCreeperMode(self):
        """when left bumper is released, it sets the multiplier back to it's original value"""
        if not self.creeperMode:
            return
        self.driveMotorsMultiplier = self.prevMultiplier
        self.creeperMode = False

    def stop(self):
        self.controlMode = ControlMode.kDisabled

    def getMeasuredSpeed(self):
        pass

    def getRightSideDistTraveled(self):
        """
        Returns the right motor's distance traveled in inches
        """
        self.rightDistInch = (self.rightMotor.getPosition(0, positionUnits.kRotations) / self.gearRatio) * self.wheelCircumference
        if self.rightSideSensorInverted:
            return -1 * self.rightDistInch# / 12
        else:
            return self.rightDistInch

    def getLeftSideDistTraveled(self):
        """
        Returns the left motor's distance traveled in inches
        """
        self.leftDistInch = (self.leftMotor.getPosition(0, positionUnits.kRotations) / self.gearRatio) * self.wheelCircumference
        if self.leftSideSensorInverted:
            return -1 * self.leftDistInch# / 12
        else:
            return self.leftDistInch

    def getEstTotalDistTraveled(self):
        self.smartDashTable.putNumber("Estimated Encoder Distance since enable", (self.getLeftSideDistTraveled() + self.getRightSideDistTraveled()) / 2)
        return (self.getLeftSideDistTraveled() + self.getRightSideDistTraveled()) / 2

    def resetDistTraveled(self):
        self.leftMotor.resetPosition()
        self.rightMotor.resetPosition()

    def resetLeftDistTraveled(self):
        self.leftMotor.resetPosition()

    def resetRightDistTraveled(self):
        self.rightMotor.resetPosition()

    def execute(self):
        if self.controlMode == ControlMode.kTankDrive:
            self.driveTrain.tankDrive(self.tankLeftSpeed, self.tankRightSpeed, False)

        elif self.controlMode == ControlMode.kArcadeDrive:
            self.driveTrain.arcadeDrive(self.arcadeSpeed, self.arcadeRotation, False)
