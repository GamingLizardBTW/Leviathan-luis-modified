import wpilib
import commands2
from subsystems.AlgaeSubsystem import AlgaeSubsystemClass
import logging
logger = logging.getLogger("algaesubsystemlogger")
from wpilib import XboxController
import phoenix6
from constants import OP

class AlgaeWithTriggers(commands2.Command):
    def __init__(self, algaesubsystem: AlgaeSubsystemClass) -> None:
        self.addRequirements(algaesubsystem)
        self.algaesub = algaesubsystem

    def initialize(self):
        logger.info("algae intake command initialized")

    def execute(self):
        self.lefttrigger = XboxController(OP.operator_controller).getLeftTriggerAxis()
        self.righttrigger = XboxController(OP.operator_controller).getRightTriggerAxis()
        self.calculated_input = self.righttrigger - self.lefttrigger
        if self.calculated_input >= 0.05:
            self.algaesub.algaeintake()
        elif self.calculated_input <= -0.05:
            self.algaesub.algaeoutake()
        else:
            self.algaesub.algaestop()
        #logger.info("x")

    def isFinished(self):
        return False
   
    def end(self, interrupted):
        self.algaesub.algaestop()

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
        if self.algaesub.wristToFloor():
            self.algaesub.algaeintake()

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
        return False
   
    def end(self, interrupted):
        self.algaesub.algaeWristStop()

class resetWristEncoder(commands2.Command):
    def __init__(self, algaesubsystem: AlgaeSubsystemClass) -> None:
        self.algaesub = algaesubsystem

    def initialize(self):
        logger.info("Wrist PID offset reset")

    def execute(self):
        self.algaesub.resetPIDOffset()

    def isFinished(self):
        return False
   
    def end(self, interrupted):
        self.algaesub.resetPIDOffset()