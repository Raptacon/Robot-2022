from magicbot import StateMachine, state, tunable
from components.Actuators.LowLevel.turretThreshold import TurretThreshold
from components.SoftwareControl.speedSections import SpeedSections
from networktables import NetworkTable, NetworkTables as networktable
import logging as log

class TurretTurn(StateMachine):
    compatString = ["doof", "greenChassis"]
    motors_turret: dict
    limeTable = networktable.getTable("limelight")
    turretThreshold: TurretThreshold
    speedSections: SpeedSections
    turnAngle = None
    tolerance = tunable(0.5)

    def setup(self):
        self.pos = self.turretThreshold.getPosition()

    def setAngle(self, angle):
        """sets angle turret is turning to"""
        self.turnAngle = self.turretThreshold.angleCheck(angle)

    def setLimeLightControl(self):
        """Determines if turret is using limelight input."""
        self.controlMode = "Limelight"
    def setEncoderControl(self):
        """Determines if turret is using encoder input."""
        self.controlMode = "Encoder"
    def getOffset(self):
        """Gives difference between current position and target angle."""
        if self.controlMode == "Limelight":
            limePosition = self.limeTable.getNumber("tx", -50)
            if limePosition != -50:
                return limePosition
            else:
                log.error("Limelight missing target")
                return False
        elif self.controlMode == "Encoder":
            return self.turnAngle - self.pos
        # Figure out if taking input from lime/encoder
        # Get input from lime/encoder
        # Give offset


    def setRelAngle(self, relangle):
        """
        Sets target angle (relative to current position)
        """
        self.turnAngle = self.pos + relangle

    @state(first = True)
    def idling(self):
        """Stays in this state until started"""
        if self.turnAngle != None:
            self.next_state("turn")
        else:
            self.next_state("idling")

    def setSpeed(self):
        """
        Sets speed of turret based on what angle we are turning to
        """
        offset = self.getOffset()
        # Check to see if offset is false
        speed = self.speedSections.getSpeed(offset, "TurretTurn")
        if abs(offset) < self.tolerance:
            speed = 0
        self.turretThreshold.setTurretspeed(speed)

    @state
    def turn(self):
        """
        Starts turning process, if in tolerance it will stop
        """
        self.pos = self.turretThreshold.getPosition()
        self.setSpeed()
        self.next_state("turn")
