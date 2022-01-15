import navx
from magicbot import feedback

class Navx:
    
    def setup(self):
        self.navx = navx._navx.AHRS.create_spi()

    @feedback
    def getXDisplacement(self):
        return self.navx.getDisplacementX()

    @feedback
    def getYDisplacement(self):
        return self.navx.getDisplacementY()

    @feedback
    def getZDisplacement(self):
        return self.navx.getDisplacementZ()
    
    @feedback
    def getXAngle(self):
        return self.navx.getRoll()

    @feedback
    def getYAngle(self):
        return self.navx.getPitch()

    @feedback
    def getYaw(self):
        return self.navx.getYaw()

    @feedback
    def getFusedHeading(self):
        return self.navx.getFusedHeading()
        
    def reset(self):
        """Resets values to 0 from the current position"""

        self.navx.reset()
        self.navx.resetDisplacement()

    def execute(self):
        pass
