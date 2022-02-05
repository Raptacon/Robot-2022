from magicbot import StateMachine, state, tunable
from components.Actuators.LowLevel.turretThreshold import TurretThreshold
from components.SoftwareControl.speedSections import SpeedSections

class turretTurn(StateMachine):
    compatString = ["doof", "greenChassis"]
    motors_turret: dict
    turretThreshold: TurretThreshold
    speedSections: SpeedSections
    turnAngle = 0
    tolerance = tunable(0.5)

    def setAngle(self, angle):
        """gets angle turret is turning to"""
        self.turnAngle = self.turretThreshold.angleCheck(angle)

    @state(first = True)
    def idling(self):
        """Stays in this state until started"""
        if self.turnAngle != 0:
            self.next_state("turn")
        else:
            self.next_state("idling")

    def setSpeed(self):
        """
        Sets speed of turret based on what angle we are turning to
        """
        speed = self.speedSections.getSpeed(self.turretThreshold.getPosition(), "TurretsTurn")
        self.turretThreshold.setTurretspeed(speed)

    @state
    def turn(self):
        """
        Starts turning process, if in tolerance it will stop
        """
        self.pos = self.turretThreshold.getPosition()
        self.setSpeed()
        if self.pos < (self.turnAngle + self.tolerance) and self.pos > (self.turnAngle - self.tolerance):
            self.stop()
        else:
            self.next_state("turn")

    def stop(self):
        """stops turret"""
        self.next_state("idling")
        self.turretThreshold.stopTurret()
