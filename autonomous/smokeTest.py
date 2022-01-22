from magicbot import AutonomousStateMachine, state, timed_state, feedback
from components.driveTrain import DriveTrain
from components.colorSensor import ColorSensor
import logging as log

class SmokeTest(AutonomousStateMachine):
    compatString = ["greenChassis", "doof"]
    MODE_NAME= "Smoke Test"
    driveTrain: DriveTrain
    colorSensor: ColorSensor
    #DEFAULT = True
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
        """
        Sets the LED on the color sensor to strobe and
        requires user input to advance to the next state
        """
        pass

    @state
    def checkEncoders(self):
        pass

    @state
    def checkBreakSensors(self):
        """
        Create one for each break sensor,
        would move on to the next one when
        the one requested is broken
        """
        pass
