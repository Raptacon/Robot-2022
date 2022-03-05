from magicbot import StateMachine, feedback, state
from rev import SparkMaxLimitSwitch

from components.Actuators.AutonomousControl.turretTurn import TurretTurn
from components.Actuators.LowLevel.turretThreshold import TurretThreshold
from networktables import NetworkTables as networktable
class CalibrateTurret(StateMachine):
    compatString = ["greenChassis", "teapot"]
    turretTurn: TurretTurn
    turretThreshold: TurretThreshold
    limitTable = networktable.getTable("SmartDashboard")
    offset = 206
    limitL = None
    limitR = None

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


    @state(first = True)
    def findRightdeadzone(self):
        self.turretThreshold.setCalibrating(True)
        if self.getRightClicked():
            self.limitR = self.turretThreshold.getPosition()
            self.limitL = self.limitR - self.offset
            self.next_state('foundDeadzones')
        else:
            self.turretThreshold.setTurretspeed(self.turretThreshold.calibSpeed)
            self.next_state("findRightdeadzone")

    @state
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
