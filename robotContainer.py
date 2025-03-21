from wpilib import XboxController
from wpilib import SmartDashboard
import subsystems.DrivetrainSubsystem
import commands2

# Constants
from constants import OP

# Subsystems
import subsystems.IntakeSubsystem
import subsystems.WristSubsystem
import subsystems.ElevatorSubsystem
import subsystems.VisionSubsystem
import subsystems.HangSubsystem
import subsystems.MotionMagicExample

# Commands
from commands.IntakeCommands import IntakeCommand, OutakeCommand, IntakeStop, AutoIntakeCommand, AutoOuttakeCommand
# from commands.IntakeCommands import IntakeCommand, OutakeCommand, IntakeStop
from commands.WristCommands import wristWithJoystick, WristL2, WristL3, WristL4, WristBarge, WristHome, AutoWristL2, AutoWristL3, AutoWristL4, AutoWristBarge, AutoWristHome
from commands.ElevatorCommands import ElevatorWithJoysticks, ElevatorL2, ElevatorL3, ElevatorL4, ElevatorBarge, ElevatorHome, AutoElevatorL2, AutoElevatorL3, AutoElevatorL4, AutoElevatorBarge, AutoElevatorHome
from commands.HangCommands import hangBackwards, hangForward, hangStop
from commands.ReefScoringCommand import ScoringL2, ScoringL3, ScoringL4, BargeScoring
from commands.MotionMagicCommand import MotionWithJoystick

from commands.DrivetrainCommands import driveWithJoystickCommand
from pathplannerlib.auto import AutoBuilder, PathPlannerAuto, NamedCommands
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
        # self.visionSub = subsystems.VisionSubsystem.visionSubsystem()
        # self.Intakesub = subsystems.IntakeSubsystem.IntakeSubsystemClass()
        # self.wristsub = subsystems.WristSubsystem.WristSubsystemClass()
        self.elevatorsub = subsystems.ElevatorSubsystem.ElevatorSubsystemClass()
        self.drivetrainSub = subsystems.DrivetrainSubsystem.drivetrainSubsystemClass()
        # self.hangSub = subsystems.HangSubsystem.HangSubsystem()
        # self.testSub = subsystems.MotionMagicExample.MotionMagicClass()
        
        # Controllers
        self.DriverController = commands2.button.CommandXboxController(OP.driver_controller)
        self.OperatorController = commands2.button.CommandXboxController(OP.operator_controller)
        
        #Command groups
        # self.teleopL2 = commands2.ParallelCommandGroup(WristL2(self.wristsub), ElevatorL2(self.elevatorsub))
        # self.teleopL3 = commands2.ParallelCommandGroup(WristL3(self.wristsub), ElevatorL3(self.elevatorsub))
        # self.teleopL4 = commands2.ParallelCommandGroup(WristL4(self.wristsub), ElevatorL4(self.elevatorsub))
        # self.teleopBarge = commands2.ParallelCommandGroup(WristBarge(self.wristsub), ElevatorBarge(self.elevatorsub))
        # self.teleopHome = commands2.ParallelCommandGroup(WristHome(self.wristsub), ElevatorHome(self.elevatorsub))

        
        #Auto command groups
        # self.autoL2 = commands2.ParallelCommandGroup(AutoWristL2(self.wristsub), AutoElevatorL2(self.elevatorsub))
        # self.autoL3 = commands2.ParallelCommandGroup(AutoWristL3(self.wristsub), AutoElevatorL3(self.elevatorsub))
        # self.autoL4 = commands2.ParallelCommandGroup(AutoWristL4(self.wristsub), AutoElevatorL4(self.elevatorsub))
        # self.AutoBarge = commands2.ParallelCommandGroup(AutoWristBarge(self.wristsub), AutoElevatorBarge(self.elevatorsub))
        # self.autoHome = commands2.ParallelCommandGroup(AutoWristHome(self.wristsub), AutoElevatorHome(self.elevatorsub))
        
        
        #Path planner commands
        # NamedCommands.registerCommand("autoL2", self.autoL2)
        # NamedCommands.registerCommand("autoL3", self.autoL3)
        # NamedCommands.registerCommand("autoL4", self.autoL4)
        # NamedCommands.registerCommand("autoBarge", self.AutoBarge)
        # NamedCommands.registerCommand("autoHome", self.autoHome)
        # NamedCommands.registerCommand("autoIntake", AutoIntakeCommand(self.Intakesub))
        # NamedCommands.registerCommand("autoOuttake", AutoOuttakeCommand(self.Intakesub))
        
        # Configure Bindings
        self.configureButtonBindings()
        self.autoChooser = AutoBuilder.buildAutoChooser("AutoDriveBack")
        SmartDashboard.putData("Auto Chooser", self.autoChooser)
        logger.info("Robot container created")
        self.autoChooser.addOption("Score1AlgaeThenBackup", PathPlannerAuto("Score1AlgaeThenBackup"))
    
    def get_autonomous_command(self):
        # return self.autoChooser.getSelected()

    # Create a path following command using AutoBuilder. This will also trigger event markers.
        return self.autoChooser.getSelected()

    def configureButtonBindings(self):
        pass
        
        # Default Commands
        # self.testSub.setDefaultCommand(MotionWithJoystick(self.testSub))
        self.elevatorsub.setDefaultCommand(ElevatorWithJoysticks(self.elevatorsub))
        # self.wristsub.setDefaultCommand(wristWithJoystick(self.wristsub))
        # self.drivetrainSub.setDefaultCommand(driveWithJoystickCommand(self.drivetrainSub, self.visionSub)) # Additional Buttons used: A
        
        # # Intake Intake Commands
        # self.OperatorController.leftBumper().onTrue(IntakeCommand(self.Intakesub))
        # self.OperatorController.leftBumper().onFalse(IntakeStop(self.Intakesub))
        # self.OperatorController.rightBumper().onTrue(OutakeCommand(self.Intakesub))
        # self.OperatorController.rightBumper().onFalse(IntakeStop(self.Intakesub))
        
        # # Elevator and Wrist Teleop PID Commands
        # self.OperatorController.y().whileTrue(self.teleopL4) # Considering making it to "on true" to only have to press once
        # self.OperatorController.x().whileTrue(self.teleopL3)
        # self.OperatorController.a().whileTrue(self.teleopL2)
        # self.OperatorController.b().whileTrue(self.teleopHome)
        
        # # Hang Commands
        # self.DriverController.a().whileTrue(hangBackwards(self.hangSub))
        # self.DriverController.a().whileFalse(hangStop(self.hangSub))
        # self.DriverController.y().whileTrue(hangForward(self.hangSub))
        # self.DriverController.y().whileFalse(hangStop(self.hangSub))
        
        # Elevator PID Commands
        self.OperatorController.a().whileTrue(ElevatorL2(self.elevatorsub))
        self.OperatorController.x().whileTrue(ElevatorL3(self.elevatorsub))
        # self.OperatorController.y().whileTrue(ElevatorL4(self.elevatorsub))
        # self.OperatorController.b().whileTrue(ElevatorHome(self.elevatorsub))
        
        # Intake Wrist PID Commands
        # self.OperatorController.a().whileTrue(WristL2(self.Intakesub)) # Considering making it to "on true" to only have to press once
        # self.OperatorController.x().whileTrue(WristL3(self.Intakesub))
        # self.OperatorController.y().whileTrue(WristL4(self.Intakesub))