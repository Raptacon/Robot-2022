import navx
from magicbot import tunable, feedback, StateMachine, state
from components.turnToAngle import TurnToAngle
class getPosition(navx):
    compatString = ["doof", "greenChassis"]
    turnToangle: TurnToAngle
    navx = navx._navx.AHRS.create_spi()


    def getOriginalheading(self):
        self.originalHeading = self.navx.getFusedHeading()

    def stop(self):
        self.running = False
        self.starting = False
        #self.done()

    def getCurrentheading(self):
        pass


    def checkClamp(self):
        if abs(self.navx.getFusedHeading() - self.nextHeading) < self.tolerance:
            self.stop()
