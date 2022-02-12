
from magicbot import state_machine, state
from components.Actuators.AutonomousControl.turretTurn import TurretTurn
class CalibrateTurret(state_machine):
    compatString = ["doof", "greenChassis", "newBot"]
    clicked = False
    #a dummy variable until we find something else
    turretTurn: TurretTurn

    @state(first = True)
    def findRightdeadzone(self):
        while self.clicked == False:
            self.turretTurn()
            if self.clicked == True:
                self.limitR = self.turretTurn.setup()
                self.next_state('findLeftdeadzone')


    @state
    def findLeftdeadzone(self):




