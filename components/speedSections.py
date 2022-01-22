from logging import RootLogger
from utils.configMapper import findConfig
from utils import yaml
from robotMap import RobotMap
import os
class SpeedSections():
    configPath = os.path.join(findConfig()[1],"speedSections.yml")
    map: RobotMap

    def setup(self):
        with open(self.configPath) as file:
            self.values = yaml.load(file, yaml.FullLoader)
        self.listRobots = self.values.keys()

    def execute(self):
        print(self.listRobots)
