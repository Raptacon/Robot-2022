from magicbot import StateMachine, feedback, state
from rev import SparkMaxLimitSwitch

from components.Actuators.AutonomousControl.turretTurn import TurretTurn
from components.Actuators.LowLevel.turretThreshold import TurretThreshold
from networktables import NetworkTables as networktable
class CalibrateTurret(StateMachine):
    compatString = ["greenChassis", "teapot", "minibot"]
    turretTurn: TurretTurn
    turretThreshold: TurretThreshold
    const_turnAngle = 5
    limitTable = networktable.getTable("SmartDashboard")

    def setup(self):
        turretMotor = self.turretThreshold.turretMotor
        self.forwardLimitSwitch = turretMotor.getForwardLimitSwitch(SparkMaxLimitSwitch.Type.kNormallyOpen)
        self.reverseLimitSwitch = turretMotor.getReverseLimitSwitch(SparkMaxLimitSwitch.Type.kNormallyOpen)

    @feedback
    def getLClicked(self):
        return self.forwardLimitSwitch.get()

    @feedback
    def getRClicked(self):
        return self.reverseLimitSwitch.get()


    @state(first = True)
    def findRightdeadzone(self):
        self.turretThreshold.setCalibrating(True)
        if self.getRClicked():
            self.limitR = self.turretThreshold.getPosition()
            self.next_state('findLeftdeadzone')
        else:
            self.turretTurn.engage()
            self.turretTurn.setRelAngle(-1*self.const_turnAngle)
            self.next_state("findRightdeadzone")


    @state
    def findLeftdeadzone(self):
        if self.getLClicked():
            self.limitL = self.turretThreshold.getPosition()
            self.next_state('foundDeadzones')
        else:
            self.turretTurn.engage()
            self.turretTurn.setRelAngle(self.const_turnAngle)
            self.next_state("findLeftdeadzone")

    @state
    def foundDeadzones(self):
        self.turretThreshold.setCalibrating(False)
        self.turretTurn.setRelAngle(0)
        self.turretThreshold.setDeadzones(self.limitL, self.limitR)
        self.limitTable.putNumber("Left Limit", self.limitL)
        self.limitTable.putNumber("Right Limit", self.limitR)
