import wpilib
import commands2
import logging
logger = logging.getLogger("WristSubsystem Logger")
from wpilib import XboxController
from constants import OP, SW

from subsystems.MotionMagicExample import MotionMagicClass

class MotionWithJoystick(commands2.Command):

    def __init__(self, motionSub: MotionMagicClass) -> None:
        self.addRequirements(motionSub)
        self.MotionSub = motionSub

    
    def initialize(self):
        logger.info("Motion Magic Command")

    def execute(self):
        self.MotionSub.motionMagic()

    def isFinished(self):
        return False
    
    def end(self, interrupted):
        pass