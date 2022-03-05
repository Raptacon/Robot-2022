"""
Contains helpers to create various acturators
"""

import logging

import wpilib


def compressorFactory(descp):
    """
    Creates compressor objects from descp.
    """
    try:
        if descp["type"] == "compressor":
            return wpilib.Compressor(descp["pcm"], wpilib.PneumaticsModuleType.CTREPCM)
    except Exception as e:
        logging.error("Failed to create compressor for %s err %s", descp, e)
    return None


def solenoidFactory(descp):
    """
    Creates single and double solenoids devices from descp
    """
    # try:
    pcm = 0
    if pcm in descp:
        pcm = descp["pcm"]
    if descp["type"] == "solenoid":
        return wpilib.Solenoid(pcm, wpilib.PneumaticsModuleType.CTREPCM, descp["channel"])
    if descp["type"] == "doubleSolenoid":
        solenoid = wpilib.DoubleSolenoid(pcm, wpilib.PneumaticsModuleType.CTREPCM, descp["channel"]["forward"], descp["channel"]["reverse"])
        if "default" in descp:
            value = {"kOff":0, "kForward":1, "kReverse":2}[descp["default"]]
            solenoid.set(wpilib.DoubleSolenoid.Value(value))
        return solenoid
    # except Exception as e:
    #     logging.error("Failed to create solenoid %s. Err %s", descp, e)

    return None
