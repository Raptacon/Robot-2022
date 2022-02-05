from rev import ColorSensorV3, ColorMatch
import wpilib
from magicbot import feedback

class ColorSensor():

    colorSensor = ColorSensorV3(wpilib.I2C.Port.kOnboard)
    colorMatch = ColorMatch()
    # The closer this is to 0, the closer the color has to be to the color.
    colors = {"red":wpilib.Color(.4, .15, .05),
             "blue":wpilib.Color(.1, .2, .4),
             "white":wpilib.Color(.5, .5, .5),
             "black":wpilib.Color(0, 0, 0)}
    colorMatched = None
    
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
        return self.colorMatch.matchClosestColor(self.color)
    
    def getRed(self):
        """Returns True if the closest color is red"""
        return True if self.colorMatch.matchClosestColor(self.color) == self.colors["red"] else False

    def getBlue(self):
        """Returns True if the closest color is blue"""
        return True if self.colorMatch.matchClosestColor(self.color, self.confidence) == self.colors["blue"] else False

    @feedback
    def displayColor(self):
        """Displays the matching color"""
        if self.getRed():
            self.colorMatched = "red"
        elif self.getBlue():
            self.colorMatched = "blue"
        else:
            self.colorMatched = "none"
        return self.colorMatched

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
