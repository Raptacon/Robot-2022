import navx
from magicbot import tunable, feedback, StateMachine, state

class getPosition(navx):
    compatString = ["doof", "greenChassis"]
    navx = navx._navx.AHRS.create_spi()

    def getOriginalheading(self):
        self.originalHeading = self.navx.getFusedHeading()