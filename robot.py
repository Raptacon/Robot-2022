import wpilib
from team3200 import Robot as Robot

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
