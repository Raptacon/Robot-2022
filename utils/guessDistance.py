import math
def guessDistanceTrig(targetHeight, ownHeight, angleOffset, angle):
    """
    Uses the difference between two heights and an angle to construct a
    right triangle and tangent to determine the horizontal distance.
    """
    return (targetHeight - ownHeight) / math.tan(math.radians(angle + angleOffset))
