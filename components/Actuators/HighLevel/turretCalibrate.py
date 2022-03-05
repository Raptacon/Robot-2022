from magicbot import StateMachine, feedback, state
from rev import SparkMaxLimitSwitch
from components.Actuators.LowLevel.turretThreshold import TurretThreshold
import logging as log
from networktables import NetworkTables as networktable
import logging as log
class CalibrateTurret(StateMachine):
    compatString = ["teapot"]
    turretThreshold: TurretThreshold
    limitTable = networktable.getTable("SmartDashboard")
<<<<<<< HEAD
    # @state(first = True)
    # def testCalibrate(self):
    #     log.error("its alive")

    @state(first = True)
    def findRightdeadzone(self):
        log.error("REEEE")
        self.turretThreshold.setCalibrating(True)
        if self.getRightClicked():
            self.limitR = self.turretThreshold.getPosition()
            self.next_state('findLeftdeadzone')
        else:
            self.turretThreshold.setTurretspeed(self.turretThreshold.calibSpeed)
            self.next_state("findRightdeadzone")
=======
    limitL = None
    limitR = None
>>>>>>> d108ea9107385b3d015b083655049abf6d858bc5

    def setup(self):
        turretMotor = self.turretThreshold.turretMotor
        self.forwardLimitSwitch = turretMotor.getForwardLimitSwitch(SparkMaxLimitSwitch.Type.kNormallyOpen)
        self.reverseLimitSwitch = turretMotor.getReverseLimitSwitch(SparkMaxLimitSwitch.Type.kNormallyOpen)

    @feedback
    def getLeftClicked(self):
        return self.reverseLimitSwitch.get()

    @feedback
    def getRightClicked(self):
        return self.forwardLimitSwitch.get()


    @state
    def findLeftdeadzone(self):
        if self.getLeftClicked():
            self.limitL = self.turretThreshold.getPosition()
            self.foundDeadzones()
        else:
            self.turretThreshold.setTurretspeed(-1*self.turretThreshold.calibSpeed)
            self.next_state("findLeftdeadzone")

    def foundDeadzones(self):
        self.turretThreshold.setCalibrating(False)
        self.turretThreshold.setTurretspeed(0)
        self.turretThreshold.setDeadzones(self.limitL, self.limitR)
        self.limitTable.putNumber("Left Limit", self.limitL)
        self.limitTable.putNumber("Right Limit", self.limitR)
        self.done()

    def checkSwitches(self):
        if self.getLeftClicked():
            self.limitL = self.turretThreshold.getPosition()
        if self.getRightClicked():
            self.limitR = self.turretThreshold.getPosition()

    def execute(self):
        self.checkSwitches()
        if self.limitL != None and self.limitR != None:
            self.foundDeadzones()
            self.limitL = None
            self.limitR = None
