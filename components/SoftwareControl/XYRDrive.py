from SoftwareControl import AxesXYR
from components.Actuators.LowLevel.driveTrain import ControlMode

class XYRDrive:
    mode = ControlMode
    def xyrdrive(self):
        if self.mode == 'kTankDrive':
            self.tank()
        elif self.mode == 'kArcadeDrive':
            self.arcade()
        elif self.mode == 'kSwerveDrive':
            self.swerve()
            
    def tank(self):
        pass
    
    def arcade(self):
        pass
    
    def swerve(self):
        pass