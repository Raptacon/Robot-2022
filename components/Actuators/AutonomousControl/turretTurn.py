from magicbot import StateMachine, state, tunable
from components.Actuators.LowLevel.turretThreshold import TurretThreshold
from components.SoftwareControl.speedSections import SpeedSections
from networktables import NetworkTables as networktable
import logging as log

class TurretTurn(StateMachine):
    compatString = ["teapot", "minibot"]
    motors_turret: dict
    limeTable = networktable.getTable("limelight")
    turretThreshold: TurretThreshold
    speedSections: SpeedSections
    turnAngle = None
    controlMode = None
    tolerance = tunable(3)

    def setup(self):
        self.pos = self.turretThreshold.getPosition()

    def setAngle(self, angle):
        """sets angle turret is turning to"""
        if self.turretThreshold.angleCheck(angle) != angle:
            log.error("Turret angle check failed")
        self.turnAngle = self.turretThreshold.angleCheck(angle)
        self.next_state("turn")

    def setLimeLightControl(self):
        """Determines if turret is using limelight input."""
        self.controlMode = "Limelight"

    def setEncoderControl(self):
        """Determines if turret is using encoder input."""
        self.controlMode = "Encoder"

    def getOffset(self):
        """
        Gives difference between current position and target angle.
        Based on self.controlMode - if in limelight control and it doesn't
        have a target returns false
        """
        if self.controlMode == "Limelight":
            limePosition = self.limeTable.getNumber("tx", -50)
            if limePosition != -50:
                return limePosition
            else:
                log.error("Limelight missing target")
                return False
        elif self.controlMode == "Encoder":
            return self.turnAngle - self.pos


    def setRelAngle(self, relangle):
        """
        Sets target angle (relative to current position)
        """
        self.setAngle(self.pos + relangle)

    @state(first = True)
    def idling(self):
        """Stays in this state until started"""
        pass

    def setSpeed(self):
        """
        Sets speed of turret based on what angle we are turning to
        """
        offset = self.getOffset()
        if offset != True:
            self.setEncoderControl()
            offset = self.getOffset()
        speed = self.speedSections.getSpeed(offset, "TurretTurn")
        if abs(offset) < self.tolerance:
            speed = 0
        self.turretThreshold.setTurretspeed(speed)

    @state
    def turn(self):
        """
        Starts turning process, if in tolerance it will stop
        """
        self.setSpeed()
        self.next_state("turn")
