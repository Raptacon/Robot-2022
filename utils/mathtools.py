
def expScale(initVal, exp):
    """
    Applies an exponent exp to a value initVal and returns value.
    Will work whether initVal is positive or negative or zero.
    """
    val = initVal
    if val > 0:
        val = val ** exp
    if val < 0:
        val *= -1
        val = val ** exp
        val *= -1
    return val
