from magicbot import state_machine, state, timed_state
from components.Actuators.LowLevel.turretThreshold import getPosition

class turretTurn:
    compatString = ["doof", "greenChassis"]
    motors_turret: dict
    GetPosition: getPosition
    turnAngle = 0

    def on_enable(self):
        self.turretMotor = self.motors_turret["turretMotor"]
        self.GetPosition.setup()

    def setAngle(self, angle):
        self.turnAngle = getPosition.angleCheck(angle)

    @state(first = True)
    def idling(self):
        """Stays in this state until started"""
        if self.turnAngle != 0:
            self.next_state("")
        else:
            self.next_state("idling")
