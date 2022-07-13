from enum import Enum


# This is how we will name motors in configs
class Tank(Enum):
    """
    Tank Motors Keys
    """
    numMotors = 4
    FrontLeft = "FrontLeftTankMotor"
    FrontRight = "FrontRightTankMotor"
    BackLeft = "BackLeftTankMotor"
    BackRight = "BackLeftTankMotor"

class Swerve(Enum):
    """
    Swerve Motors Keys
    """
    numMotors = 8
    FrontLeft = "FrontLeftSwerveMotor"
    FrontRight = "FrontRightSwerveMotor"
    BackLeft = "BackLeftSwerveMotor"
    BackRight = "BackLeftSwerveMotor"
    FrontLeftRotation = "FrontLeftRotationMotor"
    FrontRightRotation = "FrontRightRotationMotor"
    BackLeftRotation = "BackLeftRotationMotor"
    BackRightRotation = "BackLeftRotationMotor"
