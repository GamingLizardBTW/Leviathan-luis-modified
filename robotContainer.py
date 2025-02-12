from wpilib import XboxController
import subsystems.DrivetrainSubsystem
import commands2

# Constants
from constants import OP

# Subsystems
import subsystems.AlgaeSubsystem
import subsystems.WristSubsystem
import subsystems.CoralSubsystem

# Commands
from commands.AlgaeCommands import AlgaeIntakeCommand, AlgaeOutakeCommand, AlgaeStop, AlgaeWithTriggers, AlgaeWristForward, AlgaeWristBackwards, AlgaeWristStop, AlgaeWristToFloor, AlgaeWristToRobot, resetWristEncoder
from commands.WristCommands import WristMotorStop, WristWithJoysticks
from commands.CoralCommands import CoralIntake, CoralOuttake, CoralStop

from commands.DrivetrainCommands import driveWithJoystickCommand
class RobotContainer:
    """
    This example robot container should serve as a demonstration for how to
    implement swervepy on your robot.  You should not need to edit much of the
    code in this module to get a test working.  Instead, edit the values and
    class choices in constants.py.
    """

    def __init__(self):
        
        # Subsytems
        self.algaesub = subsystems.AlgaeSubsystem.AlgaeSubsystemClass()
        # self.wristsub = subsystems.WristSubsystem.WristSubsystemClass()
        # self.coralsub = subsystems.CoralSubsystem.CoralSubsystemClass()
        # self.drivetrainSub = subsystems.DrivetrainSubsystem.drivetrainSubsystemClass()
        
        # Controllers
        self.DriverController = commands2.button.CommandXboxController(OP.driver_controller)
        self.OperatorController = commands2.button.CommandXboxController(OP.operator_controller)
        
        # Configure Bindings
        self.configureButtonBindings()
    
    def get_autonomous_command(self):
        pass

    def configureButtonBindings(self):
        
        # Dont Need
        # self.algaesub.setDefaultCommand(AlgaeWithTriggers(self.algaesub))
        # self.wristsub.setDefaultCommand(WristWithJoysticks(self.wristsub))
        # self.drivetrainSub.setDefaultCommand(driveWithJoystickCommand(self.drivetrainSub))
        
        # Will re-add later on
        # self.OperatorController.leftBumper().whileTrue(CoralOuttake(self.coralsub))
        # self.OperatorController.leftBumper().whileFalse(CoralStop(self.coralsub))
        # self.OperatorController.rightBumper().whileTrue(CoralIntake(self.coralsub))
        # self.OperatorController.rightBumper().whileFalse(CoralStop(self.coralsub))
        
        self.OperatorController.x().onTrue(AlgaeIntakeCommand(self.algaesub))
        self.OperatorController.x().onFalse(AlgaeStop(self.algaesub))
        
        
        self.OperatorController.y().onTrue(AlgaeOutakeCommand(self.algaesub))
        self.OperatorController.y().onFalse(AlgaeStop(self.algaesub))
        
        # self.OperatorController.a().whileTrue(AlgaeWristToRobot(self.algaesub))
        self.OperatorController.a().whileTrue(AlgaeWristForward(self.algaesub))
        self.OperatorController.a().whileFalse(AlgaeWristStop(self.algaesub))
        
        # self.OperatorController.b().whileTrue(AlgaeWristToFloor(self.algaesub))
        self.OperatorController.b().whileTrue(AlgaeWristBackwards(self.algaesub))
        self.OperatorController.b().whileFalse(AlgaeWristStop(self.algaesub))
        
        # self.OperatorController.button(7).whileTrue(resetWristEncoder(self.algaesub))


