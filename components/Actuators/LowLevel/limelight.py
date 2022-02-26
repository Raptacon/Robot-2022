from networktables import NetworkTables

class Limelight():
    compatString = ["teapot"]
    limeTable = NetworkTables.getTable("limelight")
    def LEDOff(self):
        self.limeTable.putNumber('ledMode',1)
    def LEDOn(self):
        self.limeTable.putNumber('ledMode',3)
    def resetLED(self):
        """
        Resets the LED to whatever the setting is
        """
        self.limeTable.putNumber('ledMode',0)
    def execute(self):
        pass
