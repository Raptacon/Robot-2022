from rev.color import ColorSensorV3, ColorMatch
import wpilib

class ColorSensor():

    colorSensor = ColorSensorV3(wpilib.I2C.Port.kOnboard)
    colorMatch = ColorMatch()
    colors = {"red":wpilib.Color(1, 0, 0),
             "blue":wpilib.Color(0, 1, 0),
             "white":wpilib.Color(1, 1, 1),
             "black":wpilib.Color(0, 0, 0)}

    def setup(self):
        for color in self.colors:
            self.colorMatch.addColorMatch(color)

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
        return True if self.colorMatch.matchClosestColor(self.color) == self.colors["red"] else False

    def getBlue(self):
        return True if self.colorMatch.matchClosestColor(self.color) == self.colors["blue"] else False

    def execute(self):
        self.updateColor()