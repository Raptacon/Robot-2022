import wpilib

class DriveTrain: #Note - The way we will want to do this will be to give this component motor description dictionaries from robotmap and then creating the motors with motorhelper. After that, we simply call wpilib' differential drive
    driveTrain_motors: dict

    def enable(self):
        print("{}".format(self.driveTrain_motors['left']))
        print("{}".format(self.driveTrain_motors['right']))
        pass

    def getLeft(self):
        pass

    def getRight(self):
        pass

    def isStopping(self):
        pass

    def setArcade(self, speed, rotation):
        pass
    
    def setTank(self, leftSpeed, rightSpeed):
        pass

    def stop(self, coast = False):
        pass

    def getMeasuredSpeed(self):
        pass

    def execute(self):
        print("{}".format(self.driveTrain_motors['left']))
        print("{}".format(self.driveTrain_motors['right']))
    
