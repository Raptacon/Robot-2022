from SoftwareControl import AxesXYR
from components.Actuators.LowLevel.driveTrain import ControlMode

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
    pass
    
class arcade:
    pass
    
class swerve:
    pass