from wpilib import DoubleSolenoid
dsPos = DoubleSolenoid.Value
import logging as log

class Pneumatics:
    compatString = []
    compressors_pneumatics: dict
    solenoids_pneumatics: dict


    def setup(self):
        """
        Setup to enable everything after variable injection from robot.py. This is where the bulk of setup for this class should be.
        on_enable() may need to be used for when something needs to happen everytime the state is changed, like from autonomous to teleop.
        """
        self.loaderSolenoid = self.solenoids_pneumatics["loader"]
        self.newLoaderValue = None
        #turn on all compressors
        log.info("Starting compressor %s", self.compressors_pneumatics["compressor"])
        self.compressors_pneumatics["compressor"].start()

    def getLoaderDeployed(self):
        """
        returns the "value" of the solenoid. Boolean, is it on or off?
        """
        return True if self.solenloaderSolenoidoid.get() == dsPos.kForward else False
    def deployLoader(self):
        """
        Turn the loader to the deployed position
        """
        self.newLoaderValue = dsPos.kForward
        #self.solenoid.set(wpilib.DoubleSolenoid.Value.kForward) #currently, this is only set to handle one solenoid. I believe that both bots only have one.

    def retractLoader(self):
        """
        Turn loader to the retracted position
        """
        self.newLoaderValue = dsPos.kReverse
        #self.solenoid.set(wpilib.DoubleSolenoid.Value.kReverse) #currently, this is only set to handle one solenoid. I believe that both bots only have one.

    def toggleLoader(self):
        """
        Toggle the Loader from deployed to retracted or vice versa
        """
        log.warning("Changing solenoid")
        self.newLoaderValue = (dsPos.kReverse if self.loaderSolenoid.get() == dsPos.kForward else dsPos.kForward)

    def getCompressorCurrent(self):
        """
        Returns how much current the compressor is currently drawing. Useful to not brown out
        """
        return self.compressors_pneumatics["compressor"].getCompressorCurrent()

    def execute(self):
        """
        Set loader if loader change was requested
        """
        if self.newLoaderValue:
            self.loaderSolenoid.set(self.newLoaderValue)
            self.newLoaderValue = None
