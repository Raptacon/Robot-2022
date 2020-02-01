"""
Base file that setups basic robot. Actual robot is in team3200 module.
This file should not need to be edited.
"""
import wpilib
import team3200

class Robot(team3200.Team3200Robot):
    """
    Shim class to make Robot code happy. Please do not edit
    """
    pass


if __name__ == '__main__':
    wpilib.run(Robot, physics_enabled=True)

