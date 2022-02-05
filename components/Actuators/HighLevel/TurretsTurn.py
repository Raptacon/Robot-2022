from webbrowser import get
from magicbot import state_machine, state, timed_state, tunable
from components.Actuators.AutonomousControl.turnToAngle import TurnToAngle
from components.Actuators.LowLevel.turretThreshold import turretThreshold

class turretTurn:
    compatString = ["doof", "greenChassis"]
    motors_turret: dict
    TurretThreshold: turretThreshold
    turnAngle = 0
    tolerance = tunable(0.5)

    def on_enable(self):
        self.turretMotor = self.motors_turret["turretMotor"]
        self.TurretThreshold.setup()

    def setAngle(self, angle):
        self.turnAngle = turretThreshold.angleCheck(angle)

    @state(first = True)
    def idling(self):
        """Stays in this state until started"""
        if self.turnAngle != 0:
            self.next_state("turn")
        else:
            self.next_state("idling")

    def setSpeed(self, angle):
        self.pos = self.turretMotor.getEncoder().getPosition()
        if self.pos < (self.setAngle + angle) or self.pos > (self.setAngle - angle):
            turretThreshold.runTurret(0.5)
        else:
            turretThreshold.runTurret(1)

    @state
    def turn(self, angle):
        self.setSpeed()
        turretThreshold.execute()
        if self.pos < (self.turnAngle + self.tolerance) and self.pos > (self.turnAngle - self.tolerance):
            self.stop()

    def stop(self):
        turretThreshold.stopTurret()
