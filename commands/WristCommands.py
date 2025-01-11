import wpilib
import commands2
from subsystems.WristSubsystem import WristSubsystemClass
import logging
logger = logging.getLogger("WristSubsystem Logger")

class WristWithJoysticks(commands2.Command):

    def __init__(self, WristSubsytem: WristSubsystemClass, joystickinput: float) -> None:
        self.WristSub = WristSubsytem
        self.inputvalue = joystickinput
    
    def initialize(self):
        logger.info("wrist with joystick initialize")

    def execute(self):
        self.WristSub.wristwithjoystick(self.inputvalue)
        logging.info("Running motor")

    def isFinished(self):
        return False
    def end(self, interrupted):
        self.WristSub.wristmotorstop()

class WristMotorStop(commands2.Command):
    
    def __init__(self, WristSubsytem: WristSubsystemClass) -> None:
        self.WristSub = WristSubsytem
    
    def initialize(self):
        logger.info("wrist motor stop initialize")

    def execute(self):
        self.WristSub.wristmotorstop()
        logger.info("stopping")

    def isFinished(self):
        return False
    
    def end(self, interrupted):
        self.WristSub.wristmotorstop()
