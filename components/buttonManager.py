"""
Manager class to turn HID buttons into events
"""
import wpilib
from enum import Flag, auto
import inspect
import traceback

class ButtonEvent(Flag):
    """
    Supported button actions
    """
    kOnPress = auto()
    kOnRelease = auto()
    kWhilePressed = auto()
    kWhileReleased = auto()
    kNone = 0

class ButtonManager:
    """
    Class manages the buttons on a HID device. If a HID device is registered users should not
    use any registered buttons directley.
    """

    #def __init__():
    #    """
    #    Initilizer for class
    #    """
    #    self.entrys = {}

    def __createCallbackEntry(self, hidDevice, buttonId, eventTypes, callback):
        """
        Private method for creating a callback entry
        """
        if hidDevice not in self.entrys:
            self.entrys[hidDevice] = {}
            self.enabledTypes[hidDevice] = {}
        if buttonId not in self.entrys[hidDevice]:
            self.entrys[hidDevice][buttonId] = []
            self.enabledTypes[hidDevice][buttonId] = ButtonEvent.kNone
        

        entry = {}
        entry["hidDevice"] = hidDevice
        entry["buttonId"] = buttonId
        entry["eventTypes"] = eventTypes
        entry["callback"] = callback
        entry["triggerCount"] = {}
        #TODO validate entry does not exist
        self.entrys[hidDevice][buttonId].append(entry)
        self.enabledTypes[hidDevice][buttonId] |= eventTypes
        return entry

    def __entryStr(self, entry):
        """
        Private: Returns string rep for entry
        """
        retVal = f'{entry["hidDevice"].getName()}:{str(entry["buttonId"])} for {str(entry["eventTypes"])}'
        for key,value in entry["triggerCount"]:
            retVal = retVal + f"\n[{str(key)}: {str(value)}]"

        return retVal

    def setup(self):
        """
        Sets up Button manager.
        """
        #update to change logging level
        #self.logger.setLevel(logging.DEBUG)
        
        self.entrys = {}
        self.enabledTypes = {}

    def registerButtonEvent(self, hidDevice, buttonId, eventTypes: ButtonEvent, callback):
        """
        Registered a button on a HID for eventType. When even type is triggered, callback is invoked.
        Callback must take form of callable(**kwargs). See exampleCallback. It may be of type self.callable
        where self is a class instance
        """
        assert isinstance(hidDevice, wpilib.interfaces.GenericHID), f"{str(hidDevice)} is not a HID"
        #assert buttonId > 0 and buttonId < 16, f"Invalid button ID {str(buttonId)}"
        assert isinstance(eventTypes, ButtonEvent), f"{eventTypes} is not an eventTypes"
        assert callable(callback), f"{str(callback)} must be callable"
        
        entry = self.__createCallbackEntry(hidDevice, buttonId, eventTypes, callback)
        self.logger.info(f"Registering event [{self.__entryStr(entry)}]")

    def getregisteredEvent(self, hidDevice, buttonId, callback):
        """
        Finds matching callback for a given hidDevice, buttonId, and callback
        Can be used to get call counts
        """
        #TODO test and cleanup
        try:
            entrys = self.entrys[hidDevice][buttonId]
            for entry in entrys:
                if callback == entrys[entry]["callback"]:
                    return entry
        except Exception as e:
            print(e)
        return None

    def __processEvent(self, entrys, action):
        """
        Private: Process all entrys when action occurs
        """
        for entry in entrys:
            #Check if entry is valid for action
            if not (action & entry["eventTypes"]):
                #if not enabled for this action, do not process
                continue
            
            #track metrics
            if not action in entry["triggerCount"]:
                entry["triggerCount"][action] = 0
            entry["triggerCount"][action] +=1
            callback = entry["callback"]
            args, varargs, varkw, defaults = inspect.getargspec(callback)
            try:
                if(varkw):
                    #takes kwargs
                    callback(action = action, **entry)
                else:
                    #no varargs, so assume no arguments
                    callback()
            except Exception as e:
                self.logger.error(f"{str(callback)} crashed. E is {str(e)}")
                traceback.print_exc()

    def __runOnPressed(self, hidDevice: wpilib.interfaces.GenericHID, button, enabledActions, entrys):
        """
        Private: checks button pressed
        """
        if not enabledActions & ButtonEvent.kOnPress:
            return
        #note that when getRawButtonPressed is called it resets the value
        wasButtonPressed = hidDevice.getRawButtonPressed(button)
        if wasButtonPressed:
            self.logger.debug("__runOnPressed: %s:%s", hidDevice.getName, str(button))
            self.__processEvent(entrys, ButtonEvent.kOnPress)

    def __runOnReleased(self, hidDevice: wpilib.interfaces.GenericHID, button, enabledActions, entrys):
        """
        Private Processes event type
        """
        if not enabledActions & ButtonEvent.kOnRelease:
            return
        wasButtonReleased = hidDevice.getRawButtonReleased(button)
        if wasButtonReleased:
            self.logger.debug("__runOnReleased: %s:%s", hidDevice.getName, str(button))
            self.__processEvent(entrys, ButtonEvent.kOnRelease)
        
    def __runWhilePressed(self, hidDevice: wpilib.interfaces.GenericHID, button, enabledActions, entrys):
        """
        Private Processes event type
        """
        if not enabledActions & ButtonEvent.kWhilePressed:
            return
        isButtonPressed = hidDevice.getRawButton(button)
        if isButtonPressed:
            self.logger.debug("__runWhilePressed: %s:%s", hidDevice.getName, str(button))
            self.__processEvent(entrys, ButtonEvent.kWhilePressed)
    def __runWhileReleased(self, hidDevice: wpilib.interfaces.GenericHID, button, enabledActions, entrys):
        """
        Private Processes event type
        """
        if not enabledActions & ButtonEvent.kWhileReleased:
            return
        isButtonReleased = not hidDevice.getRawButton(button)
        if isButtonReleased:
            self.logger.debug("__runWhileReleased: %s:%s", hidDevice.getName, str(button))
            self.__processEvent(entrys, ButtonEvent.kWhileReleased)

    def execute(self):
        """
        Process button events each cycle
        """
        for hidDevice in self.entrys:
            for button in self.entrys[hidDevice]:
                entrys = self.entrys[hidDevice][button]

                enabledActions = self.enabledTypes[hidDevice][button]
                
                #check each event type
                self.__runOnPressed(hidDevice, button, enabledActions, entrys)
                self.__runOnReleased(hidDevice, button, enabledActions, entrys)
                self.__runWhilePressed(hidDevice, button, enabledActions, entrys)
                self.__runWhileReleased(hidDevice, button, enabledActions, entrys)
