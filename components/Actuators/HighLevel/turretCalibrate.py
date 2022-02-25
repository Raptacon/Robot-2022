from magicbot import StateMachine, feedback, state
from rev import SparkMaxLimitSwitch

from components.Actuators.AutonomousControl.turretTurn import TurretTurn
from components.Actuators.LowLevel.turretThreshold import TurretThreshold
from networktables import NetworkTables as networktable
class CalibrateTurret(StateMachine):
    compatString = ["greenChassis", "teapot"]
    turretTurn: TurretTurn
    turretThreshold: TurretThreshold
    const_turnAngle = 7
    limitTable = networktable.getTable("SmartDashboard")

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
            self.next_state('findLeftdeadzone')
        else:
            self.turretTurn.setRelAngle(self.const_turnAngle)
            self.next_state("findRightdeadzone")


    @state
    def findLeftdeadzone(self):
        if self.getLeftClicked():
            self.limitL = self.turretThreshold.getPosition()
            self.next_state('foundDeadzones')
        else:
            self.turretTurn.setRelAngle(-1*self.const_turnAngle)
            self.next_state("findLeftdeadzone")

    @state
    def foundDeadzones(self):
        self.turretThreshold.setCalibrating(False)
        self.turretTurn.setRelAngle(0)
        self.turretThreshold.setDeadzones(self.limitL, self.limitR)
        self.limitTable.putNumber("Left Limit", self.limitL)
        self.limitTable.putNumber("Right Limit", self.limitR)
        self.done()
