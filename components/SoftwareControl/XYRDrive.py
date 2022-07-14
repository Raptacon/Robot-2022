from utils.XYRVector import XYRVector
from utils.motorEnums import Tank, Swerve
from utils.configMapper import ConfigMapper
import logging as log
from components.Actuators.HighLevel.driveTrainHandler import DriveTrainHandler
import math

MotorSpeed = []

class TankDrive:
    lmotor = 0
    rmotor = 0

    def MotorDrive(self, x,y,r):
        if y >= 0:
            if r >= 0:  # I quadrant
                lmotor = y
                rmotor = r
            else:            # II quadrant
                lmotor = r
                rmotor = y
        else:
            if r >= 0:  # IV quadrant
                lmotor = 1 + y
                rmotor = r
            else:            # III quadrant
                lmotor = r
                rmotor = 1 + y

        return {Tank.FrontLeft.value : lmotor,
                Tank.BackLeft.value : lmotor,
                Tank.BackRight.value : rmotor,
                Tank.FrontRight.value : rmotor}

class SwerveDrive:
    L = 30
    W = 30

    def MotorDrive(self, x,y,r):
        ratio = math.sqrt ((self.L * self.L) + (self.W * self.W))
        y *= -1

        a = x - r * (self.L / ratio)
        b = x + r * (self.L / ratio)
        c = y - r * (self.W / ratio)
        d = y + r * (self.W / ratio)

        backRightSpeed = math.sqrt ((a * a) + (d * d))
        backLeftSpeed = math.sqrt ((a * a) + (c * c))
        frontRightSpeed = math.sqrt ((b * b) + (d * d))
        frontLeftSpeed = math.sqrt ((b * b) + (c * c))

        backRightAngle = math.atan2 (a, d) / math.pi
        backLeftAngle = math.atan2 (a, c) / math.pi
        frontRightAngle = math.atan2 (b, d) / math.pi
        frontLeftAngle = math.atan2 (b, c) / math.pi
        return {Swerve.BackRight.value:backRightSpeed,
                Swerve.BackLeft.value:backLeftSpeed,
                Swerve.FrontRight.value:frontRightSpeed,
                Swerve.FrontLeft.value:frontLeftSpeed,
                Swerve.BackRightRotation.value:backRightAngle,
                Swerve.BackLeftRotation.value:backLeftAngle,
                Swerve.FrontRightRotation.value:frontRightAngle,
                Swerve.FrontLeftRotation.value:frontLeftAngle}

class XYRDrive:
    driveTrainType: str
    driveTrainHandler: DriveTrainHandler
    TankDrive = TankDrive()
    SwerveDrive = SwerveDrive()

    def __init__(self):
        self.transformDict = {"Tank":self.TankDrive, "Swerve":self.SwerveDrive}
    def xyrdrive(self, requestSource, vector:XYRVector):
        """
        Pass in self as requestSource
        """

        transformKey = self.driveTrainType

        if transformKey in self.transformDict.keys():
            transformer = self.transformDict[transformKey]
            self.driveTrainHandler.setDriveTrain(requestSource, transformer.MotorDrive(vector.getX(), vector.getY(), vector.getR()))
        else:
            log.error("Unrecognized drivetrain type "+str(self.driveTrainType))

    def execute(self):
        pass
