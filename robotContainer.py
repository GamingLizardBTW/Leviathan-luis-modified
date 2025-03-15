from wpilib import XboxController
from wpilib import SmartDashboard
import subsystems.DrivetrainSubsystem
import commands2

# Constants
from constants import OP

# Subsystems
import subsystems.IntakeSubsystem
import subsystems.WristSubsystem
import subsystems.ElevatorSubystem
import subsystems.VisionSubsystem
import subsystems.HangSubsystem

# Commands
from commands.IntakeCommands import IntakeCommand, OutakeCommand, IntakeStop
from commands.WristCommands import WristForward, WristBackwards, WristStop, WristL2, WristL3, WristL4
from commands.ElevatorCommands import ElevatorWithJoysticks, ElevatorL2, ElevatorL3, ElevatorL4, ElevatorHome
from commands.HangCommands import hangBackwards, hangForward, hangStop
from commands.ReefScoringCommand import ScoringL2

from commands.DrivetrainCommands import driveWithJoystickCommand
from pathplannerlib.auto import AutoBuilder, PathPlannerAuto
from pathplannerlib.path import PathPlannerPath

import logging
logger = logging.getLogger("RobotContainer")

class RobotContainer:
    """
    This example robot container should serve as a demonstration for how to
    implement swervepy on your robot.  You should not need to edit much of the
    code in this module to get a test working.  Instead, edit the values and
    class choices in constants.py.
    """

    def __init__(self):
        logger.info("Creating robot container")
        
        # Subsytems
        self.visionSub = subsystems.VisionSubsystem.visionSubsystem()
        self.Intakesub = subsystems.IntakeSubsystem.IntakeSubsystemClass()
        self.wristsub = subsystems.WristSubsystem.WristSubsystemClass()
        self.elevatorsub = subsystems.ElevatorSubystem.ElevatorSubsystemClass()
        self.drivetrainSub = subsystems.DrivetrainSubsystem.drivetrainSubsystemClass()
        self.hangSub = subsystems.HangSubsystem.HangSubsystem()
        
        # Controllers
        self.DriverController = commands2.button.CommandXboxController(OP.driver_controller)
        self.OperatorController = commands2.button.CommandXboxController(OP.operator_controller)
        
        # Configure Bindings
        self.configureButtonBindings()
        self.autoChooser = AutoBuilder.buildAutoChooser()
        SmartDashboard.putData("Auto Chooser", self.autoChooser)
        logger.info("Robot container created")
    
    def get_autonomous_command(self):
        # return self.autoChooser.getSelected()

    # Create a path following command using AutoBuilder. This will also trigger event markers.
        return PathPlannerAuto('New Auto')

    def configureButtonBindings(self):
        pass
        
        # Default Commands
        self.elevatorsub.setDefaultCommand(ElevatorWithJoysticks(self.elevatorsub))
        self.drivetrainSub.setDefaultCommand(driveWithJoystickCommand(self.drivetrainSub, self.visionSub)) # Additional Buttons used: A
        
        # Intake Intake Commands
        self.OperatorController.leftBumper().onTrue(IntakeCommand(self.Intakesub))
        self.OperatorController.leftBumper().onFalse(IntakeStop(self.Intakesub))
        self.OperatorController.rightBumper().onTrue(OutakeCommand(self.Intakesub))
        self.OperatorController.rightBumper().onFalse(IntakeStop(self.Intakesub))
        
        # Intake Wrist PID Commands
        # self.OperatorController.x().whileTrue(WristL2(self.Intakesub)) # Considering making it to "on true" to only have to press once
        # self.OperatorController.b().whileTrue(WristL3(self.Intakesub))
        # self.OperatorController.a().whileTrue(WristL4(self.Intakesub))
        
        # Intake Wrist Manual Commands
        self.OperatorController.a().whileTrue(WristForward(self.wristsub))
        self.OperatorController.a().whileFalse(WristStop(self.wristsub))
        self.OperatorController.y().whileTrue(WristBackwards(self.wristsub))
        self.OperatorController.y().whileFalse(WristStop(self.wristsub))
        
        # Elevator PID Commands
        # self.OperatorController.y().whileTrue(ElevatorL4(self.elevatorsub))
        # self.OperatorController.a().whileTrue(ElevatorL3(self.elevatorsub))
        self.OperatorController.b().whileTrue(ElevatorL2(self.elevatorsub))
        # self.OperatorController.a().whileTrue(ElevatorHome(self.elevatorsub))
        
        self.DriverController.a().whileTrue(hangBackwards(self.hangSub))
        self.DriverController.a().whileFalse(hangStop(self.hangSub))
        self.DriverController.y().whileTrue(hangForward(self.hangSub))
        self.DriverController.y().whileFalse(hangStop(self.hangSub))
        
        self.OperatorController.x().whileTrue(ScoringL2(self.elevatorsub, self.wristsub))
        # self.OperatorController.b().whileTrue(ScoringL3(self.Intakesub))
        # self.OperatorController.a().whileTrue(ScoringL4(self.Intakesub))