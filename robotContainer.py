import subsystems.AlgaeSubsystem
from commands.AlgaeCommands import AlgaeIntakeCommand, AlgaeOutakeCommand, AlgaeStop, AlgaeWithTriggers

from wpilib import XboxController

class RobotContainer:
    """
    This example robot container should serve as a demonstration for how to
    implement swervepy on your robot.  You should not need to edit much of the
    code in this module to get a test working.  Instead, edit the values and
    class choices in constants.py.
    """

    def __init__(self):
        self.algaesub = subsystems.AlgaeSubsystem.AlgaeSubsystemClass()
        self.DriverController = XboxController(0)
        self.OperatorController = XboxController(1)

    def get_autonomous_command(self):
        pass

    def configureButtonBindings(self):
        self.algaesub.setDefaultCommand(AlgaeWithTriggers(self.algaesub, self.OperatorController.getLeftTriggerAxis(), self.OperatorController.getRightTriggerAxis()))
