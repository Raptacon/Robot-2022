import enum
from utils.UnitEnums import positionUnits
from utils.motorHelper import WPI_TalonFXFeedback
from enum import Enum, auto
import ctre
import math
import wpilib.drive
import logging as log
from networktables import NetworkTables
from SoftwareControl.XYRDrive import SwerveDrive


from magicbot import tunable, feedback
class ControlMode(Enum):
    """
    Drive Train Control Modes
    """
    kArcadeDrive = auto()
    kTankDrive = auto()
    kDisabled = auto()
    kSwerveDrive = auto()
    MotorEnum = auto()

class findMotorEnum(enum):
    motorListEnum = ["leftFrontSwerve", "rightFrontSwerve", "leftBackSwerve", "rightBackSwerve"]



class Tank(Enum):
    """
    Tank Motors Keys
    """
    numMotors = 4
    FrontLeft = "FrontLeftTankMotor"
    FrontRight = "FrontRightTankMotor"
    BackLeft = "BackLeftTankMotor"
    BackRight = "BackLeftTankMotor"

class Swerve(Enum):
    """
    Swerve Motors Keys
    """
    numMotors = 8
    FrontLeft = "FrontLeftSwerveMotor"
    FrontRight = "FrontRightSwerveMotor"
    BackLeft = "BackLeftSwerveMotor"
    BackRight = "BackLeftSwerveMotor"
    FrontLeftRotation = "FrontLeftRotationMotor"
    FrontRightRotation = "FrontRightRotationMotor"
    BackLeftRotation = "BackLeftRotationMotor"
    BackRightRotation = "BackLeftRotationMotor"

class DriveTrain():
    compatString = ["doof","teapot","greenChassis"]
    # Note - The way we will want to do this will be to give this component motor description dictionaries from robotmap and then creating the motors with motorhelper. After that, we simply call wpilib' differential drive
    motors_driveTrain: dict
    motorSpeeds:list
    driveMotorsMultiplier = tunable(.5)
    creeperMotorsMultiplier = tunable(.25)
    # gearRatio = 10
    # wheelCircumference = 6 * math.pi
    swervedrive = SwerveDrive

    smartDashTable = NetworkTables.getTable("SmartDashboard")

    # Encoder variables
    # leftSideSensorInverted = True
    # rightSideSensorInverted = False

    def setup(self):
        self.tankLeftSpeed = 0
        self.tankRightSpeed = 0
        self.arcadeSpeed = 0
        self.arcadeRotation = 0
        self.creeperMode = False
        self.controlMode = ControlMode.kDisabled
        self.driveTrain = wpilib.drive.DifferentialDrive(self.motors_driveTrain[0], self.motors_driveTrain[1])
        log.info("DriveTrain setup completed")



    def setBraking(self, braking:bool):
        """
        This isn't incorporated into the handler
        (I'm not sure if it should be)
        """
        if braking:
            for motor in self.motors_driveTrain:
                motor.setNeutralMode(ctre.NeutralMode.Brake)
        else:
            for motor in self.motors_driveTrain:
                motor.setNeutralMode(ctre.NeutralMode.Coast)


    def setSpeeds(self):
        for i in range(len(self.motors_driveTrain)):
            self.motors_driveTrain[i-1].setspeed(self.motorSpeeds[i-1])

    def setMotors(self, motorSpeedInfo:dict):
        self.motorSpeedInfo = motorSpeedInfo


    def getMotors(self):
        for motor in self.motors_driveTrain:
            return motor.get()

    def getSpecificMotor(self, motorPosition):
        return self.motors_driveTrain[motorPosition].get()

    def isStopping(self):
        pass

    # def setTank(self, leftSpeed, rightSpeed):
    #     """
    #     THIS IS CONTROLLED BY THE HANDLER
    #     DO NOT CALL THIS
    #     """
    #     self.controlMode = ControlMode.kTankDrive
    #     self.tankLeftSpeed = leftSpeed
    #     self.tankRightSpeed = rightSpeed

    # def setArcade(self, speed, rotation):
    #     """
    #     THIS IS CONTROLLED BY THE HANDLER
    #     DO NOT CALL THIS
    #     """
    #     self.controlMode = ControlMode.kArcadeDrive
    #     self.arcadeSpeed = speed
    #     self.arcadeRotation = rotation

    # def setSwerve(self, )

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

    # def getMotorsDistTraveled(self):
    #     """
    #     Returns the right motor's distance traveled in inches
    #     """
    #     for motor in self.motors_driveTrain:
    #         self.rightDistInch = (motor.getPosition(0, positionUnits.kRotations) / self.gearRatio) * self.wheelCircumference
    #         if self.rightSideSensorInverted:
    #             return -1 * self.rightDistInch# / 12
    #         else:
    #             return self.rightDistInch


    def getSpecificMotorDistTraveled(self, motorName):
        """
        Returns a specific motor's distance traveled
        (Only works with Falcon 500s)
        """
        if type(self.motors_driveTrain[motorName]) == WPI_TalonFXFeedback:
            # self.leftDistInch = (self.motors_driveTrain[motorName].getPosition(0, positionUnits.kRotations) / self.gearRatio) * self.wheelCircumference
            if self.leftSideSensorInverted:
                return -1 * self.leftDistInch
            else:
                return self.leftDistInch
        return 0

    # @feedback
    # def getEstTotalDistTraveled(self):
    #     """"
    #     Return an estimate of total distance traveled in inches
    #     """
    #     self.smartDashTable.putNumber("Estimated Encoder Distance since enable", self.getMotorsDistTraveled() / self.motors_driveTrain.__len__)
    #     return self.getMotorsDistTraveled() / self.motors_driveTrain.__len__

    def resetMotorsDistTraveled(self):
        for motor in self.motors_driveTrain:
            if type(motor) == WPI_TalonFXFeedback:
                motor.resetPosition()

    def resetSpecificMotorDistTraveled(self, motorPosition):
        if type(motor) == WPI_TalonFXFeedback:
            self.motors_driveTrain[motorPosition].resetPosition()

    def execute(self):
        # if self.controlMode == ControlMode.kTankDrive:
        #     self.driveTrain.tankDrive(self.tankLeftSpeed, self.tankRightSpeed, False)

        # elif self.controlMode == ControlMode.kArcadeDrive:
        #     self.driveTrain.arcadeDrive(self.arcadeSpeed, self.arcadeRotation, False)
