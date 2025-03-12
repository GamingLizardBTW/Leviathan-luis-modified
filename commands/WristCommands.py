import wpilib
import commands2
from subsystems.WristSubsystem import WristSubsystemClass
import logging
logger = logging.getLogger("WristSubsystem Logger")
from wpilib import XboxController
from constants import OP
import time
        
# Wrist Manual Commands
class WristForward(commands2.Command):
    def __init__(self, WristSubsytem: WristSubsystemClass) -> None:
        self.WristSub = WristSubsytem

    def initialize(self):
        logger.info(" wrist initialized")

    def execute(self):
        self.WristSub.wristForward()

    def isFinished(self):
        return False
   
    def end(self, interrupted):
        self.WristSub.WristStop()

class WristBackwards(commands2.Command):
    def __init__(self, WristSubsytem: WristSubsystemClass) -> None:
        self.WristSub = WristSubsytem

    def initialize(self):
        logger.info(" wrist initialized")

    def execute(self):
        self.WristSub.wristBackwards()
        logger.info("outaking")

    def isFinished(self):
        return False
   
    def end(self, interrupted):
        self.WristSub.WristStop()

class WristStop(commands2.Command):
    def __init__(self, WristSubsytem: WristSubsystemClass) -> None:
        self.WristSub = WristSubsytem

    def initialize(self):
        logger.info(" wrist stop")

    def execute(self):
        self.WristSub.WristStop()

    def isFinished(self):
        return False
   
    def end(self, interrupted):
        self.WristSub.WristStop()

# Wrist PID Commands
class WristL2(commands2.Command):
    def __init__(self, WristSubsytem: WristSubsystemClass) -> None:
        self.WristSub = WristSubsytem

    def initialize(self):
        logger.info(" wrist to robot")

    def execute(self):
        self.WristSub.WristL2()

    def isFinished(self):
        if self.WristSub.wristPID.atSetpoint():
            return True
        return False
   
    def end(self, interrupted):
        self.WristSub.WristStop()
        
class WristL3(commands2.Command):
    def __init__(self, WristSubsytem: WristSubsystemClass) -> None:
        self.WristSub = WristSubsytem

    def initialize(self):
        logger.info(" wrist to proccesor")

    def execute(self):
        self.WristSub.WristL3()

    def isFinished(self):
        if self.WristSub.wristPID.atSetpoint():
            return True
        return False
   
    def end(self, interrupted):
        XboxController(OP.driver_controller).setRumble(XboxController.RumbleType(2), 0.8)
        self.WristSub.WristStop()
        time.sleep(.3)

class WristL4(commands2.Command):
    def __init__(self, WristSubsytem: WristSubsystemClass) -> None:
        self.WristSub = WristSubsytem

    def initialize(self):
        logger.info(" wrist to floor")

    def execute(self):
        self.WristSub.WristL4()

    def isFinished(self):
        return False
   
    def end(self, interrupted):
        self.WristSub.WristStop()