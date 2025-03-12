import wpilib
import commands2
from subsystems.IntakeSubsystem import IntakeSubsystemClass
import logging
logger = logging.getLogger("Intakesubsystemlogger")
from wpilib import XboxController
from constants import OP


# Intake Commands
class IntakeCommand(commands2.Command):
    def __init__(self, Intakesubsystem: IntakeSubsystemClass) -> None:
        self.Intakesub = Intakesubsystem

    def initialize(self):
        self.Intakesub.Intake()
        logger.info("Intake intake command initialized")

    def isFinished(self):
        return True

class OutakeCommand(commands2.Command):
    def __init__(self, Intakesubsystem: IntakeSubsystemClass) -> None:
        self.Intakesub = Intakesubsystem

    def initialize(self):
        self.Intakesub.Outake()
        logger.info("Intake outake command initialized")

    def isFinished(self):
        return True

class IntakeStop(commands2.Command):
    def __init__(self, Intakesubsystem: IntakeSubsystemClass) -> None:
        self.Intakesub = Intakesubsystem

    def initialize(self):
        self.Intakesub.Stop()
        logger.info("Intake stop initialized")

    def isFinished(self):
        return True