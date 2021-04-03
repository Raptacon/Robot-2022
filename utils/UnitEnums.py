from enum import Enum, auto
class velocityUnits(Enum):
    kRPM = auto()
    kRPS = auto()
    kEncoderTicksPer100 = auto()

class positionUnits(Enum):
    kEncoderTicks = auto()
    kRotations = auto()
