from enum import IntEnum
import logging as log

class SensorKey(IntEnum):
    kLoadingSensor = 0
    kMiddleSensor = 1
    kPostShootSensor = 2
class State:
    kTripped = False
    kNotTripped = True

class Sensors:

    compatString = ["doof", "testBoard", "teapot"]
    digitalInput_breaksensors: dict
    SensorArray = []

    def on_enable(self):
        for x in range(3):
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
        log.error(str(self.loadingSensor(State.kTripped))+str(self.middleSensor(State.kTripped))+str(self.postShootingSensor(State.kTripped)))
        pass
