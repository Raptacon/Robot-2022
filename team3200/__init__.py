# Import the base classes to use anywhere in team3200
from .robot_int import Team3200Robot as Team3200Robot
from .robotMap import RobotMap as RobotMap

# import submodules
from . import subsystems
from . import commands

# create instance of robotMap for use everywhere
robotMap = RobotMap()

__all__ = ["Robot", "RobotMap", "subsystems", "commands", "robotMap"]
