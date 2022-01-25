from enum import Enum, auto

class Direction(Enum):
    """Enum for intake direction."""
    kForwards = auto()
    kBackwards = auto()
    kDisabled = auto()
