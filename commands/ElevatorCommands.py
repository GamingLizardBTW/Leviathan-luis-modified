import wpilib
import commands2
from subsystems.ElevatorSubystem import ElevatorSubsystemClass
import logging
logger = logging.getLogger("WristSubsystem Logger")
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
            self.ElevatorSub.wristwithjoystick(self.inputvalue)
        else:
            self.ElevatorSub.elevatorMotorStop()
        #logging.info("Running motor")

    def isFinished(self):
        return False
    
    def end(self, interrupted):
        self.ElevatorSub.elevatorMotorStop()
        
class ElevatorL2(commands2.Command):

    def __init__(self, ElevSub: ElevatorSubsystemClass) -> None:
        self.addRequirements(ElevSub)
        self.ElevatorSub = ElevSub
        logger.info("Elevator constructor")

    
    def initialize(self):
        logger.info("Elevaotr to L2 initialize")

    def execute(self):
        self.ElevatorSub.normalPID(SW.L2_Setpoint)

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
        self.ElevatorSub.normalPID(SW.L3_Setpoint)

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
        self.ElevatorSub.normalPID()

    def isFinished(self):
        # return False
        if self.ElevatorSub.bottomOveride is False:
            return True
    
    def end(self, interrupted):
        self.ElevatorSub.elevatorMotorStop(SW.L4_Setpoint)
        
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
        return self.ElevatorSub.topOveride
    
    def end(self, interrupted):
        self.ElevatorSub.elevatorMotorStop()