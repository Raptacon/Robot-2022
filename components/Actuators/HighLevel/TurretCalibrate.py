from magicbot import state_machine, state

class CalibrateTurret(state_machine):
    compatString = ["doof", "greenChassis", "newBot"]
    clicked = False
    #a dummy variable until

    @state(first = True)
    def findReftdeadzone(self):
        pass


