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

    def execute(self):
        """
        This component doesn't need to update anything on every frame.
        """
        pass
