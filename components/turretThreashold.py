import navx
from magicbot import tunable, feedback, StateMachine, state
from components.turnToAngle import TurnToAngle
from components.shooterMotors import ShooterMotors
class getPosition(navx):
    compatString = ["doof", "greenChassis"]
    turnToangle: TurnToAngle
    navx = navx._navx.AHRS.create_spi()
    Deadzones = [[-45, -405] [360, 360] [45, 405]]
    shooterMotor: ShooterMotors
    motors_turret: dict

    def setup(self):
        self.turretMotor = self.motors_turret["turretMotor"]

    def getOriginalheading(self):
        self.shooterMotor.shooterMotor1.getencoder().getPosition()


    def stop(self):
        self.running = False
        self.starting = False
        #self.done()

    def checkClamp(self):
        for leftLim, right in self.Deadzones:
            if self.shooterMotor.shooterMotor1.getencoder().getPosition() < leftLim or self.shooterMotor.shooterMotor1.getencoder().getPosition() > right:
                self.stop()


