import navx
from magicbot import tunable, feedback, StateMachine, state
from components.turnToAngle import TurnToAngle
class getPosition(navx):
    compatString = ["doof", "greenChassis"]
    turnToangle: TurnToAngle
    navx = navx._navx.AHRS.create_spi()


    def getOriginalheading(self):
        self.originalHeading = self.navx.getFusedHeading()
        self.shooterMotor.shooterMotor1.getencoder().getPosition()
        self.leftLimit = self.originalHeading - 45
        self.rightLimit = self.originalHeading + 45

    def stop(self):
        self.running = False
        self.starting = False
        #self.done()

    def checkClamp(self):

        if abs(self.navx.getFusedHeading() - self.nextHeading) < self.leftLimit or abs(self.navx.getFusedHeading() + self.rightLimit):
            self.stop()
