import wpilib
import commands2
import logging
logger = logging.getLogger("WristSubsystem Logger")
from wpilib import XboxController
from constants import OP, SW

from subsystems.ElevatorSubystem import ElevatorSubsystemClass
from subsystems.WristSubsystem import WristSubsystemClass

class ScoringL2(commands2.Command):

    def __init__(self, ElevSub: ElevatorSubsystemClass, WristSubsystem: WristSubsystemClass) -> None:
        self.addRequirements(ElevSub)
        self.addRequirements(WristSubsystem)
        self.ElevatorSub = ElevSub
        self.WristSub = WristSubsystem
        logger.info("reef scoring constructor")

    
    def initialize(self):
        logger.info("reef scoring command initialize")

    def execute(self):
        self.ElevatorSub.normalPID(SW.L2_Setpoint)
        self.WristSub.writPID(SW.Wrist_L2_Setpoint)

    def isFinished(self):
        return False
    
    def end(self, interrupted):
        self.ElevatorSub.elevatorMotorStop()
        self.WristSub.WristStop()
        
class ScoringL3(commands2.Command):

    def __init__(self, ElevSub: ElevatorSubsystemClass, WristSubsystem: WristSubsystemClass) -> None:
        self.addRequirements(ElevSub)
        self.addRequirements(WristSubsystem)
        self.ElevatorSub = ElevSub
        self.WristSub = WristSubsystem
        logger.info("reef scoring constructor")

    
    def initialize(self):
        logger.info("reef scoring command initialize")

    def execute(self):
        self.ElevatorSub.normalPID(SW.L3_Setpoint)
        self.WristSub.writPID(SW.Wrist_L3_Setpoint)

    def isFinished(self):
        return False
    
    def end(self, interrupted):
        self.ElevatorSub.elevatorMotorStop()
        self.WristSub.WristStop()
        
class ScoringL4(commands2.Command):

    def __init__(self, ElevSub: ElevatorSubsystemClass, WristSubsystem: WristSubsystemClass) -> None:
        self.addRequirements(ElevSub)
        self.addRequirements(WristSubsystem)
        self.ElevatorSub = ElevSub
        self.WristSub = WristSubsystem
        logger.info("reef scoring constructor")

    
    def initialize(self):
        logger.info("reef scoring command initialize")

    def execute(self):
        self.ElevatorSub.normalPID(SW.L4_Setpoint)
        self.WristSub.writPID(SW.Wrist_L4_Setpoint)

    def isFinished(self):
        return False
    
    def end(self, interrupted):
        self.ElevatorSub.elevatorMotorStop()
        self.WristSub.WristStop()
        
class BargeScoring(commands2.Command):

    def __init__(self, ElevSub: ElevatorSubsystemClass, WristSubsystem: WristSubsystemClass) -> None:
        self.addRequirements(ElevSub)
        self.addRequirements(WristSubsystem)
        self.ElevatorSub = ElevSub
        self.WristSub = WristSubsystem
        logger.info("reef scoring constructor")

    
    def initialize(self):
        logger.info("reef scoring command initialize")

    def execute(self):
        self.ElevatorSub.normalPID(SW.Barge_Setpoint)
        self.WristSub.writPID(SW.Wrist_Barge_Setpoint)

    def isFinished(self):
        return False
    
    def end(self, interrupted):
        self.ElevatorSub.elevatorMotorStop()
        self.WristSub.WristStop()