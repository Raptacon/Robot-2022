import logging
from enum import IntEnum, Enum, auto
from components.shooterLogic import ShooterLogic
# from components.ledLogic import LED

class Sensors(IntEnum):
    kLoadingSensor = 5
    kShootingSensor = 1

class ActionType(Enum):
    kLoading = auto()
    kShooter = auto()
    kLED = auto()

class BreakSensors:
    """Class that holds breaksensor callbacks."""

    compatString = ["doof"]
    digitalInput_breaksensors: dict
    shooter: ShooterLogic
    # led: LED
    logger: logging

    def setup(self):
        self.entries = {}
        # self.sensorArray = []

        self.logger.info("IR Break Sensor component created.")

    #NOTE: May be used in the future
    # def canBeAutomatic(self):
    #     for sensor in range(1, 6):
    #         sensorKey = "sensor" + str(sensor)
    #         self.sensorArray.append(self.digitalInput_breaksensors[sensorKey].get())
    #     return all(self.sensorArray)

    def registerSensorEvent(self, stateMachine, actionType, sensor, requestedValue, conditionalState, newState):
        """
        Registers a callback and creates a dictionary 'entry' with specified attributes.
        NOTE: This method is used EXCLUSIVELY for StateMachines.
        These attributes are:
        stateMachine - what StateMachine is being used for this callback
        actionName - title of action that callback does (also key for entry in entries dict)
        sensor - what sensor is used to execute this action (MUST be an int)
        requestedValue - what value the sensor has to read to execute this action
        conditionalState - state the StateMachine must be in for callback to execute (None if no state necessary)
        newState - what state the shooterLogic StateMachine transitions to
        """
        self.logger.info("sensor %s, requesting %s, condition %s, moving to %s.", int(sensor), requestedValue, conditionalState, newState)
        entry = {}
        entry["stateMachine"] = stateMachine
        if "Loader" in actionType:
            entry["actionType"] = ActionType.kLoading
        elif "Shooter" in actionType:
            entry["actionType"] = ActionType.kShooter
        elif "LED" in actionType:
            entry["actionType"] = ActionType.kLED
        else:
            raise ValueError("Invalid action type")
        entry["sensor"] = int(sensor)
        entry["requestedValue"] = requestedValue
        entry["conditionalState"] = conditionalState
        entry["newState"] = newState
        self.entries[actionType] = entry

    def __executeEvent(self, stateMachine, conditionalState, newState):
        """Executes an action with arguments."""
        if self.shooter.current_state == conditionalState or conditionalState == None:
            stateMachine.next_state(str(newState))

    def __processLoadingEvent(self, stateMachine, sensor, requestedValue, conditionalState, newState):
        """Contains information necessary for executing the loader."""
        sensorKey = "sensor" + str(sensor)
        if self.digitalInput_breaksensors[sensorKey].get() == requestedValue and self.shooter.current_state != newState and self.shooter.current_state != "runLoaderManually" and "shoot" not in self.shooter.current_state:
            self.__executeEvent(stateMachine, conditionalState, newState)

    def __processShootingEvent(self, stateMachine, sensor, requestedValue, conditionalState, newState):
        """Contains information necessary for executing the shooter."""
        sensorKey = "sensor" + str(sensor)
        if self.digitalInput_breaksensors[sensorKey].get() == requestedValue and self.shooter.current_state != newState:
            self.__executeEvent(stateMachine, conditionalState, newState)

    def __processLEDEvent(self, stateMachine, sensor, requestedValue, conditionalState, newState):
        """Contains information necessary for activating LEDs."""
        sensorKey = "sensor" + str(sensor)
        if self.digitalInput_breaksensors[sensorKey].get() == requestedValue and self.shooter.current_state != newState:
            self.__executeEvent(stateMachine, conditionalState, newState)

    def execute(self):
        """Loads all entries made and runs '__processEvent' for all of them."""
        for entry in self.entries:
            stateMachine = self.entries[entry]["stateMachine"]
            actionType = self.entries[entry]["actionType"]
            sensor = self.entries[entry]["sensor"]
            requestedValue = self.entries[entry]["requestedValue"]
            conditionalState = self.entries[entry]["conditionalState"]
            newState = self.entries[entry]["newState"]

            if actionType == ActionType.kLoading:
                self.__processLoadingEvent(stateMachine, sensor, requestedValue, conditionalState, newState)
            elif actionType == ActionType.kShooter:
                self.__processShootingEvent(stateMachine, sensor, requestedValue, conditionalState, newState)
            elif actionType == ActionType.kLED:
                self.__processLEDEvent(stateMachine, sensor, requestedValue, conditionalState, newState)
