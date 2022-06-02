from components.SoftwareControl.AxesXYR import AxesXYR
from components.Actuators.HighLevel.driveTrainHandler import DriveTrainHandler
class XYRDrive:
    mode = 0
    transformDict = {"Tank", "Arcade", "Swerve"}
    def xyrdrive(self):
        if self.transformDict[self.mode] == 'Tank':
            tank
        elif self.transformDict[self.mode] == 'Arcade':
            arcade
        elif self.transformDict[self.mode] == 'Swerve':
            swerve
            
class tank:
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

class arcade:
    pass
    
class swerve:
    pass