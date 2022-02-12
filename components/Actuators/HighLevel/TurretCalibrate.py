from magicbot import state_machine, state

class CalibrateTurret(state_machine):
    compatString = ["doof", "greenChassis", "newBot"]
    clicked = False
    #a dummy variable until we find something else

    @state(first = True)
    def findRightdeadzone(self):
        pass


