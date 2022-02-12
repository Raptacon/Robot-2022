from magicbot import state_machine, state

class CalibrateTurret(state_machine):
    compatString = ["doof", "greenChassis", "newBot"]

    @state(first = True)
    def findLeftDeadzone(self):
        pass


