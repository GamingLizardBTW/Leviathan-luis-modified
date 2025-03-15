import wpilib
import commands2
from subsystems.WristSubsystem import WristSubsystemClass
import logging
logger = logging.getLogger("WristSubsystem Logger")
from wpilib import XboxController
from constants import OP, SW
import time
        
# Wrist Manual Commands

class wristWithJoystick(commands2.Command):
    def __init__(self, WristSubsytem: WristSubsystemClass) -> None:
        self.WristSub = WristSubsytem

    def initialize(self):
        logger.info(" wrist initialized")

    def execute(self):
        self.inputvalue = XboxController(OP.operator_controller).getRightY()
        if self.inputvalue > 0.1 or self.inputvalue < -0.1:
            self.WristSub.wristWithJoystick(self.inputvalue)
        else:
            self.WristSub.WristStop()

    def isFinished(self):
        return False
   
    def end(self, interrupted):
        self.WristSub.WristStop()
    
    
    
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
        self.WristSub.writPID(SW.Wrist_L2_Setpoint)

    def isFinished(self):
        return False
   
    def end(self, interrupted):
        self.WristSub.WristStop()
        
class WristL3(commands2.Command):
    def __init__(self, WristSubsytem: WristSubsystemClass) -> None:
        self.WristSub = WristSubsytem

    def initialize(self):
        logger.info(" wrist to proccesor")

    def execute(self):
        self.WristSub.writPID(SW.Wrist_L3_Setpoint)

    def isFinished(self):
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
        self.WristSub.writPID(SW.Wrist_L4_Setpoint)

    def isFinished(self):
        return False
   
    def end(self, interrupted):
        self.WristSub.WristStop()
        
class AutoWristL2(commands2.Command):
    def __init__(self, WristSubsytem: WristSubsystemClass) -> None:
        self.WristSub = WristSubsytem

    def initialize(self):
        logger.info(" wrist to robot")

    def execute(self):
        self.WristSub.writPID(SW.Wrist_L2_Setpoint)

    def isFinished(self):
        if self.WristSub.wristPID.atSetpoint():
            return True
        return False
   
    def end(self, interrupted):
        self.WristSub.WristStop()
        
class AutoWristL3(commands2.Command):
    def __init__(self, WristSubsytem: WristSubsystemClass) -> None:
        self.WristSub = WristSubsytem

    def initialize(self):
        logger.info(" wrist to proccesor")

    def execute(self):
        self.WristSub.writPID(SW.Wrist_L3_Setpoint)

    def isFinished(self):
        if self.WristSub.wristPID.atSetpoint():
            return True
        return False
   
    def end(self, interrupted):
        self.WristSub.WristStop()

class AutoWristL4(commands2.Command):
    def __init__(self, WristSubsytem: WristSubsystemClass) -> None:
        self.WristSub = WristSubsytem

    def initialize(self):
        logger.info(" wrist to floor")

    def execute(self):
        self.WristSub.writPID(SW.Wrist_L4_Setpoint)

    def isFinished(self):
        if self.WristSub.wristPID.atSetpoint():
            return True
        return False
   
    def end(self, interrupted):
        self.WristSub.WristStop()