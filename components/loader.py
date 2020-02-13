import wpilib
from time import sleep
# import motorHelper

class LoaderClass:

    def __init__(self):
        self.isAcivated = False

    def reverse(self):
        pass

    def run(self):
        self.isAcivated = True
        # print("Is activated successful. Activated: ", self.isAcivated)

    def stop(self):
        self.isAcivated = False

    def execute(self):
        if self.isAcivated:
            print("Activated")
