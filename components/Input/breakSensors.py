from enum import IntEnum
import logging as log

class SensorKey(IntEnum):
    kLoadingSensor = 1
    kMiddleSensor = 2
    kPostShootSensor = 3
class State:
    kTripped = False
    kNotTripped = True

class Sensors:

    compatString = ["doof", "testBoard"]
    digitalInput_breaksensors: dict
    SensorArray = []

    def on_enable(self):
        for x in range(4):
            self.SensorArray.append(self.digitalInput_breaksensors["sensor" + str(x)])
        log.info("Break sensor component created")

    def loadingSensor(self, state):
        """Gets the loading sensor state and checks if it matches the requested state."""
        if self.SensorArray[SensorKey.kLoadingSensor].get() == state:
            return True
        return False

    def postShootingSensor(self, state):
        """Gets the shooting sensor after the shooter state and checks if it matches the requested state."""
        if self.SensorArray[SensorKey.kPostShootSensor].get() == state:
            return True
        return False

    def middleSensor(self, state):
        """Gets the middle sensor state and checks if it matches the requested state."""
        if self.SensorArray[SensorKey.kMiddleSensor].get() == state:
            return True
        return False

    def execute(self):
        pass
