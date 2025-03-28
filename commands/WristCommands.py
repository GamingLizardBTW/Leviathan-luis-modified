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
        self.addRequirements(self.WristSub)

    def initialize(self):
        logger.info(" wrist initialized")

    def execute(self):
        self.inputvalue = XboxController(OP.operator_controller).getRightY()
        if self.inputvalue > 0.13 or self.inputvalue < -0.13:
            self.WristSub.wristwithjoystick(self.inputvalue)
        else:
            self.WristSub.WristStop()

    def isFinished(self):
        return False
   
    def end(self, interrupted):
        self.WristSub.WristStop()



#======================================= Teleop =======================================================

# Wrist PID Commands
class WristL2(commands2.Command):
    def __init__(self, WristSubsytem: WristSubsystemClass) -> None:
        self.WristSub = WristSubsytem

    def initialize(self):
        logger.info(" wrist to L2")

    def execute(self):
        # self.WristSub.wristMotionMagic(SW.Wrist_L2_Setpoint)
            
        if self.WristSub.coralMode:
            self.WristSub.wristMotionMagic(SW.Wrist_L2_Setpoint)
        else:
            self.WristSub.wristMotionMagic(SW.Algae_L2_Setpoint)

    def isFinished(self):
        return False
   
    def end(self, interrupted):
        print("MotionMagic to L2 Ended")
        self.WristSub.WristStop()
        
class WristL3(commands2.Command):
    def __init__(self, WristSubsytem: WristSubsystemClass) -> None:
        self.WristSub = WristSubsytem

    def initialize(self):
        logger.info(" wrist to L3")

    def execute(self):
        if self.WristSub.coralMode:
            self.WristSub.wristMotionMagic(SW.Wrist_L3_Setpoint)
        else:
            self.WristSub.wristMotionMagic(SW.Algae_L3_Setpoint)

    def isFinished(self):
        return False
   
    def end(self, interrupted):
        # XboxController(OP.driver_controller).setRumble(XboxController.RumbleType(2), 0.8)
        self.WristSub.WristStop()

class WristL4(commands2.Command):
    def __init__(self, WristSubsytem: WristSubsystemClass) -> None:
        self.WristSub = WristSubsytem

    def initialize(self):
        logger.info(" wrist to L4")

    def execute(self):
        if self.WristSub.coralMode:
            self.WristSub.wristMotionMagic(SW.Wrist_L4_Setpoint)
        else:
            self.WristSub.wristMotionMagic(SW.Wrist_Barge_Setpoint)

    def isFinished(self):
        return False
   
    def end(self, interrupted):
        self.WristSub.WristStop()
        
class WristStation(commands2.Command):
    def __init__(self, WristSubsytem: WristSubsystemClass) -> None:
        self.WristSub = WristSubsytem

    def initialize(self):
        logger.info(" wrist to human player")

    def execute(self):
        if self.WristSub.coralMode:
            self.WristSub.wristMotionMagic(SW.Wrist_Human_Player_Setpoint)
        else:
            self.WristSub.wristMotionMagic(SW.Wrist_Processor_Setpoint)

    def isFinished(self):
        return False
   
    def end(self, interrupted):
        self.WristSub.WristStop()
        
class WristGroundIntake(commands2.Command):
    def __init__(self, WristSubsytem: WristSubsystemClass) -> None:
        self.WristSub = WristSubsytem

    def initialize(self):
        logger.info(" wrist to robot")

    def execute(self):
        self.WristSub.wristMotionMagic(SW.Wrist_ground_Setpoint)

    def isFinished(self):
        return False
   
    def end(self, interrupted):
        self.WristSub.WristStop()
        
class WristHome(commands2.Command):
    def __init__(self, WristSubsytem: WristSubsystemClass) -> None:
        self.WristSub = WristSubsytem

    def initialize(self):
        logger.info(" wrist to robot")

    def execute(self):
        self.WristSub.wristMotionMagic(0)

    def isFinished(self):
        return False
   
    def end(self, interrupted):
        self.WristSub.WristStop()
        
class CoralMode(commands2.Command):
    def __init__(self, WristSubsytem: WristSubsystemClass) -> None:
        self.WristSub = WristSubsytem

    def initialize(self):
        logger.info("changing modes")

    def execute(self):
        self.WristSub.cMode()

    def isFinished(self):
        return True
        
class AlgaeMode(commands2.Command):
    def __init__(self, WristSubsytem: WristSubsystemClass) -> None:
        self.WristSub = WristSubsytem

    def initialize(self):
        logger.info("changing modes")

    def execute(self):
        self.WristSub.aMode()

    def isFinished(self):
        return True
        
        
        
        
