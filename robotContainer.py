from wpilib import XboxController
from wpilib import SmartDashboard
import subsystems.DrivetrainSubsystem
import commands2

# Constants
from constants import OP

# Subsystems
import subsystems.AlgaeSubsystem
import subsystems.WristSubsystem
import subsystems.CoralSubsystem

# Commands
from commands.AlgaeCommands import AlgaeIntakeCommand, AlgaeOutakeCommand, AlgaeStop, AlgaeWristForward, AlgaeWristBackwards, AlgaeWristStop, AlgaeWristToFloor, AlgaeWristToRobot
from commands.WristCommands import WristMotorStop, WristWithJoysticks
from commands.CoralCommands import CoralIntake, CoralOuttake, CoralStop

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
        self.algaesub = subsystems.AlgaeSubsystem.AlgaeSubsystemClass()
        # self.wristsub = subsystems.WristSubsystem.WristSubsystemClass()
        # self.coralsub = subsystems.CoralSubsystem.CoralSubsystemClass()
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
        
        # Dont Need
        # self.algaesub.setDefaultCommand(AlgaeWithTriggers(self.algaesub))
        # self.wristsub.setDefaultCommand(WristWithJoysticks(self.wristsub))
        # self.drivetrainSub.setDefaultCommand(driveWithJoystickCommand(self.drivetrainSub))
        
        # Will re-add later on
        # self.OperatorController.leftBumper().whileTrue(CoralOuttake(self.coralsub))
        # self.OperatorController.leftBumper().whileFalse(CoralStop(self.coralsub))
        # self.OperatorController.rightBumper().whileTrue(CoralIntake(self.coralsub))
        # self.OperatorController.rightBumper().whileFalse(CoralStop(self.coralsub))
        
        self.DriverController.leftBumper().onTrue(AlgaeIntakeCommand(self.algaesub))
        self.DriverController.leftBumper().onFalse(AlgaeStop(self.algaesub))
        
        self.DriverController.rightBumper().onTrue(AlgaeOutakeCommand(self.algaesub))
        self.DriverController.rightBumper().onFalse(AlgaeStop(self.algaesub))
        
        # self.DriverController.b().onTrue(AlgaeWristToRobot(self.algaesub)) # Considering making it to "on true" to only have to press once
        
        self.DriverController.a().whileTrue(AlgaeWristForward(self.algaesub))
        self.DriverController.a().whileFalse(AlgaeWristStop(self.algaesub))
        
        # self.DriverController.b().whileTrue(AlgaeWristToFloor(self.algaesub))
        
        self.DriverController.y().whileTrue(AlgaeWristBackwards(self.algaesub))
        self.DriverController.y().whileFalse(AlgaeWristStop(self.algaesub))