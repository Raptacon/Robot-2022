import logging as log
from utils.configMapper import findConfig
from utils import yaml
from robotMap import RobotMap
import os
class SpeedSections():
    configPath = os.path.join(findConfig()[1],"speedSections.yml")
    map: RobotMap
    currentRobot: str

    def setup(self):
        """
        Loads the file and collects data.
        """
        with open(self.configPath) as file:
            self.values = yaml.load(file, yaml.FullLoader)
        if self.currentRobot in self.values:
            self.data = self.values[self.currentRobot]
        else:
            log.error("Current robot does not have speed sections defined")
            self.data = {"None":None}

    def getSpeedSection(self, component:str):
        """
        Gives a 2D array with a table of
        distance limits for a specific component.
        """
        if component in self.data:
            return self.data[component]
        elif "None" in self.data:
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
