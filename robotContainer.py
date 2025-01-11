import subsystems.WristSubsystem
import commands.WristCommands
from wpilib import XboxController
from commands.WristCommands import WristMotorStop, WristWithJoysticks

class RobotContainer:

    def __init__(self):
        self.wristsub = subsystems.WristSubsystem.WristSubsystemClass()
        self.DriverController = XboxController(0)
        self.OperatorController = XboxController(1)
    
    def get_autonomous_command(self):
        pass


    def configureButtonBindings(self):
        self.wristsub.setDefaultCommand(WristWithJoysticks(self.wristsub, self.OperatorController.getRightY()))
