from enum import Enum


class ServoPosition(Enum):
    kForward = 1
    kBackward = 0


class Servos:
    """
    This class' only purpose is to put the servo down and up once.
    If you want to make it more useful, go ahead.
    """
    compatString = ["teapot"]
    digitalServos_servos: dict
    complete = False
    servoName = "rampServo"

    def getServo(self, servoName:str):
        """
        Returns a servo if servoName is included in dict
        """
        if servoName in self.digitalServos_servos:
            return self.digitalServos_servos[servoName]
        else:
            return None

    def execute(self):
        """
        Moves the servo forwards if it hasn't yet
        """
        servo = self.getServo(self.servoName)
        if not self.complete:
            servo.set(ServoPosition.kForward)
            if abs(servo.get() - ServoPosition.kForward) < self.tolerance:
                self.complete = True
                servo.set(ServoPosition.kBackward)
        else:
            servo.set(ServoPosition.kBackward)

