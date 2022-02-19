
from magicbot import StateMachine, state
from wpilib import SmartDashboard, _wpilib
from components.Actuators.AutonomousControl.turretTurn import TurretTurn
from components.Actuators.LowLevel.turretThreshold import TurretThreshold
from networktables import NetworkTables as networktable
class CalibrateTurret(StateMachine):
    compatString = ["doof", "greenChassis", "newBot"]
    turretTurn: TurretTurn
    turretThreshold: TurretThreshold
    const_turnAngle = 5
    limitTable = networktable.getTable("SmartDashboard")
    wpilib: _wpilib

    def initLimswitches(self):
        self.forwardLimitSwitch = self.wpilib.DigitalInput(1)
        self.reverseLimitSwitch = self.wpilib.DigitalInput(2)

    def getLClicked(self):
        self.forwardLimitSwitch.get()

    def getRClicked(self):
        self.reverseLimitSwitch.get()


    @state(first = True)
    def findRightdeadzone(self):
        self.turretThreshold.setCalibrating(True)
        if self.getRClicked():
            self.limitR = self.turretThreshold.getPosition()
            self.next_state('findLeftdeadzone')
        else:
            self.turretTurn.engage()
            self.turretTurn.setRelAngle(self.const_turnAngle)
            self.next_state("findRightdeadzone")


    @state
    def findLeftdeadzone(self):
        if self.getLClicked():
            self.limitL = self.turretThreshold.getPosition()
            self.next_state('foundDeadzones')
        else:
            self.turretTurn.engage()
            self.turretTurn.setRelAngle(-1*self.const_turnAngle)
            self.next_state("findLeftdeadzone")

    @state
    def foundDeadzones(self):
        self.turretThreshold.setCalibrating(False)
        self.turretThreshold.setDeadzones(self.limitL, self.limitR)
        self.limitTable.putNumber("Left Limit", self.limitL)
        self.limitTable.putNumber("Right Limit", self.limitR)
