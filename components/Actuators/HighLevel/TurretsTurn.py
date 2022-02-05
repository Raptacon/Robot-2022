from magicbot import state_machine, state, timed_state

class turretTurn:
    compatString = ["doof", "greenChassis"]
    motors_turret: dict
    


    def on_enable(self):
        self.turretMotor = self.motors_turret["turretMotor"]
        self.turret = False


    def execute(self):
        pass




