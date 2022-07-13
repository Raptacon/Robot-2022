from utils.motorHelper import WPI_TalonFXFeedback
import ctre
import logging as log
from networktables import NetworkTables


from magicbot import tunable, feedback


class DriveTrain():
    compatString = ["doof","teapot","greenChassis"]
    # Note - The way we will want to do this will be to give this component motor description dictionaries from robotmap and then creating the motors with motorhelper. After that, we simply call wpilib' differential drive
    motors_driveTrain: dict
    driveMotorsMultiplier = tunable(.5)
    creeperMotorsMultiplier = tunable(.25)

    smartDashTable = NetworkTables.getTable("SmartDashboard")

    def setup(self):
        self.motorSpeedInfo = {}
        self.creeperMode = False
        log.info("DriveTrain setup completed")

    def setBraking(self, braking:bool):
        """
        This isn't incorporated into the handler
        (I'm not sure if it should be)
        """
        if braking:
            for motor in self.motors_driveTrain.keys():
                if type(self.motors_driveTrain[motor]) == WPI_TalonFXFeedback:
                    self.motors_driveTrain[motor].setNeutralMode(ctre.NeutralMode.Brake)
        else:
            for motor in self.motors_driveTrain.keys():
                if type(self.motors_driveTrain[motor]) == WPI_TalonFXFeedback:
                    self.motors_driveTrain[motor].setNeutralMode(ctre.NeutralMode.Coast)

    def setMotors(self, motorSpeedInfo:dict):
        """
        DO NOT CALL THIS, ONLY THE HANDLER SHOULD HAVE CONTROL

        Accepts motorSpeedInfo, a dictionary of motor names and speeds.
        """
        self.motorSpeedInfo = motorSpeedInfo

    def getSpecificMotor(self, motorName):
        """
        returns object for motorName
        if no object exists, returns nothing
        """
        try:
            return self.motors_driveTrain[motorName].get()
        except:
            return

    def enableCreeperMode(self):
        """when left bumper is pressed, it sets the driveMotorsMultiplier to .25"""
        if self.creeperMode:
            return
        self.prevMultiplier = self.driveMotorsMultiplier
        self.driveMotorsMultiplier = self.creeperMotorsMultiplier
        self.creeperMode = True

    def disableCreeperMode(self):
        """when left bumper is released, it sets the multiplier back to it's original value"""
        if not self.creeperMode:
            return
        self.driveMotorsMultiplier = self.prevMultiplier
        self.creeperMode = False

    def stop(self):
        self.motorSpeedInfo = {}
        for key in self.motors_driveTrain.keys():
            self.motorSpeedInfo[key] = 0

    def getSpecificMotorDistTraveled(self, motorName):
        """
        Returns a specific motor's distance traveled
        (Only works with Falcon 500s)
        """
        if type(self.motors_driveTrain[motorName]) == WPI_TalonFXFeedback:
            # self.leftDistInch = (self.motors_driveTrain[motorName].getPosition(0, positionUnits.kRotations) / self.gearRatio) * self.wheelCircumference
            if self.leftSideSensorInverted:
                return -1 * self.leftDistInch
            else:
                return self.leftDistInch
        return 0

    def resetMotorsDistTraveled(self):
        for motor in self.motors_driveTrain.keys():
            if type(self.motors_driveTrain[motor]) == WPI_TalonFXFeedback:
                motor.resetPosition()

    def resetSpecificMotorDistTraveled(self, motorName):
        if type(self.motors_driveTrain[motorName]) == WPI_TalonFXFeedback:
            self.motors_driveTrain[motorName].resetPosition()

    def execute(self):

        # Make sure motors are the same between parameter information and drivetrain
        # then set motors
        speedInfoKeys = sorted(dict(self.motorSpeedInfo).keys())
        driveTrainKeys = sorted(self.motors_driveTrain.keys())
        if speedInfoKeys == driveTrainKeys:
            for key in speedInfoKeys:
                self.motors_driveTrain[key].set(self.motorSpeedInfo[key])
