import wpilib
import commands2
from subsystems.HangSubsystem import HangSubsystem
import logging
logger = logging.getLogger("hangSubsystem Logger")
from wpilib import XboxController
from constants import OP
import time
        
# hang Manual Commands
class hangForward(commands2.Command):
    def __init__(self, hangSubsytem: HangSubsystem) -> None:
        self.hangSub = hangSubsytem

    def initialize(self):
        logger.info("Hang initialized")

    def execute(self):
        self.hangSub.hangForward()

    def isFinished(self):
        return False
   
    def end(self, interrupted):
        self.hangSub.hangStop()

class hangBackwards(commands2.Command):
    def __init__(self, hangSubsytem: HangSubsystem) -> None:
        self.hangSub = hangSubsytem

    def initialize(self):
        logger.info("Hang initialized")

    def execute(self):
        self.hangSub.hangBackwards()

    def isFinished(self):
        return False
   
    def end(self, interrupted):
        self.hangSub.hangStop()

class hangStop(commands2.Command):
    def __init__(self, hangSubsytem: HangSubsystem) -> None:
        self.hangSub = hangSubsytem

    def initialize(self):
        logger.info("Hang stop")

    def execute(self):
        self.hangSub.hangStop()

    def isFinished(self):
        return False
   
    def end(self, interrupted):
        self.hangSub.hangStop()