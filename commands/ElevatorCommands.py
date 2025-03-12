import wpilib
import commands2
from subsystems.ElevatorSubystem import ElevatorSubsystemClass
import logging
logger = logging.getLogger("WristSubsystem Logger")
from wpilib import XboxController
from constants import OP

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
        
class ElevatorPID1(commands2.Command):

    def __init__(self, ElevSub: ElevatorSubsystemClass) -> None:
        self.addRequirements(ElevSub)
        self.ElevatorSub = ElevSub
        logger.info("Elevator constructor")

    
    def initialize(self):
        logger.info("Elevaotr with Trapezoid PID initialize")

    def execute(self):
        self.ElevatorSub.trapezoidPID()

    def isFinished(self):
        return False
    
    def end(self, interrupted):
        self.ElevatorSub.elevatorMotorStop()
        
class ElevatorPID2(commands2.Command):

    def __init__(self, ElevSub: ElevatorSubsystemClass) -> None:
        self.addRequirements(ElevSub)
        self.ElevatorSub = ElevSub
        logger.info("Elevator constructor")

    
    def initialize(self):
        logger.info("Elevaotr Trapezoid with PID initialize")

    def execute(self):
        self.ElevatorSub.trapezoidPID()

    def isFinished(self):
        return False
    
    def end(self, interrupted):
        self.ElevatorSub.elevatorMotorStop()
        
class ElevatorPID3(commands2.Command):

    def __init__(self, ElevSub: ElevatorSubsystemClass) -> None:
        self.addRequirements(ElevSub)
        self.ElevatorSub = ElevSub
        logger.info("Elevator constructor")

    
    def initialize(self):
        logger.info("Elevaotr with PID initialize")

    def execute(self):
        self.ElevatorSub.normalPID()

    def isFinished(self):
        if self.ElevatorSub.bottomOveride:
            return True
    
    def end(self, interrupted):
        self.ElevatorSub.elevatorMotorStop()
        
class ElevatorPID4(commands2.Command):

    def __init__(self, ElevSub: ElevatorSubsystemClass) -> None:
        self.addRequirements(ElevSub)
        self.ElevatorSub = ElevSub
        logger.info("Elevator constructor")

    
    def initialize(self):
        logger.info("Elevaotr with PID initialize")

    def execute(self):
        self.ElevatorSub.normalPID()

    def isFinished(self):
        return self.ElevatorSub.topOveride
    
    def end(self, interrupted):
        self.ElevatorSub.elevatorMotorStop()