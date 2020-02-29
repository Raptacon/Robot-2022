"""
Contains helpers to create various sensor types
"""

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
