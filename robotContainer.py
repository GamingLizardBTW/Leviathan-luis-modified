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

# Commands
from commands.IntakeCommands import IntakeCommand, OutakeCommand, IntakeStop
from commands.WristCommands import WristForward, WristBackwards, WristStop, WristL2, WristL3, WristL4
from commands.ElevatorCommands import ElevatorWithJoysticks, ElevatorPID1, ElevatorPID2, ElevatorPID3, ElevatorPID4

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
        # self.Intakesub = subsystems.IntakeSubsystem.IntakeSubsystemClass()
        # self.wristsub = subsystems.WristSubsystem.WristSubsystemClass()
        self.elevatorsub = subsystems.ElevatorSubystem.ElevatorSubsystemClass()
        self.drivetrainSub = subsystems.DrivetrainSubsystem.drivetrainSubsystemClass()
        
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
        # self.elevatorsub.setDefaultCommand(ElevatorWithJoysticks(self.elevatorsub))
        # self.drivetrainSub.setDefaultCommand(driveWithJoystickCommand(self.drivetrainSub)) # Additional Buttons used: A
        
        # Intake Intake Commands
        # self.DriverController.leftBumper().onTrue(IntakeCommand(self.Intakesub))
        # self.DriverController.leftBumper().onFalse(IntakeStop(self.Intakesub))
        # self.DriverController.rightBumper().onTrue(OutakeCommand(self.Intakesub))
        # self.DriverController.rightBumper().onFalse(IntakeStop(self.Intakesub))
        
        # Intake Wrist PID Commands
        # self.DriverController.x().whileTrue(WristL2(self.Intakesub)) # Considering making it to "on true" to only have to press once
        # self.DriverController.b().whileTrue(WristL3(self.Intakesub))
        # self.DriverController.a().whileTrue(WristL4(self.Intakesub))
        
        # Intake Wrist Manual Commands
        # self.DriverController.a().whileTrue(WristForward(self.Intakesub))
        # self.DriverController.a().whileFalse(WristStop(self.Intakesub))
        # self.DriverController.y().whileTrue(WristBackwards(self.Intakesub))
        # self.DriverController.y().whileFalse(WristStop(self.Intakesub))
        
        # Elevator PID Commands
        # self.OperatorController.y().whileTrue(ElevatorPID1(self.elevatorsub))
        # self.OperatorController.a().whileTrue(ElevatorPID2(self.elevatorsub))
        self.OperatorController.y().whileTrue(ElevatorPID3(self.elevatorsub))
        self.OperatorController.a().whileTrue(ElevatorPID4(self.elevatorsub))