import wpilib
import commands2
import logging
logger = logging.getLogger("WristSubsystem Logger")
from wpilib import XboxController
from constants import OP, SW

from subsystems.ElevatorSubsystem import ElevatorSubsystemClass
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