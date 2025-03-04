import wpilib
import commands2
from subsystems.AlgaeSubsystem import AlgaeSubsystemClass
import logging
logger = logging.getLogger("algaesubsystemlogger")
from wpilib import XboxController
from constants import OP
import time


# Intake Commands
class AlgaeIntakeCommand(commands2.Command):
    def __init__(self, algaesubsystem: AlgaeSubsystemClass) -> None:
        self.algaesub = algaesubsystem

    def initialize(self):
        self.algaesub.algaeintake()
        logger.info("algae intake command initialized")

    def isFinished(self):
        return True

class AlgaeOutakeCommand(commands2.Command):
    def __init__(self, algaesubsystem: AlgaeSubsystemClass) -> None:
        self.algaesub = algaesubsystem

    def initialize(self):
        self.algaesub.algaeoutake()
        logger.info("algae outake command initialized")

    def isFinished(self):
        return True

class AlgaeStop(commands2.Command):
    def __init__(self, algaesubsystem: AlgaeSubsystemClass) -> None:
        self.algaesub = algaesubsystem

    def initialize(self):
        self.algaesub.algaestop()
        logger.info("algae stop initialized")

    def isFinished(self):
        return True


# Wrist Commands
class AlgaeWristForward(commands2.Command):
    def __init__(self, algaesubsystem: AlgaeSubsystemClass) -> None:
        self.algaesub = algaesubsystem

    def initialize(self):
        logger.info("algae wrist initialized")

    def execute(self):
        self.algaesub.wristForward()

    def isFinished(self):
        return False
   
    def end(self, interrupted):
        self.algaesub.algaeWristStop()

class AlgaeWristBackwards(commands2.Command):
    def __init__(self, algaesubsystem: AlgaeSubsystemClass) -> None:
        self.algaesub = algaesubsystem

    def initialize(self):
        logger.info("algae wrist initialized")

    def execute(self):
        self.algaesub.wristBackwards()
        logger.info("outaking")

    def isFinished(self):
        return False
   
    def end(self, interrupted):
        self.algaesub.algaeWristStop()

class AlgaeWristStop(commands2.Command):
    def __init__(self, algaesubsystem: AlgaeSubsystemClass) -> None:
        self.algaesub = algaesubsystem

    def initialize(self):
        logger.info("algae wrist stop")

    def execute(self):
        self.algaesub.algaeWristStop()

    def isFinished(self):
        return False
   
    def end(self, interrupted):
        self.algaesub.algaeWristStop()

class AlgaeWristToFloor(commands2.Command):
    def __init__(self, algaesubsystem: AlgaeSubsystemClass) -> None:
        self.algaesub = algaesubsystem

    def initialize(self):
        logger.info("algae wrist to floor")

    def execute(self):
        self.algaesub.wristToFloor()

    def isFinished(self):
        return False
   
    def end(self, interrupted):
        self.algaesub.algaeWristStop()
        self.algaesub.algaestop()

class AlgaeWristToRobot(commands2.Command):
    def __init__(self, algaesubsystem: AlgaeSubsystemClass) -> None:
        self.algaesub = algaesubsystem

    def initialize(self):
        logger.info("algae wrist to robot")

    def execute(self):
        self.algaesub.wristToRobot()

    def isFinished(self):
        if self.algaesub.wristPID.atSetpoint():
            return True
        return False
   
    def end(self, interrupted):
        self.algaesub.algaeWristStop()
        
class AlgaeWristToProccesor(commands2.Command):
    def __init__(self, algaesubsystem: AlgaeSubsystemClass) -> None:
        self.algaesub = algaesubsystem

    def initialize(self):
        logger.info("algae wrist to proccesor")

    def execute(self):
        self.algaesub.wristToProcesor()

    def isFinished(self):
        if self.algaesub.wristPID.atSetpoint():
            return True
        return False
   
    def end(self, interrupted):
        XboxController(OP.driver_controller).setRumble(XboxController.RumbleType(2), 0.8)
        time.sleep(.3)
        self.algaesub.algaeWristStop()