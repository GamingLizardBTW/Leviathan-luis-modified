import wpilib
import commands2
from subsystems.AlgaeSubsystem import AlgaeSubsystemClass
import logging
logger = logging.getLogger("algaesubsystemlogger")

class AlgaeWithTriggers(commands2.Command):
    def __init__(self, algaesubsystem: AlgaeSubsystemClass, lefttrigger: float, righttrigger: float) -> None:
        super().__init__()
        self.addRequirements(algaesubsystem)
        self.algaesub = algaesubsystem
        self.lefttrigger = lefttrigger
        self.righttrigger = righttrigger

    def initialize(self):
        logger.info("algae intake command initialized")

    def execute(self):
        self.calculated_input = self.righttrigger - self.lefttrigger
        if self.calculated_input >= 0.05:
            self.algaesub.algaeintake()
        elif self.calculated_input <= 0.05:
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
        super().__init__()
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
        super().__init__()
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
        super().__init__()
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