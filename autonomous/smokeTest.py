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
        self.toDo = "Drive motors forwards"
        if self.driveTrain.tankLeftSpeed > 0 and self.driveTrain.tankRightSpeed > 0:
            self.next_state("colorSensorCheck")
        else:
            log.error("Not driving forwards")
    
    @state
    def colorSensorCheck(self):
        self.toDo = "Check to see if color sensor LED is flashing"
        self.colorSensor.colorSensor.LEDPulseFrequency(value = 60)
        
