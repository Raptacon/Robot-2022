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
    try:
        # patch no exit error if not running on robot
        try:
            print(wpilib._impl.main.exit)
        except Exception:
            wpilib._impl.main.exit = exit

        # fixes simulation rerun errors.
        # todo verify this causes no issues on robot
        wpilib.DriverStation._reset()

    except Exception as err:
        print("Failed to do extra setup. Error", err)

    wpilib.run(Robot, physics_enabled=True)

