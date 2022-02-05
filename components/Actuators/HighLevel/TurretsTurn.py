from magicbot import state_machine, state, timed_state
from components.Actuators.LowLevel.turretThreshold import getPosition

class turretTurn:
    compatString = ["doof", "greenChassis"]
    motors_turret: dict
    GetPosition: getPosition


    def on_enable(self):
        self.turretMotor = self.motors_turret["turretMotor"]
        self.GetPosition.setup()
        self.turret = False


    def execute(self):
        pass




