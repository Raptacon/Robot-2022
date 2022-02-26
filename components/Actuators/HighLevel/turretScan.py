from magicbot import StateMachine, state, feedback
from components.Actuators.AutonomousControl.turretTurn import TurretTurn
from components.Actuators.LowLevel.turretThreshold import TurretThreshold
from components.SoftwareControl.speedSections import SpeedSections
from networktables import NetworkTables as networktable

# TODO: start scanning
# TODO: Return scan result

class TurretScan (StateMachine):
    compatString = ["teapot", "greenChassis"]
    limeTable = networktable.getTable("limelight")
    turretTurn: TurretTurn
    speedSections: SpeedSections
    tv = 0
    turretThreshold: TurretThreshold
    stateTurn = "turnRight"
     
    @state(first=True)
    def check(self):
        """
        Like an idling state, makes sure that limelight has a target.
        If it doesn't, transitions to scanning between the left limit and right limit
        until the limelight has a target.
        """
        if self.turretThreshold.calibrated:
            if self.hasTarget() == False:
                self.turretTurn.setEncoderControl()
                self.next_state("turnLeft")
            else:
                self.turretTurn.setLimeLightControl()
                self.next_state("check")

    @state
    def turnLeft(self):
        if self.hasTarget() == False:
            self.turretTurn.setAngle(self.turretThreshold.leftLim + 7)
            self.stateTurn = "turnRight"
            self.next_state("wait")
        else:
            self.next_state("check")

    @state
    def wait(self):
        self.turretTurn.setEncoderControl()
        turn = self.turretTurn.getTurning()

        if self.hasTarget():
            self.next_state("foundTarget")
        elif turn:
            self.next_state("wait")
        else:
            self.next_state(self.stateTurn)

    @state
    def turnRight(self):
        if self.hasTarget() == False:
            self.turretTurn.setAngle(self.turretThreshold.rightLim - 7)
            self.stateTurn = "turnLeft"
            self.next_state("wait")
        else:
            self.next_state("check")

    @state
    def foundTarget(self):
        self.turretTurn.setLimeLightControl()
        self.next_state("check")

    @feedback
    def hasTarget(self):
        self.tv = self.limeTable.getNumber("tv", None)
        if self.tv == 1:
            return True
        else:
            return False

