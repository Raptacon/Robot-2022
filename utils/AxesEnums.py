from enum import Enum, auto

class AxesTransforms(Enum):
    """Enum for axes input interpretation."""
    kTank = auto()
    kArcade = auto()
    kSwerve = auto()
