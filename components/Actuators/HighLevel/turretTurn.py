from magicbot import StateMachine, state, tunable
from components.Actuators.LowLevel.turretThreshold import TurretThreshold
from components.SoftwareControl.speedSections import SpeedSections
import logging as log

class TurretTurn(StateMachine):
    compatString = ["doof", "greenChassis"]
    motors_turret: dict
    turretThreshold: TurretThreshold
    speedSections: SpeedSections
    turnAngle = None
    tolerance = tunable(3)

    def setup(self):
        self.pos = self.turretThreshold.getPosition()

    def setAngle(self, angle):
        """sets angle turret is turning to"""
        if self.turretThreshold.angleCheck(angle) != angle:
            log.error("Turret angle check failed")
        self.turnAngle = self.turretThreshold.angleCheck(angle)

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
        offset = self.turnAngle - self.pos
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
