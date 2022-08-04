import time
from wpimath.geometry import Pose2d
from wpimath.geometry import Rotation2d
from wpimath.geometry import Translation2d

class Odometry():
    GyroAngle = 0
    Kinamatics = 0
    pose2d = Pose2d(Translation2d(x=0.000000, y=0.000000), Rotation2d(0.000000))
    def Odometry(self):
        self.InitialPose = self.pose2d()
    def getPosition(self):
        """
        Returns Position of the Robot
        """
        return self.pose2d()
    def resetPosition(self):
        """
        Resets Robots Postion on the feild
        """
        self.previousAngle = self.pose2d.rotation()
        self.gryroOffset = self.pose2d.rotation() - self.GyroAngle
    def Update(self):
        pass
    def UpdateWithTime(self):
        """
        Updates Postion of the Robot on the feild using time
        """
        pass