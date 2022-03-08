"""
Contains helpers to create various sensor types
"""

from wpilib import DigitalInput as di, Servo
import logging
import navx

def gyroFactory(descp):
    """
    Creates gyros from a gyro descp
    """
    try:
        if "navx" == descp["type"]:
            """
            Supports spi and i2c with default values. More can be added as needed.
            """
            method = descp["method"]
            if method == "spi":
                return navx.AHRS.create_spi()
            if method == "i2c":
                return navx.AHRS.create_i2c()
            #invalid method, thorw a fit
            raise ValueError(f"{method} method is invalid")

    except Exception as e:
        logging.error("Failed to create gyro for %s. Error %s",descp, e)
    return None

def breaksensorFactory(descp):
    """
    Creates break sensors from a break sensor descp
    """
    try:
        if "RIODigitalIn" in descp["type"]:
            return di(descp["channel"])

    except Exception as e:
        logging.error("Failed to create IR Break sensor for %s. Error %s", descp, e)
    return None

def servoFactory(descp):
    if "channel" in descp:
        return Servo(descp["channel"])
    else:
        logging.error("Channel not included with servo %s", descp)
    return None
