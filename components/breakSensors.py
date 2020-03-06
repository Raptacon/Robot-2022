from enum import IntEnum

class SensorKey(IntEnum):
    kLoadingSensor = 0
    kShootingSensor = 4

class Sensors:

    digitalInput_breaksensors: dict

    def on_enable(self):
        self.SensorArray = []
        for x in range(1, 6):
            self.SensorArray.append(self.digitalInput_breaksensors["sensor" + str(x)])
        self.logger.info("Break sensor component created")

    def execute(self):
        return self.SensorArray
