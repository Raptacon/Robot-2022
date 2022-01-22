from magicbot import AutonomousStateMachine, state, timed_state, feedback
from components.driveTrain import DriveTrain
#from components.breakSensors import S
from components.colorSensor import ColorSensor
import logging as log

class SmokeTest(AutonomousStateMachine):

    MODE_NAME= "Smoke Test"
    driveTrain: DriveTrain
    colorSensor: ColorSensor
    toDo = None

    @feedback
    def getToDo(self):
        return self.toDo

    @state(first = True)
    def drive(self):
        """Tests to see if the motors are working with an input from the driver"""
        self.toDo = "Drive motors forwards"
        if self.driveTrain.tankLeftSpeed > 0 and self.driveTrain.tankRightSpeed > 0:
            self.next_state("colorSensorCheck")
        else:
            log.error("Not driving forwards")
    
    @state
    def colorSensorCheck(self):
        """Sets the LED on the color sensor to strobe and requires user input to advance to the next state"""
        self.toDo = "Check to see if color sensor LED is flashing"
        self.colorSensor.colorSensor.LEDPulseFrequency(value = 60)

    @state
    def checkGoToDist(self):
        """Checks to see if goToDist is working by making it drive forwards a certain distance"""
        pass

    @state
    def checkTurnToAngle(self):
        """Checks to see if turnToAngle is working by making it turn to a certain angle"""
        pass

    @state
    def checkEncoders(self):
        pass

    @state
    def checkBreakSensors(self):
        """Create one for each break sensor, """
        pass
