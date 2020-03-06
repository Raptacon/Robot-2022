from utils.magicbotStrict import StrictStateMachine, state
import utils.magicbotStrict
print(dir(utils.magicbotStrict))

class Stroll(StrictStateMachine):
    flowerStates = ["smelling"]
    
    @state(first=True, state_transitions=["walking"])
    def smellingFlowers(self, state_tm):
        """This happens first"""
        print("Smelling flowers")
        if(self.valid_change("invalid")):
            self.next_state("invalid")
        else:
            if state_tm < .05:
                print("Sad day I can't goto Invalid")
                self.next_state("invalid", force=True)
        
        if state_tm > 2:
            self.next_state("walking")

    @state(state_transitions=["smellingFlowers", "picking"])
    def walking(self):
        print("Walking...")
        self.next_state("picking")


    @state
    def picking(self):
        print("Picked a flower")
        self.next_state("smellingFlowers")
        self.next_state("smellingFlowers")


    @state
    def invalid(self):
        print("Invalid state")

    def execute(self):
        self.engage()
        super().execute()
