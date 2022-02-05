import navx
from magicbot import tunable, feedback, StateMachine, state
from components.turnToAngle import TurnToAngle
class getPosition(navx):
    compatString = ["doof", "greenChassis"]
    turnToangle: TurnToAngle
    navx = navx._navx.AHRS.create_spi()
    Deadzones = [[-45, -405] [360, 360] [45, 405]]
    motors_turret: dict

    def setup(self):
        self.turretMotor = self.motors_turret["turretMotor"]

    def getOriginalheading(self):
        self.turretMotor.getEncoder().getPosition()


    def stop(self):
        self.running = False
        self.starting = False
        #self.done()

    def checkClamp(self):
        for leftLim, right in self.Deadzones:
            if self.turretMotor.getEncoder().getPosition() < leftLim or self.turretMotor.getEncoder().getPosition() > right:
                self.stop()


