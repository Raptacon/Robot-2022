import wpilib

class driveTrain: #Note - The way we will want to do this will be to give this component motor description dictionaries from robotmap and then creating the motors with motorhelper. After that, we simply call wpilib' differential drive
    drive_motors: DriveMotors    

    def enable():

    def getLeft():
        pass

    def getRight():
        pass

    def isStopping():
        pass

    def setArcade(speed, rotation):
        pass
    
    def setTank(leftSpeed, rightSpeed):
        pass

    def stop(coast = False):
        pass

    def getMeasuredSpeed():
        pass

    def execute():
        print("{}".format(drive_motor['left'])
        print("{}".format(drive_motor['right']))
    
