from magicbot import StateMachine, state, tunable
from components.Actuators.LowLevel.turretThreshold import TurretThreshold

class turretTurn(StateMachine):
    compatString = ["doof", "greenChassis"]
    motors_turret: dict
    turretThreshold: TurretThreshold
    turnAngle = 0
    tolerance = tunable(0.5)
    values = [
             [20, .15], # The first value is the limit, so it will
             [45, .2],  # use the included speed if the distance is
             [90, .25],# under this value and above the last.
             [180, .3],
             ["End", .4]
             ]  # The array must end with "End" - this will be the value used
    # if the target is really far away.

    def on_enable(self):
        #sets up position and connects motors
        self.turretMotor = self.motors_turret["turretMotor"]

    def setAngle(self, angle):
        #gets angle turret is turning to
        self.turnAngle = self.turretThreshold.angleCheck(angle)

    @state(first = True)
    def idling(self):
        """Stays in this state until started"""
        if self.turnAngle != 0:
            self.next_state("turn")
        else:
            self.next_state("idling")

    def setSpeed(self, angle):
        #Sets speed of turret based on what angle we are turning to
        self.pos = self.turretMotor.getEncoder().getPosition()
        for distTotargetAngle, speed in self.values:
            if (distTotargetAngle == "End"
                or self.pos < distTotargetAngle):
                self.turretThreshold.setTurretspeed(speed)
                break

    @state
    def turn(self, angle):
        #Starts turning process, if in tolerance it will stop
        self.setSpeed()
        if self.pos < (self.turnAngle + self.tolerance) and self.pos > (self.turnAngle - self.tolerance):
            self.stop()
        else:
            self.next_state("turn")

    def stop(self):
        #stops turret
        self.next_state("idling")
        self.turretThreshold.stopTurret()
