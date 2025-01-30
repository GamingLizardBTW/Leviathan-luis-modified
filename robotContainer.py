import subsystems.AlgaeSubsystem
from commands.AlgaeCommands import AlgaeIntakeCommand, AlgaeOutakeCommand, AlgaeStop, AlgaeWithTriggers

from wpilib import XboxController
import subsystems.DrivetrainSubsystem
import subsystems.WristSubsystem
import commands.WristCommands
from wpilib import XboxController
from commands.WristCommands import WristMotorStop, WristWithJoysticks
import commands2
from constants import OP

from commands.CoralCommands import CoralIntake, CoralOuttake, CoralStop
import subsystems.CoralSubsystem

from commands.DrivetrainCommands import driveWithJoystickCommand
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
        self.coralsub = subsystems.CoralSubsystem.CoralSubsystemClass()
        self.drivetrainSub = subsystems.DrivetrainSubsystem.drivetrainSubsystemClass()
        self.DriverController = commands2.button.CommandXboxController(OP.driver_controller)
        self.OperatorController = commands2.button.CommandXboxController(OP.operator_controller)
        self.configureButtonBindings()
    
    def get_autonomous_command(self):
        pass

    def configureButtonBindings(self):
        self.algaesub.setDefaultCommand(AlgaeWithTriggers(self.algaesub))
        self.wristsub.setDefaultCommand(WristWithJoysticks(self.wristsub))
        self.drivetrainSub.setDefaultCommand(driveWithJoystickCommand(self.drivetrainSub))
        self.OperatorController.leftBumper().whileTrue(CoralOuttake(self.coralsub))
        self.OperatorController.leftBumper().whileFalse(CoralStop(self.coralsub))
        self.OperatorController.rightBumper().whileTrue(CoralIntake(self.coralsub))
        self.OperatorController.rightBumper().whileFalse(CoralStop(self.coralsub))


