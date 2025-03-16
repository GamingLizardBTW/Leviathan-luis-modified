import wpilib
import commands2
from subsystems.IntakeSubsystem import IntakeSubsystemClass
import logging
logger = logging.getLogger("Intakesubsystemlogger")
from wpilib import XboxController, Timer
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
    
class AutoIntakeCommand(commands2.Command):
    def __init__(self, Intakesubsystem: IntakeSubsystemClass) -> None:
        self.Intakesub = Intakesubsystem

    def initialize(self):
        logger.info("Intake intake command initialized")
        
    def execute(self):
        self.Intakesub.Intake()

    def isFinished(self):
        if self.Intakesub.beamBreak.get() == True:
            Timer.start()
            if Timer.get() >= 1:
                return True
        else:
            return False
        
    def end(self, interrupted: bool):
        Timer.reset()
        self.Intakesub.Stop()
        
class AutoOuttakeCommand(commands2.Command):
    def __init__(self, Intakesubsystem: IntakeSubsystemClass) -> None:
        self.Intakesub = Intakesubsystem

    def initialize(self):
        logger.info("auto outtake command initialized")
        Timer.start()
        
    def execute(self):
        self.Intakesub.Outake()

    def isFinished(self):
        if Timer.get() >= 2:
            return True
        else:
            return False
        
    def end(self, interrupted: bool):
        Timer.reset()
        self.Intakesub.Stop()