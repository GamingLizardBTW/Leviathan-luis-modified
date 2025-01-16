import wpilib
import commands2
from subsystems.WristSubsystem import WristSubsystemClass
import logging
logger = logging.getLogger("WristSubsystem Logger")
from wpilib import XboxController
from constants import OP

class WristWithJoysticks(commands2.Command):

    def __init__(self, WristSubsytem: WristSubsystemClass) -> None:
        self.addRequirements(WristSubsytem)
        self.WristSub = WristSubsytem
        logger.info("wrist with joystick constructor")

    
    def initialize(self):
        logger.info("wrist with joystick initialize")

    def execute(self):
        self.inputvalue = XboxController(OP.operator_controller).getRightY()
        self.WristSub.wristwithjoystick(self.inputvalue)
        logging.info("Running motor")

    def isFinished(self):
        return False
    
    def end(self, interrupted):
        self.WristSub.wristmotorstop()

class WristMotorStop(commands2.Command):
    
    def __init__(self, WristSubsytem: WristSubsystemClass) -> None:
        self.WristSub = WristSubsytem
        logger.info("wrist motor stop constructor")
    
    def initialize(self):
        logger.info("wrist motor stop initialize")

    def execute(self):
        self.WristSub.wristmotorstop()
        logger.info("stopping")

    def isFinished(self):
        return False
    
    def end(self, interrupted):
        self.WristSub.wristmotorstop()
