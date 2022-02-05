from magicbot import feedback

class TurretThreshold:
    compatString = ["doof", "greenChassis"]
    Deadzones = [[0, 90],
                [90, 180]]
    motors_turret: dict
    speed = 0
    safetySpeed = .07
    safetyThreshold = 5

    def setup(self):
        #connects moters and gets position
        self.turretMotor = self.motors_turret["turretMotor"]
        self.pos = self.turretMotor.getEncoder().getPosition()

    def setTurretspeed(self, tSpeed):
        #sets speed
        self.speed = tSpeed

    def stopTurret(self):
        #stops turret
        self.speed = 0

    def angleCheck(self, angle):
        """
        Checks if desired angle is within the deadzone.Then, returns closest point to the angle it can reach.
        """
        for leftLim, rightLim in self.Deadzones:
            if angle > leftLim and angle < rightLim:
                if abs(leftLim - angle) < abs(rightLim - angle):
                    return leftLim
                else:
                    return rightLim
        return angle

    @feedback
    def getPosition(self):
        return self.pos

    def execute(self):
        #gets position, sets speed for every frames
        self.pos = self.turretMotor.getEncoder().getPosition()

        #Final safety check
        if self.speed > self.safetySpeed:
            for lLimit, rLimit in self.Deadzones:
                if abs(lLimit - self.pos) < self.safetyThreshold:
                    self.speed = -1*self.safetySpeed
                elif abs(rLimit - self.pos) < self.safetyThreshold:
                    self.speed = self.safetySpeed

        self.turretMotor.set(self.speed)
