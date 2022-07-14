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

        return {Tank.FrontLeft:lmotor, Tank.BackLeft:lmotor, Tank.FrontRight:rmotor, Tank.BackRight:rmotor}

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
        return {Swerve.BackRight:backRightSpeed, Swerve.BackLeft:backLeftSpeed, Swerve.FrontRight:frontRightSpeed, Swerve.FrontLeft:frontLeftSpeed,
                Swerve.BackRightRotation:backRightAngle, Swerve.BackLeftRotation:backLeftAngle, Swerve.FrontRightRotation:frontRightAngle, Swerve.FrontLeftRotation:frontLeftAngle}

class XYRDrive:
    driveTrainType: str
    TankDrive = TankDrive()
    SwerveDrive = SwerveDrive()

    def __init__(self):
        self.transformDict = {"Tank":self.TankDrive, "Swerve":self.SwerveDrive}
    def xyrdrive(self, requestSource, vector:XYRVector):
        """
        Pass in self as requestSource
        """

        transformKey = self.DriveTrainType

        if transformKey in self.transformDict.keys():
            transformer = self.transformDict[transformKey]
            DriveTrainHandler.setDriveTrain(requestSource, transformer.MotorDrive(vector.getX(), vector.getY(), vector.getR()))
        else:
            log.error("Unrecognized drivetrain type "+str(self.DriveTrainType))

    def execute(self):
        pass
