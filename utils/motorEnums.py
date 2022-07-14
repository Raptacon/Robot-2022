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
    BackRight = "BackRightTankMotor"

class TwoMotorTank(Enum):
    """
    Tank Motors Keys
    """
    numMotors = 2
    Left = "LeftTankTwoMotor"
    Right = "RightTankTwoMotor"

class Swerve(Enum):
    """
    Swerve Motors Keys
    """
    numMotors = 8
    FrontLeft = "FrontLeftSwerveMotor"
    FrontRight = "FrontRightSwerveMotor"
    BackLeft = "BackLeftSwerveMotor"
    BackRight = "BackRightSwerveMotor"
    FrontLeftRotation = "FrontLeftRotationMotor"
    FrontRightRotation = "FrontRightRotationMotor"
    BackLeftRotation = "BackLeftRotationMotor"
    BackRightRotation = "BackRightRotationMotor"
