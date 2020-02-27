class ShooterMotorCreation:
    compatString = ["doof"]
    motors_shooter: dict
    motors_loader: dict

    def on_enable(self):
        self.intakeSpeed = 0
        self.loaderSpeed = 0
        self.shooterSpeed = 0
        self.intake = False
        self.loader = False
        self.shooter = False

        self.loaderMotor = self.motors_loader["loaderMotor"]
        self.intakeMotor = self.motors_loader["intakeMotor"]
        self.shooterMotor = self.motors_shooter["shooterMotor"]

        self.logger.info("Shooter Motor Component Created")

    def runLoader(self, lSpeed):
        self.loaderSpeed = lSpeed
        self.loader = True

    def runIntake(self, iSpeed):
        self.intakeSpeed = iSpeed
        self.intake = True

    def runShooter(self, sSpeed):
        self.shooterSpeed = sSpeed
        self.shooter = True

    def stopIntake(self):
        self.intake = False

    def stopLoader(self):
        self.loader = False

    def stopShooter(self):
        self.shooter = False

    def getLoaderStatus(self):
        return self.loader

    def execute(self):
        if self.intake:
            self.intakeMotor.set(self.intakeSpeed)
        elif self.intake == False:
            self.intakeMotor.set(0)

        if self.loader:
            self.loaderMotor.set(self.loaderSpeed)
        elif self.loader == False:
            self.loaderMotor.set(0)

        if self.shooter:
            self.shooterMotor.set(self.shooterSpeed)
        elif self.shooter == False:
            self.shooterMotor.set(0)
