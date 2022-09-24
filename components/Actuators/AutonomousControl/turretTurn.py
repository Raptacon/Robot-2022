from magicbot import StateMachine, feedback, state, tunable
from components.Actuators.LowLevel.turretThreshold import TurretThreshold
from components.SoftwareControl.speedSections import SpeedSections
from networktables import NetworkTables as networktable
import logging as log
from enum import Enum, auto

class TurretControlMode(Enum):
    """
    Turret Control Modes
    Encoder
    Limelight
    and Manual
    """
    kEncoder = auto()
    kLimelight = auto()
    kManual = auto()

class TurretTurn(StateMachine):
    compatString = ["teapot"]
    motors_turret: dict
    limeTable = networktable.getTable("limelight")
    turretThreshold: TurretThreshold
    speedSections: SpeedSections
    turnAngle = None
    controlMode = TurretControlMode.kManual
    tolerance = tunable(3)
    manualSpeed = 0
    maxManualSpeed = .7
    minManualSpeed = .22

    def setup(self):
        self.pos = self.turretThreshold.getPosition()

    @feedback
    def getTurning(self):
        """
        If the turret is within tolerance, return True
        """
        if self.getSpeed() != 0:
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
        self.controlMode = TurretControlMode.kLimelight

    def setEncoderControl(self):
        """Determines if turret is using encoder input."""
        self.controlMode = TurretControlMode.kEncoder

    def setManualControl(self):
        """Sets turret to manual input."""
        self.controlMode = TurretControlMode.kManual

    @feedback
    def getOffset(self):
        """
        Gives difference between current position and target angle.
        Based on self.controlMode - if in limelight control and it doesn't
        have a target returns false
        """
        if self.controlMode == TurretControlMode.kLimelight:
            limePosition = self.limeTable.getNumber("tx", -50)
            if limePosition != -50:
                return limePosition
            else:
                log.error("Limelight missing target")
                return None
        elif self.controlMode == TurretControlMode.kEncoder:
            if self.turnAngle == None:
                return 0
            return self.turnAngle - self.pos
        elif self.controlMode == TurretControlMode.kManual:
            return "Manual"

    def setRelAngle(self, relangle):
        """
        Sets target angle (relative to current position)
        """
        self.setAngle(self.pos + relangle)

    @feedback
    def getTargetAngle(self):
        return self.turnAngle

    @feedback
    def getSpeed(self):
        offset = self.getOffset()
        if offset == None:
            self.setEncoderControl()
            offset = self.getOffset()
        elif offset == "Manual":
            return self.manualSpeed
        speed = self.speedSections.getSpeed(offset, "TurretTurn")
        if abs(offset) < self.tolerance:
            speed = 0
        return speed

    def getControlMode(self):
        """
        Returns a TurretControlMode enum
        of Limelight, Manual or Encoder
        depending on the source that the turret is using for input
        """
        return self.controlMode

    def setSpeed(self):
        """
        Sets speed of turret based on what angle we are turning to
        """
        speed = self.getSpeed()
        self.turretThreshold.setTurretspeed(speed)

    def setManualSpeed(self, speed):
        if speed !=0:
            diff = (self.maxManualSpeed- self.minManualSpeed)
            self.manualSpeed = (abs(speed) * abs(diff) + abs(self.minManualSpeed))/1.75
            if speed < 0:
                self.manualSpeed *= -1
        else:
            self.manualSpeed = 0

    @state(first = True)
    def turn(self):
        """
        Starts turning process, if in tolerance it will stop
        """
        self.pos = self.turretThreshold.getPosition()
        self.setSpeed()
        self.next_state("turn")

    def withinTolerance(self):
        """
        returns true if the turret is within tolerance of target
        """
        offset = self.getOffset()
        if offset != None and abs(offset) < self.tolerance:
            return True
        return False
