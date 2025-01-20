import wpilib
import commands2
from subsystems.CoralSubsystem import CoralSubsystemClass
import logging
logger = logging.getLogger("coralsubsystemlogger")
import phoenix6

class CoralIntake(commands2.Command):
    def __init__(self, coralsubsystem: CoralSubsystemClass) -> None:
        self.coralsub = coralsubsystem

    def initialize(self):
        logger.info("coral intake command initialized")

    def execute(self):
        self.coralsub.coralintake()
        logger.info("coral intake running")

    def isFinished(self):
        return False
    
    def end(self, interrupted):
        self.coralsub.coralstop()

class CoralOuttake(commands2.Command):
    def __init__(self, coralsubsystem: CoralSubsystemClass) -> None:
        self.coralsub = coralsubsystem

    def initialize(self):
        logger.info("coral outtake command initialized")

    def execute(self):
        self.coralsub.coralouttake()
        logger.info("coral outtake running")

    def isFinished(self):
        return False

    def end(self, interrupted):
        self.coralsub.coralstop()

class CoralStop(commands2.Command):
    def __init__(self, coralsubsystem: CoralSubsystemClass) -> None:
        self.coralsub = coralsubsystem

    def initialize(self):
        logger.info("coral stop command initialized")

    def execute(self):
        self.coralsub.coralstop()
        logger.info("coral stop running")

    def isFinished(self):
        return False
    
    def end(self, interrupted):
        self.coralsub.coralstop()
        

