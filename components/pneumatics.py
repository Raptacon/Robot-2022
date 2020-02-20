import wpilib

class Pneumatics:
    
    def setup(self):
        self.solenoid = wpilib.DoubleSolenoid(0, 1) #I don't know if this is the proper a) class to define or b) the right channels for the solenoid. This is mostly a placeholder and can be fixed

    def get(self):
        return self.solenoid.get()
        
    def execute(self):
        pass