import logging as log
from wpimath.controller import PIDController

def speedFactory(descp):
    return descp

class SpeedSections():
    configuredValues_speedSections: dict

    def setup(self):
        self.speedSections = self.configuredValues_speedSections
        self.PIDs = self.speedSections["PID"]
        self.PIDControllers = []
        for PIDset in self.PIDs.keys():
            self.PIDControllers[PIDset] = PIDController()


    def getSpeedSection(self, component:str):
        """
        Gives a 2D array with a table of
        distance limits for a specific component.
        """
        if component in self.speedSections:
            return self.speedSections[component]
        elif "None" in self.speedSections:
            log.error("Current robot does not have speed sections defined")
            return
        else:
            log.error(component+"'s speed sections aren't present in current data")
            return

    def getPID(self, component:str):
        if component in self.PIDs:
            return self.PIDs[component]
        elif "None" in self.PIDs:
            log.error("Current robot does not have speed sections PID defined")
            return
        else:
            log.error(component+"'s PIDs aren't present in current data")
            return

    def getSpeed(self, offset, component:str):
        """
        Returns a speed for you based on an offset
        and your component.
        """
        section = self.getSpeedSection(component)
        for dist, speed in section:
            if (dist == "End"
                or offset < dist):
                if speed == "PID":
                    return 0
                return speed

    def execute(self):
        """
        This component doesn't need to update anything on every frame.
        """
        pass
