import navx
from components.Actuators.AutonomousControl.turnToAngle import TurnToAngle
class getPosition(navx):
    compatString = ["doof", "greenChassis"]
    turnToangle: TurnToAngle
    navx = navx._navx.AHRS.create_spi()
    Deadzones = [[0, 90] [90, 180]]
    motors_turret: dict

    def setup(self):
        self.turretMotor = self.motors_turret["turretMotor"]
        self.turretMotor.getEncoder().getPosition()


    def stop(self):
        self.running = False
        self.starting = False
        #self.done()

    def checkDeadzone(self):
        for leftLim, right in self.Deadzones:
            if self.turretMotor.getEncoder().getPosition() < leftLim or self.turretMotor.getEncoder().getPosition() > right:
                self.stop()


