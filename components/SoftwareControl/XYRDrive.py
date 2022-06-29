from components.SoftwareControl.AxesXYR import AxesXYR
from components.Actuators.HighLevel.driveTrainHandler import DriveTrainHandler
import math

MotorSpeed = []
class transform:
    def transform(self,x, y, r):
        return MotorSpeed()
class TankDrive(transform):
    driveTrainHandler: DriveTrainHandler
    lmotor = 0
    rmotor = 0
    def MotorDrive(self,x,y,r):
        if y >= 0:
            if r >= 0:  # I quadrant
                self.lmotor = y
                self.rmotor = r
            else:            # II quadrant
                self.lmotor = r
                self.rmotor = y
        else:
            if r >= 0:  # IV quadrant
                self.lmotor = 1 + y
                self.rmotor = r
            else:            # III quadrant
                self.lmotor = r
                self.rmotor = 1 + y
        self.lmotor2 = self.lmotor
        self.rmotor2 = self.rmotor
        return MotorSpeed(self.lmotor, self.rmotor)
    
class SwerveDrive(transform):
    L = 30
    W = 30

    def MotorDrive (self, x, y, r):
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
        return MotorSpeed(backRightSpeed, backLeftSpeed, frontRightSpeed, frontLeftSpeed,
                          backRightAngle, backLeftAngle, frontRightAngle, frontLeftAngle)

class XYRDrive:
    transformDict = {"Tank":TankDrive, "Swerve":SwerveDrive}
    def xyrdrive(self, transformKey:str, x, y, r):

        if transformKey in self.transformDict.keys():
            transformer = self.transformDict[transformKey]
            return transformer.transform(x,y,r)