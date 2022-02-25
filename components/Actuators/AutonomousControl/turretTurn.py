from magicbot import StateMachine, feedback, state, tunable
from components.Actuators.LowLevel.turretThreshold import TurretThreshold
from components.SoftwareControl.speedSections import SpeedSections
from networktables import NetworkTables as networktable
import logging as log

class TurretTurn(StateMachine):
    compatString = ["teapot"]
    motors_turret: dict
    limeTable = networktable.getTable("limelight")
    turretThreshold: TurretThreshold
    speedSections: SpeedSections
    turnAngle = None
    controlMode = "Encoder"
    tolerance = tunable(3)

    def setup(self):
        self.pos = self.turretThreshold.getPosition()

    @feedback
    def getTurning(self):
        """
        If the turret is within tolerance, return True
        """
        offset = self.getOffset()
        if offset != None and abs(self.getOffset()) > self.tolerance:
            return True
        return False

    def setAngle(self, angle):
        """sets angle turret is turning to"""
        if self.turretThreshold.angleCheck(angle) != angle:
            log.error("Turret angle check failed: "+str(self.turretThreshold.angleCheck(angle))+" vs. "+str(angle))
        self.turnAngle = self.turretThreshold.angleCheck(angle)
        self.next_state("turn")

    def setLimeLightControl(self):
        """Determines if turret is using limelight input."""
        self.controlMode = "Limelight"

    def setEncoderControl(self):
        """Determines if turret is using encoder input."""
        self.controlMode = "Encoder"

    @feedback
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
                return None
        elif self.controlMode == "Encoder":
            if self.turnAngle == None:
                return 0
            return self.turnAngle - self.pos


    def setRelAngle(self, relangle):
        """
        Sets target angle (relative to current position)
        """
        self.setAngle(self.pos + relangle)

    @feedback
    def getTargetAngle(self):
        return self.turnAngle

    @state(first = True)
    def idling(self):
        """Stays in this state until started"""
        pass

    @feedback
    def getSpeed(self):
        offset = self.getOffset()
        if offset == None:
            self.setEncoderControl()
            offset = self.getOffset()
        speed = self.speedSections.getSpeed(offset, "TurretTurn")
        if abs(offset) < self.tolerance:
            speed = 0
        return speed

    def setSpeed(self):
        """
        Sets speed of turret based on what angle we are turning to
        """
        speed = self.getSpeed()
        self.turretThreshold.setTurretspeed(speed)

    @state
    def turn(self):
        """
        Starts turning process, if in tolerance it will stop
        """
        self.pos = self.turretThreshold.getPosition()
        self.setSpeed()
        self.next_state("turn")
