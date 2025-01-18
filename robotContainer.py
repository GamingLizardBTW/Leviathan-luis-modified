import subsystems.AlgaeSubsystem
from commands.AlgaeCommands import AlgaeIntakeCommand, AlgaeOutakeCommand, AlgaeStop, AlgaeWithTriggers

from wpilib import XboxController
import subsystems.WristSubsystem
import commands.WristCommands
from wpilib import XboxController
from commands.WristCommands import WristMotorStop, WristWithJoysticks

class RobotContainer:
    """
    This example robot container should serve as a demonstration for how to
    implement swervepy on your robot.  You should not need to edit much of the
    code in this module to get a test working.  Instead, edit the values and
    class choices in constants.py.
    """

    def __init__(self):
        self.algaesub = subsystems.AlgaeSubsystem.AlgaeSubsystemClass()
        self.wristsub = subsystems.WristSubsystem.WristSubsystemClass()
        self.DriverController = XboxController(0)
        self.OperatorController = XboxController(1)
        self.configureButtonBindings()
    
    def get_autonomous_command(self):
        pass

    def configureButtonBindings(self):
        self.algaesub.setDefaultCommand(AlgaeWithTriggers(self.algaesub))
        self.wristsub.setDefaultCommand(WristWithJoysticks(self.wristsub))
