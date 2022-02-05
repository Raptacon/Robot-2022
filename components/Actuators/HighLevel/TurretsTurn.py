from webbrowser import get
from magicbot import state_machine, state, timed_state, tunable
from components.Actuators.AutonomousControl.turnToAngle import TurnToAngle
from components.Actuators.LowLevel.turretThreshold import getPosition

class turretTurn:
    compatString = ["doof", "greenChassis"]
    motors_turret: dict
    GetPosition: getPosition
    turnAngle = 0
    tolerance = tunable(0.5)

    def on_enable(self):
        self.turretMotor = self.motors_turret["turretMotor"]
        self.GetPosition.setup()

    def setAngle(self, angle):
        self.turnAngle = getPosition.angleCheck(angle)

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
            getPosition.runTurret(0.5)
        else:
            getPosition.runTurret(1)

    @state
    def turn(self, angle):
        self.setSpeed()
        getPosition.execute()
        if self.pos < (self.turnAngle + self.tolerance) and self.pos > (self.turnAngle - self.tolerance):
            self.stop()

    def stop(self):
        getPosition.stopTurret()