# ==================================== Auto ================================================

#         ---------------------------- Coral ---------------------------
class CoralL2(commands2.Command):
    def __init__(self, WristSubsytem: WristSubsystemClass) -> None:
        self.WristSub = WristSubsytem

    def initialize(self):
        logger.info(" wrist to robot")

    def execute(self):
        self.WristSub.wristMotionMagic(SW.Wrist_L2_Setpoint)

    def isFinished(self):
        if self.WristSub.wristPID.atSetpoint():
            return True
        return False
   
    def end(self, interrupted):
        self.WristSub.WristStop()
        
class CoralL3(commands2.Command):
    def __init__(self, WristSubsytem: WristSubsystemClass) -> None:
        self.WristSub = WristSubsytem

    def initialize(self):
        logger.info(" wrist to proccesor")

    def execute(self):
        self.WristSub.wristMotionMagic(SW.Wrist_L3_Setpoint)

    def isFinished(self):
        if self.WristSub.wristPID.atSetpoint():
            return True
        return False
   
    def end(self, interrupted):
        self.WristSub.WristStop()

class CoralL4(commands2.Command):
    def __init__(self, WristSubsytem: WristSubsystemClass) -> None:
        self.WristSub = WristSubsytem

    def initialize(self):
        logger.info(" wrist to floor")

    def execute(self):
        self.WristSub.wristMotionMagic(SW.Wrist_L4_Setpoint)

    def isFinished(self):
        if self.WristSub.wristPID.atSetpoint():
            return True
        return False
   
    def end(self, interrupted):
        self.WristSub.WristStop()
        
class AutoWristHumanPlayer(commands2.Command):
    def __init__(self, WristSubsytem: WristSubsystemClass) -> None:
        self.WristSub = WristSubsytem

    def initialize(self):
        logger.info(" wrist to floor")

    def execute(self):
        self.WristSub.wristMotionMagic(SW.Wrist_Human_Player_Setpoint)

    def isFinished(self):
        return False
   
    def end(self, interrupted):
        self.WristSub.WristStop()
        
        
#      ------------------------ Algae -----------------------------
        
class AlgaeL2(commands2.Command):
    def __init__(self, WristSubsytem: WristSubsystemClass) -> None:
        self.WristSub = WristSubsytem

    def initialize(self):
        logger.info(" wrist to robot")

    def execute(self):
        self.WristSub.wristMotionMagic(SW.Algae_L2_Setpoint)

    def isFinished(self):
        if self.WristSub.wristPID.atSetpoint():
            return True
        return False
   
    def end(self, interrupted):
        self.WristSub.WristStop()
        
class AlgaeL3(commands2.Command):
    def __init__(self, WristSubsytem: WristSubsystemClass) -> None:
        self.WristSub = WristSubsytem

    def initialize(self):
        logger.info(" wrist to proccesor")

    def execute(self):
        self.WristSub.wristMotionMagic(SW.Algae_L3_Setpoint)

    def isFinished(self):
        if self.WristSub.wristPID.atSetpoint():
            return True
        return False
   
    def end(self, interrupted):
        self.WristSub.WristStop()
        
class AutoWristBarge(commands2.Command):
    def __init__(self, WristSubsytem: WristSubsystemClass) -> None:
        self.WristSub = WristSubsytem

    def initialize(self):
        logger.info(" wrist to floor")

    def execute(self):
        self.WristSub.wristMotionMagic(SW.Wrist_Barge_Setpoint)

    def isFinished(self):
        if self.WristSub.wristPID.atSetpoint():
            return True
        return False
   
    def end(self, interrupted):
        self.WristSub.WristStop()
        
class AutoWristProcessor(commands2.Command):
    def __init__(self, WristSubsytem: WristSubsystemClass) -> None:
        self.WristSub = WristSubsytem

    def initialize(self):
        logger.info(" wrist to floor")

    def execute(self):
        self.WristSub.wristMotionMagic(SW.Wrist_Processor_Setpoint)

    def isFinished(self):
        return False
   
    def end(self, interrupted):
        self.WristSub.WristStop()
        
        
    #      --------------------- Home ---------------------------- 
class AutoWristHome(commands2.Command):
    def __init__(self, WristSubsytem: WristSubsystemClass) -> None:
        self.WristSub = WristSubsytem

    def initialize(self):
        logger.info(" wrist to robot")

    def execute(self):
        self.WristSub.wristMotionMagic(0)

    def isFinished(self):
        if self.WristSub.wristPID.atSetpoint():
            return True
        return False
   
    def end(self, interrupted):
        self.WristSub.WristStop()