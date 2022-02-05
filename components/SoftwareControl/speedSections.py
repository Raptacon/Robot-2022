import logging as log

def speedFactory(descp):
    return descp

class SpeedSections():
    configuredValues_speedSections: dict

    def setup(self):
        self.speedSections = self.configuredValues_speedSections

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

    def getSpeed(self, offset, component:str):
        """
        """
        section = self.getSpeedSection(component)
        for dist, speed in section:
            if (dist == "End"
                or offset < dist):
                if speed == "PID":
                    return NotImplementedError
                    # Sorry
                return speed

    def execute(self):
        """
        This component doesn't need to update anything on every frame.
        """
        pass
