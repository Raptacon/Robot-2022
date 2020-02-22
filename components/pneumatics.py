import wpilib

class Pneumatics:
    
    def setup(self):
        self.solenoid = wpilib.DoubleSolenoid(0, 1) #I don't know if this is the proper a) class to define or b) the right channels for the solenoid. This is mostly a placeholder and can be fixed
        self.compressor = wpilib.Compressor()
        self.compressor.start()

    def getSolenoid(self):
        """
        returns the "value" of the solenoid. Boolean, is it on or off?
        """
        return self.solenoid.get()
        
    def enableSolenoid(self):
        self.solenoid.set(True)

    def disableSolenoid(self):
        self.solenoid.set(False)

    def execute(self):
        pass