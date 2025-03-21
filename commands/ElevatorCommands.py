import wpilib
import commands2
from subsystems.ElevatorSubsystem import ElevatorSubsystemClass
import logging
logger = logging.getLogger("elevator Subsystem Logger")
from wpilib import XboxController
from constants import OP, SW

class ElevatorWithJoysticks(commands2.Command):

    def __init__(self, ElevSub: ElevatorSubsystemClass) -> None:
        self.addRequirements(ElevSub)
        self.ElevatorSub = ElevSub
        logger.info("Elevator constructor")

    
    def initialize(self):
        logger.info("Elevaotr with joystick initialize")

    def execute(self):
        self.inputvalue = XboxController(OP.operator_controller).getLeftY()
        if self.inputvalue > 0.1 or self.inputvalue < -0.1:
            # self.ElevatorSub.elevatorWithjoystick(self.inputvalue)
            self.ElevatorSub.motionMagic(self.inputvalue)
        # else:
        #     self.ElevatorSub.elevatorMotorStop()
        # #logging.info("Running motor")

    def isFinished(self):
        return False
    
    def end(self, interrupted):
        self.ElevatorSub.elevatorMotorStop()
        
        
    # Elevator with PID
class ElevatorL2(commands2.Command):

    def __init__(self, ElevSub: ElevatorSubsystemClass) -> None:
        self.addRequirements(ElevSub)
        self.ElevatorSub = ElevSub
        logger.info("Elevator constructor")

    
    def initialize(self):
        logger.info("Elevaotr to L2 initialize")

    def execute(self):
        # self.ElevatorSub.normalPID(SW.L2_Setpoint)
        self.ElevatorSub.normalPID2(SW.L2_Setpoint)

    def isFinished(self):
        return False
    
    def end(self, interrupted):
        self.ElevatorSub.elevatorMotorStop()
        
class ElevatorL3(commands2.Command):

    def __init__(self, ElevSub: ElevatorSubsystemClass) -> None:
        self.addRequirements(ElevSub)
        self.ElevatorSub = ElevSub
        logger.info("Elevator constructor")

    
    def initialize(self):
        logger.info("Elevaotr to L3 initialize")

    def execute(self):
        # self.ElevatorSub.normalPID(SW.L3_Setpoint)
        self.ElevatorSub.normalPID2(SW.L3_Setpoint)

    def isFinished(self):
        return False
    
    def end(self, interrupted):
        self.ElevatorSub.elevatorMotorStop()
        
class ElevatorL4(commands2.Command):

    def __init__(self, ElevSub: ElevatorSubsystemClass) -> None:
        self.addRequirements(ElevSub)
        self.ElevatorSub = ElevSub
        logger.info("Elevator constructor")

    
    def initialize(self):
        logger.info("Elevaotr to L4 initialize")

    def execute(self):
        self.ElevatorSub.normalPID(SW.L4_Setpoint)

    def isFinished(self):
        return False
        # if self.ElevatorSub.bottomOveride is False:
        #     return True
    
    def end(self, interrupted):
        self.ElevatorSub.elevatorMotorStop()
        
class ElevatorBarge(commands2.Command):

    def __init__(self, ElevSub: ElevatorSubsystemClass) -> None:
        self.addRequirements(ElevSub)
        self.ElevatorSub = ElevSub
        logger.info("Elevator constructor")

    
    def initialize(self):
        logger.info("Elevaotr to L4 initialize")

    def execute(self):
        self.ElevatorSub.normalPID(SW.Barge_Setpoint)

    def isFinished(self):
        return False
    
    def end(self, interrupted):
        self.ElevatorSub.elevatorMotorStop()
        
class ElevatorHome(commands2.Command):

    def __init__(self, ElevSub: ElevatorSubsystemClass) -> None:
        self.addRequirements(ElevSub)
        self.ElevatorSub = ElevSub
        logger.info("Elevator constructor")

    
    def initialize(self):
        logger.info("Elevaotr with PID initialize")

    def execute(self):
        self.ElevatorSub.homeElevator()

    def isFinished(self):
        return self.ElevatorSub.bottomOveride
    
    def end(self, interrupted):
        self.ElevatorSub.elevatorMotorStop()
        
        
    # Elevator with PID
class AutoElevatorL2(commands2.Command):

    def __init__(self, ElevSub: ElevatorSubsystemClass) -> None:
        self.addRequirements(ElevSub)
        self.ElevatorSub = ElevSub
        logger.info("Elevator constructor")

    
    def initialize(self):
        logger.info("Elevaotr to L2 initialize")

    def execute(self):
        self.ElevatorSub.normalPID(SW.L2_Setpoint)

    def isFinished(self):
        if self.ElevatorSub.encoder == SW.L2_Setpoint:
            return True
        else:
            return False
    
    def end(self, interrupted):
        self.ElevatorSub.elevatorMotorStop()
        
class AutoElevatorL3(commands2.Command):

    def __init__(self, ElevSub: ElevatorSubsystemClass) -> None:
        self.addRequirements(ElevSub)
        self.ElevatorSub = ElevSub
        logger.info("Elevator constructor")

    
    def initialize(self):
        logger.info("Elevaotr to L3 initialize")

    def execute(self):
        self.ElevatorSub.normalPID(SW.L3_Setpoint)

    def isFinished(self):
        if self.ElevatorSub.encoder == SW.L3_Setpoint:
            return True
        else:
            return False
    
    def end(self, interrupted):
        self.ElevatorSub.elevatorMotorStop()
        
class AutoElevatorL4(commands2.Command):

    def __init__(self, ElevSub: ElevatorSubsystemClass) -> None:
        self.addRequirements(ElevSub)
        self.ElevatorSub = ElevSub
        logger.info("Elevator constructor")

    
    def initialize(self):
        logger.info("Elevaotr to L4 initialize")

    def execute(self):
        self.ElevatorSub.normalPID(SW.L4_Setpoint)

    def isFinished(self):
        if self.ElevatorSub.encoder == SW.L4_Setpoint:
            return True
        else:
            return False
    
    def end(self, interrupted):
        self.ElevatorSub.elevatorMotorStop()
        
class AutoElevatorBarge(commands2.Command):

    def __init__(self, ElevSub: ElevatorSubsystemClass) -> None:
        self.addRequirements(ElevSub)
        self.ElevatorSub = ElevSub
        logger.info("Elevator constructor")

    
    def initialize(self):
        logger.info("Elevaotr to L4 initialize")

    def execute(self):
        self.ElevatorSub.normalPID(SW.Barge_Setpoint)

    def isFinished(self):
        return False
    
    def end(self, interrupted):
        self.ElevatorSub.elevatorMotorStop()
        
class AutoElevatorHome(commands2.Command):

    def __init__(self, ElevSub: ElevatorSubsystemClass) -> None:
        self.addRequirements(ElevSub)
        self.ElevatorSub = ElevSub
        logger.info("Elevator constructor")

    
    def initialize(self):
        logger.info("Elevaotr with PID initialize")

    def execute(self):
        self.ElevatorSub.homeElevator()

    def isFinished(self):
        return self.ElevatorSub.bottomOveride
    
    def end(self, interrupted):
        self.ElevatorSub.elevatorMotorStop()