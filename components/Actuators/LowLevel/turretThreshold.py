from magicbot import feedback

class TurretThreshold:
    compatString = ["doof", "greenChassis"]
    Deadzones = [[90, 180]]
    motors_turret: dict
    speed = 0
    exitSpeed = .3
    safetySpeed = .07
    safetyThreshold = 5
    gearRatio = 10
    sprocketRatio = 120/18
    DegreeToAngle = 0

    def setup(self):
        #connects moters and gets position
        self.turretMotor = self.motors_turret["turretMotor"]
        self.encoder = self.turretMotor.getEncoder()
        self.pos = self.encoder.getPosition()

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

            # Check paths
            if leftLim > self.pos and leftLim < angle:
                return leftLim
            elif rightLim < self.pos and rightLim > angle:
                return rightLim
        return angle

    # def DetermineShortestPath(self, angle, leftLim, rightLim):
    #     self.DegreeToAngle = self.pos
    #     while self.DegreeToAngle != angle:
    #         self.DegreeToAngle += 0.1
    #         if self.DegreeToAngle > leftLim and self.DegreeToAngle < rightLim:
    #             return self.DegreeToAngle

    @feedback
    def getPosition(self):
        return self.pos

    @feedback
    def getSpeed(self):
        return self.speed

    def calc_Position(self):
        self.pos = 360 * self.encoder.getPosition() / (self.gearRatio * self.sprocketRatio)

    def execute(self):
        #gets position, sets speed for every frames
        self.calc_Position()

        #Final safety check
        # if self.speed > self.safetySpeed:
        #     for lLimit, rLimit in self.Deadzones:
        #         if abs(lLimit - self.pos) < self.safetyThreshold:
        #             self.speed = -1*self.safetySpeed
        #         elif abs(rLimit - self.pos) < self.safetyThreshold:
        #             self.speed = self.safetySpeed

        for lLimit, rLimit in self.Deadzones:
            if self.pos > lLimit and self.pos < rLimit:
                if abs(lLimit - self.pos) < abs(rLimit - self.pos):
                    self.speed = -1*self.exitSpeed
                else:
                    self.speed = self.exitSpeed

        self.turretMotor.set(self.speed)
