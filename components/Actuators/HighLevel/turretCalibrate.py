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
    offset = 206
    limitL = None
    limitR = None
    useMotor = False

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

    def setup(self):
        turretMotor = self.turretThreshold.turretMotor
        self.forwardLimitSwitch = turretMotor.getForwardLimitSwitch(SparkMaxLimitSwitch.Type.kNormallyOpen)
        self.reverseLimitSwitch = turretMotor.getReverseLimitSwitch(SparkMaxLimitSwitch.Type.kNormallyOpen)

    def setUseMotor(self, motor:bool):
        """
        Determines whether we use motor or not during calibration.
        """
        self.useMotor = motor

    @feedback
    def getLeftClicked(self):
        return self.reverseLimitSwitch.get()

    @feedback
    def getRightClicked(self):
        return self.forwardLimitSwitch.get()

    @state(first = True)
    def findRightdeadzone(self):
        if self.getRightClicked():
            self.limitR = self.turretThreshold.getPosition()
            self.limitL = self.limitR - self.offset
            self.foundDeadzones()
        else:
            if self.useMotor:
                self.turretThreshold.setTurretspeed(self.turretThreshold.calibSpeed)
                self.turretThreshold.setCalibrating(True)
            self.next_state("findRightdeadzone")

    def foundDeadzones(self):
        self.turretThreshold.setCalibrating(False)
        self.turretThreshold.setTurretspeed(0)
        self.turretThreshold.setDeadzones(self.limitL, self.limitR)
        self.limitTable.putNumber("Left Limit", self.limitL)
        self.limitTable.putNumber("Right Limit", self.limitR)
        self.done()
