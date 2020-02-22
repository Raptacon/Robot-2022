import wpilib

class Pneumatics:
    
    def setup(self):
        """
        Setup to enable everything after variable injection from robot.py. This is where the bulk of setup for this class should be.
        on_enable() may need to be used for when something needs to happen everytime the state is changed, like from autonomous to teleop.
        """
        self.solenoid = wpilib.DoubleSolenoid(0, 1) #I don't know if this is the proper a) class to define or b) the right channels for the solenoid. This is mostly a placeholder and can be fixed
        self.compressor = wpilib.Compressor()
        self.compressor.start()
        self.solenoid.set(wpilib.DoubleSolenoid.Value.kOff)

    def getSolenoid(self):
        """
        returns the "value" of the solenoid. Boolean, is it on or off?
        """
        return self.solenoid.get()
        
    def enableSolenoid(self):
        """
        Turn the solenoid into the "on" position. This can vary per configuration
        """
        self.solenoid.set(wpilib.DoubleSolenoid.Value.kForward) #currently, this is only set to handle one solenoid. I believe that both bots only have one.

    def disableSolenoid(self):
        """
        Turn the solenoid into the "off" position. This can vary per configuration
        """
        self.solenoid.set(wpilib.DoubleSolenoid.Value.kReversese) #currently, this is only set to handle one solenoid. I believe that both bots only have one.

    def toggleSolenoid(self):
        """
        Toggle the solenoid from off to on, or on to off.
        """
        if self.solenoid.get() == True:
            self.solenoid.set(wpilib.DoubleSolenoid.Value.kReverse)
        else:
            self.solenoid.set(wpilib.DoubleSolenoid.Value.kForward)

    def getCompressorCurrent(self):
        """
        Returns how much power the compressor is currently drawing. Useful to not brown out
        """
        return self.compressor.getCompressorCurrent()

    def execute(self):
        """
        Nothing is needed to run every period. Otherwise, this would have something other than pass
        """
        pass
