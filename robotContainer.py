import subsystems.AlgaeSubsystem
from commands.AlgaeCommands import AlgaeIntakeCommand, AlgaeOutakeCommand, AlgaeStop, AlgaeWithTriggers

from wpilib import XboxController
from wpilib import SmartDashboard
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
        self.algaesub = subsystems.AlgaeSubsystem.AlgaeSubsystemClass()
        self.wristsub = subsystems.WristSubsystem.WristSubsystemClass()
        self.coralsub = subsystems.CoralSubsystem.CoralSubsystemClass()
        self.drivetrainSub = subsystems.DrivetrainSubsystem.drivetrainSubsystemClass()
        self.DriverController = commands2.button.CommandXboxController(OP.driver_controller)
        self.OperatorController = commands2.button.CommandXboxController(OP.operator_controller)
        self.configureButtonBindings()
        self.autoChooser = AutoBuilder.buildAutoChooser()
        SmartDashboard.putData("Auto Chooser", self.autoChooser)
        logger.info("Robot container created")
    
    def get_autonomous_command(self):
        # return self.autoChooser.getSelected()

    # Create a path following command using AutoBuilder. This will also trigger event markers.
        return PathPlannerAuto('New Auto')

    def configureButtonBindings(self):
        self.algaesub.setDefaultCommand(AlgaeWithTriggers(self.algaesub))
        self.wristsub.setDefaultCommand(WristWithJoysticks(self.wristsub))
        self.drivetrainSub.setDefaultCommand(driveWithJoystickCommand(self.drivetrainSub))
        self.OperatorController.leftBumper().whileTrue(CoralOuttake(self.coralsub))
        self.OperatorController.leftBumper().whileFalse(CoralStop(self.coralsub))
        self.OperatorController.rightBumper().whileTrue(CoralIntake(self.coralsub))
        self.OperatorController.rightBumper().whileFalse(CoralStop(self.coralsub))


