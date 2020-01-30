import wpilib
import team3200.motorHelper as motorHelper

class DriveTrain: #Note - The way we will want to do this will be to give this component motor description dictionaries from robotmap and then creating the motors with motorhelper. After that, we simply call wpilib' differential drive
    driveTrain_motorsList: dict

    def enable(self):
        leftMotorDescs = self.driveTrain_motorsList['left']
        rightMotorDescs = self.driveTrain_motorsList['right']

        self.leftMotor = motorHelper(leftMotorDescs)
        self.rightMotor = motorHelper(rightMotorDescs)

        print("{}".format(leftMotorDescs))
        print("{}".format(rightMotorDescs))

        self.driveTrain = wpilib.drive.DifferentialDrive(self.leftMotor, self.rightMotor)

    def getLeft(self):
        return self.leftMotor.get()

    def getRight(self):
        return self.rightMotor.get()

    def isStopping(self):
        pass

    def setTank(self, speed, rotation):
        self.driveTrain.tankDrive(leftSide, rightSide, False)
    
    def setArcade(self, leftSpeed, rightSpeed):
        self.driveTrain.arcadeDrive(speed, rot, False)

    def stop(self, coast = False):
        pass

    def getMeasuredSpeed(self):
        pass

    def execute(self):
        print("{}".format(self.driveTrain_motorsList['left']))
        print("{}".format(self.driveTrain_motorsList['right']))
    
