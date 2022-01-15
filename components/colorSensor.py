from rev.color import ColorSensorV3, ColorMatch
import wpilib
from magicbot import tunable, feedback

class ColorSensor():

    colorSensor = ColorSensorV3(wpilib.I2C.Port.kOnboard)
    colorMatch = ColorMatch()
    # The closer this is to 0, the closer the color has to be to the color.
    confidence = tunable(.1)
    colors = {"red":wpilib.Color(.5, 0, 0),
             "blue":wpilib.Color(0, 0, .5),
             "white":wpilib.Color(1, 1, 1),
             "black":wpilib.Color(0, 0, 0)}
    

    def setup(self):
        for color in self.colors.keys():
            self.colorMatch.addColorMatch(self.colors[color])
        self.color = self.colors["white"]

    def updateColor(self):
        self.color = self.colorSensor.getColor()

    def getColor(self):
        return self.color

    def getColorMatch(self):
        """
        Returns the color closest
        to the current input.
        Either red, blue, white or black.
        """
        return self.colorMatch.matchClosestColor(self.color, self.confidence)
    
    def getRed(self):
        return True if self.colorMatch.matchClosestColor(self.color, self.confidence) == self.colors["red"] else False

    def getBlue(self):
        return True if self.colorMatch.matchClosestColor(self.color, self.confidence) == self.colors["blue"] else False

    @feedback
    def displayRed(self):
        return self.getColor().red
        
    @feedback
    def displayRedMatch(self):
        return self.getColorMatch().red

    @feedback
    def displayBlue(self):
        return self.getColor().blue
    
    @feedback
    def displayBlueMatch(self):
        return self.getColorMatch().blue

    def execute(self):
        self.updateColor()
