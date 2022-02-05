

class turretTurn:
    compatString = ["doof", "greenChassis"]
    motors_turret: dict
    

    def on_enable(self):
        self.turretMotor = self.motors_turret["turretMotor"]
        self.turretMotorspeed = 0
