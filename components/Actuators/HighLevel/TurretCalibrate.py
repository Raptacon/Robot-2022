
from magicbot import StateMachine, state
from components.Actuators.AutonomousControl.turretTurn import TurretTurn
from components.Actuators.LowLevel.turretThreshold import TurretThreshold
from networktables import NetworkTables as networktable
class CalibrateTurret(StateMachine):
    compatString = ["doof", "greenChassis", "newBot"]
    clicked = False
    #a dummy variable until we find something else
    turretTurn: TurretTurn
    turretThreshold: TurretThreshold
    const_turnAngle = 5
    limitSwitchTable = networktable.getTable("LimitSwitch")

    @state(first = True)
    def findRightdeadzone(self):
        while self.clicked == False:
            self.turretThreshold.angleCheck(self.const_turnAngle)
            self.const_turnAngle += 1
            self.turretThreshold.setTurretspeed()
            self.turretTurn.engage()

            if self.clicked == True:
                self.limitR = self.turretThreshold.getPosition()
                self.next_state('findLeftdeadzone')
                self.clicked = False
                break


    @state
    def findLeftdeadzone(self):
        while self.clicked == False:
            self.turretThreshold.angleCheck(self.const_turnAngle)
            self.const_turnAngle -= 1
            self.turretThreshold.setTurretspeed()
            self.turretTurn.engage()
            if self.clicked == True:
                self.limitL = self.turretThreshold.getPosition()
                self.next_state('foundDeadzones')

    @state
    def foundDeadzones(self):
        self.limitSwitchTable = self.limitSwitchTable.getNumber(self.limitL, self.limitR)
        self.done()
        return self.limitSwitchTable


