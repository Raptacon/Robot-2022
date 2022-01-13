from rev.color import ColorSensorV3
import wpilib

class ColorSensor():

    colorSensor = ColorSensorV3(wpilib.I2C.Port.kOnboard)

    def getColor(self):
        print(str(self.colorSensor.getColor()))

