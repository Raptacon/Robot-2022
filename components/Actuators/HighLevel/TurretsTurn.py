

class turretTurn:
    compatString = ["doof", "greenChassis"]
    motors_turret: dict
    


    def on_enable(self):
        self.turretMotor = self.motors_turret["turretMotor"]
        self.turret = False

    def runTurret(self, sSpeed):
        self.turretMotorspeed = sSpeed
        self.turret = True

    def isTurretrunning(self):
        return self.turret

    def stopTurret(self):
        self.turret = False

    def execute(self):
        pass




