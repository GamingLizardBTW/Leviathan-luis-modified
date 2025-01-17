import wpilib
import commands2
from subsystems.AlgaeSubsystem import AlgaeSubsystemClass
import logging
logger = logging.getLogger("algaesubsystemlogger")
from wpilib import XboxController
import phoenix6

class AlgaeWithTriggers(commands2.Command):
    def __init__(self, algaesubsystem: AlgaeSubsystemClass) -> None:
        self.addRequirements(algaesubsystem)
        self.algaesub = algaesubsystem

    def initialize(self):
        logger.info("algae intake command initialized")

    def execute(self):
        self.lefttrigger = XboxController(1).getLeftTriggerAxis()
        self.righttrigger = XboxController(1).getRightTriggerAxis()
        self.calculated_input = self.righttrigger - self.lefttrigger
        if self.calculated_input >= 0.05:
            self.algaesub.algaeintake()
        elif self.calculated_input <= -0.05:
            self.algaesub.algaeoutake()
        else:
            self.algaesub.algaestop()
        logger.info("x")

    def isFinished(self):
        return False
   
    def end(self, interrupted):
        self.algaesub.algaestop()

class AlgaeIntakeCommand(commands2.Command):
    def __init__(self, algaesubsystem: AlgaeSubsystemClass) -> None:
        self.algaesub = algaesubsystem

    def initialize(self):
        logger.info("algae intake command initialized")

    def execute(self):
        self.algaesub.algaeintake()
        logger.info("intaking")

    def isFinished(self):
        return False
   
    def end(self, interrupted):
        self.algaesub.algaestop()

class AlgaeOutakeCommand(commands2.Command):
    def __init__(self, algaesubsystem: AlgaeSubsystemClass) -> None:
        self.algaesub = algaesubsystem

    def initialize(self):
        logger.info("algae outake command initialized")

    def execute(self):
        self.algaesub.algaeoutake()
        logger.info("outaking")

    def isFinished(self):
        return False
   
    def end(self, interrupted):
        self.algaesub.algaestop()

class AlgaeStop(commands2.Command):
    def __init__(self, algaesubsystem: AlgaeSubsystemClass) -> None:
        self.algaesub = algaesubsystem

    def initialize(self):
        logger.info("algae stop initialized")

    def execute(self):
        self.algaesub.algaestop()
        logger.info("stopping")

    def isFinished(self):
        return False
   
    def end(self, interrupted):
        self.algaesub.algaestop()