from components.SoftwareControl.AxesXYR import AxesXYR
from components.Actuators.HighLevel.driveTrainHandler import DriveTrainHandler
import math

class motorGroup:
    TL = 0
    BL = 0
    TR = 0
    BR = 0
    def motorgroup(self):
        motors = {{self.TL,self.BL},{self.TR,self.BR}}
        return motors
class tank(motorGroup):
    driveTrainHandler: DriveTrainHandler
    lmotor = motorGroup[0]
    rmotor = motorGroup[1]
    def tankdrive(self,x,y,r):
        if y >= 0:
            if r >= 0:  # I quadrant
                for z in self.lmotor:
                    z = y
                for w in self.rmotor:
                    w = r
            else:            # II quadrant
                for z in self.lmotor:
                    z = r
                for w in self.rmotor:
                    w = y
        else:
            if r >= 0:  # IV quadrant
                for z in self.lmotor:
                    z = y + 1
                for w in self.rmotor:
                    w = r
            else:            # III quadrant
                for z in self.lmotor:
                    z = r
                for w in self.rmotor:
                    w = 1 + y

class arcade:
    driveTrainHandler: DriveTrainHandler
    lmotor = 0
    rmotor = 0
    def tankdrive(self,x,y,r):
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
    
class swerve:
    L = 30
    W = 30

    def rec (self, x, y, r):
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

class XYRDrive:
    mode = 0
    transformDict = {"Tank":tank, "Arcade":arcade, "Swerve":swerve}

    def xyrdrive(self, transformKey:str):
        if transformKey in self.transformDict.keys():
            transformer = self.transformDict[transformKey]