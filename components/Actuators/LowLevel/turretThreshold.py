from magicbot import feedback
import navx
from components.Actuators.AutonomousControl.turnToAngle import TurnToAngle
class getPosition(navx):
    compatString = ["doof", "greenChassis"]
    turnToangle: TurnToAngle
    navx = navx._navx.AHRS.create_spi()
    Deadzones = [[0, 90],
                [90, 180]]
    motors_turret: dict
    speed = 0

    def setup(self):
        self.turretMotor = self.motors_turret["turretMotor"]
        self.pos = self.turretMotor.getEncoder().getPosition()

    def runTurret(self, tSpeed):
        self.speed = tSpeed

    def stopTurret(self):
        self.speed = 0

    def angleCheck(self, angle):
        """
        """
        for leftLim, right in self.Deadzones:
            if angle > leftLim and angle < right:
                if abs(leftLim - angle) < abs(right - angle):
                    return leftLim
                else:
                    return right
        return angle

    @feedback
    def getPosition(self):
        return self.pos

    def execute(self):
        self.pos = self.turretMotor.getEncoder().getPosition()

        self.turretMotor.set(self.speed)
