from turtle import pos
from magicbot import feedback

class TurretThreshold:
    compatString = ["doof", "greenChassis"]
    Deadzones = [[90, 180]]
    motors_turret: dict
    speed = 0
    safetySpeed = .07
    safetyThreshold = 5
    gearRatio = 10
    sprocketRatio = 120/18

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
                    smallestLeftAngle = self.smallestAngle(self.pos, leftLim)
                    return smallestLeftAngle
                else:
                    smallestRightAngle = self.smallestAngle(self.pos, rightLim)
                    return smallestRightAngle
        smallestAngle = self.smallestAngle(self.pos, angle)
        return smallestAngle

    def smallestAngle(self, currentAngle, targetAngle) -> int:
        diff = ( targetAngle - currentAngle) % 360

        if diff > targetAngle :
            diff = -(360 - diff)
            return diff

    @feedback
    def getPosition(self):
        return self.pos

    def calc_Position(self):
        self.pos = 360 * self.encoder.getPosition() / (self.gearRatio * self.sprocketRatio)

    def execute(self):
        #gets position, sets speed for every frames
        self.calc_Position()

        #Final safety check
        if self.speed > self.safetySpeed:
            for lLimit, rLimit in self.Deadzones:
                if abs(lLimit - self.pos) < self.safetyThreshold:
                    self.speed = -1*self.safetySpeed
                elif abs(rLimit - self.pos) < self.safetyThreshold:
                    self.speed = self.safetySpeed
        for leftLim, rightLim in self.Deadzones:
            if self.pos > leftLim and self.pos < rightLim:
                self.stopTurret()
        self.turretMotor.set(self.speed)
