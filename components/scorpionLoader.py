from robotMap import XboxMap

class ScorpionLoader:
    compatString = ["scorpion"]
    motors_shooter: dict
    motors_loader: dict
    xboxMap: XboxMap

    def setup(self):
        self.intakeSpeed = 0
        self.loaderSpeed = 0
        self.shooterSpeed = 0

        self.loaderMotor = self.motors_loader["loaderMotor"]
        self.intakeMotor = self.motors_loader["intakeMotor"]
        self.logger.info("Shooter Motor Component Created")

    def runLoader(self, lSpeed):
        self.loaderSpeed = lSpeed
        self.loader = True

    def runIntake(self, iSpeed):
        self.intakeSpeed = iSpeed
        self.intake = True

    def stopIntake(self):
        self.intake = False

    def stopLoader(self):
        self.loader = False

    def isLoaderActive(self):
        return self.loader

    def checkController(self):
        self.runIntake(self.xboxMap.mechLeft)
        self.runLoader(self.xboxMap.mechRight)

    def execute(self):
        if self.intake:
            self.intakeMotor.set(self.intakeSpeed)
        elif self.intake == False:
            self.intakeMotor.set(0)

        if self.loader:
            self.loaderMotor.set(self.loaderSpeed)
        elif self.loader == False:
            self.loaderMotor.set(0)
