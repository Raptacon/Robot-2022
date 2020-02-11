import wpilib
# import motorHelper

class LoaderClass:

    LoaderMotor: wpilib.Talon

    def __init__(self):
        self.isAcivated = False

    def reverse(self):
        pass

    def run(self):
        self.isAcivated = True

    def stop(self):
        self.isAcivated = False

    def execute(self):
        if self.isAcivated:
            self.LoaderMotor.set(1)