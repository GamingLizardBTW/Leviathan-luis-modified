from wpilib import XboxController
from wpilib import SmartDashboard
import subsystems.DrivetrainSubsystem
import commands2

# Constants
from constants import OP, ELEC

# Subsystems
import subsystems.IntakeSubsystem
import subsystems.WristSubsystem
import subsystems.ElevatorSubsystem
#import subsystems.VisionSubsystem
import subsystems.HangSubsystem
import subsystems.LEDSubsytem 

# Commands
from commands.IntakeCommands import IntakeCommand, OutakeCommand, IntakeStop, AutoIntakeCommand, AutoOuttakeCommand
from commands.WristCommands import wristWithJoystick, WristL2, WristL3, WristL4, WristHome, CoralMode, AlgaeMode, WristStation, WristGroundIntake
from commands.WristCommands import CoralL2, CoralL3, CoralL4, AutoWristBarge, AutoWristHome, AutoWristHumanPlayer, AutoWristProcessor, AlgaeL2, AlgaeL3   # Auto
from commands.ElevatorCommands import ElevatorWithJoysticks, ElevatorL2, ElevatorL3, ElevatorL4, ElevatorHome, ElevatorToStation
from commands.ElevatorCommands import AutoElevatorL2, AutoElevatorL3, AutoElevatorL4, AutoElevatorHome, AutoElevatorHumanStation     # Auto
from commands.HangCommands import hangBackwards, hangForward, hangStop
from commands.LEDCommands import SetLEDColorCommand

from commands.DrivetrainCommands import driveWithJoystickCommand
#from commands.SingleDrivetrainCommand import singledriveWithJoystickCommand
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
        #self.visionSub = subsystems.VisionSubsystem.visionSubsystem()
        self.Intakesub = subsystems.IntakeSubsystem.IntakeSubsystemClass()
        self.wristsub = subsystems.WristSubsystem.WristSubsystemClass()
        self.elevatorsub = subsystems.ElevatorSubsystem.ElevatorSubsystemClass()
        self.drivetrainSub = subsystems.DrivetrainSubsystem.drivetrainSubsystemClass()
        self.hangSub = subsystems.HangSubsystem.HangSubsystem()
        self.ledsub = subsystems.LEDSubsytem.LED_5v_Subsystem(pwm_port = ELEC.pwm_port, length = ELEC.LED_length)

        
        # Controllers
        self.DriverController = commands2.button.CommandXboxController(OP.driver_controller)
        self.OperatorController = commands2.button.CommandXboxController(OP.operator_controller)
        #self.SingleController = commands2.button.CommandXboxController(OP.single_controller)
        
        #Command groups
        self.teleopL2 = commands2.ParallelCommandGroup(WristL2(self.wristsub), ElevatorL2(self.elevatorsub))
        self.teleopL3 = commands2.ParallelCommandGroup(WristL3(self.wristsub), ElevatorL3(self.elevatorsub, self.wristsub))
        self.teleopL4 = commands2.ParallelCommandGroup(WristL4(self.wristsub), ElevatorL4(self.elevatorsub))
        self.teleopGroundIntake = commands2.ParallelCommandGroup(WristGroundIntake(self.wristsub), ElevatorHome(self.elevatorsub))
        self.teleopStation = commands2.ParallelCommandGroup(WristStation(self.wristsub), ElevatorToStation(self.elevatorsub, self.wristsub))
        self.teleopHome = commands2.ParallelCommandGroup(WristHome(self.wristsub), ElevatorHome(self.elevatorsub))
        
        # self.teleopBarge = commands2.ParallelCommandGroup(WristBarge(self.wristsub), ElevatorL4(self.elevatorsub))
        # self.teleopProcessor = commands2.ParallelCommandGroup(WristProcessor(self.wristsub), ElevatorHome(self.elevatorsub))

        
        #Auto command groups
        #  ------------------------ Coral -----------------------------------
        self.coralL2 = commands2.ParallelCommandGroup(CoralL2(self.wristsub), AutoElevatorL2(self.elevatorsub))
        self.coralL3 = commands2.ParallelCommandGroup(CoralL3(self.wristsub), AutoElevatorL3(self.elevatorsub))
        self.coralL4 = commands2.ParallelCommandGroup(CoralL4(self.wristsub), AutoElevatorL4(self.elevatorsub))
        self.autoHumanPlayer = commands2.ParallelCommandGroup(AutoWristHumanPlayer(self.wristsub), AutoElevatorHumanStation(self.elevatorsub))
        
        # -------------------------- Algae ----------------------------------
        self.algaeL2 = commands2.ParallelCommandGroup(AlgaeL2(self.wristsub), AutoElevatorL2(self.elevatorsub))
        self.algaeL3 = commands2.ParallelCommandGroup(AlgaeL3(self.wristsub), AutoElevatorL3(self.elevatorsub))
        self.AutoBarge = commands2.ParallelCommandGroup(AutoWristBarge(self.wristsub), AutoElevatorL4(self.elevatorsub))
        self.AutoProcessor = commands2.ParallelCommandGroup(AutoWristProcessor(self.wristsub), AutoElevatorHome(self.elevatorsub))
        
        # -------------------------- Home -----------------------------------
        self.autoHome = commands2.ParallelCommandGroup(AutoWristHome(self.wristsub), AutoElevatorHome(self.elevatorsub))
        
        
        #Path planner commands
        NamedCommands.registerCommand("autoL2", self.coralL2)
        NamedCommands.registerCommand("autoL3", self.coralL3)
        NamedCommands.registerCommand("autoL4", self.coralL4)
        NamedCommands.registerCommand("autoBarge", self.AutoBarge)
        NamedCommands.registerCommand("autoHome", self.autoHome)
        NamedCommands.registerCommand("autoIntake", AutoIntakeCommand(self.Intakesub))
        NamedCommands.registerCommand("autoOuttake", AutoOuttakeCommand(self.Intakesub))
        
        # Configure Bindings
        self.configureButtonBindings()
        self.autoChooser = AutoBuilder.buildAutoChooser("MidAutoDriveBack")
        SmartDashboard.putData("Auto Chooser", self.autoChooser)
        logger.info("Robot container created")
        self.autoChooser.addOption("LeftAutoDriveBack", PathPlannerAuto("LeftAutoDriveBack"))
        self.autoChooser.addOption("RightAutoDriveBack", PathPlannerAuto("RightAutoDriveBack"))
        self.autoChooser.addOption("LeftAuto", PathPlannerAuto("LeftAuto"))
        self.autoChooser.addOption("RightAuto", PathPlannerAuto("RightAuto"))
        self.autoChooser.addOption("MidOneL4Coral", PathPlannerAuto("MidOneL4Coral"))
        self.autoChooser.addOption("MidOneL4CoralThenBarge", PathPlannerAuto("MidOneL4CoralThenBarge"))
    
    def get_autonomous_command(self):
        # return self.autoChooser.getSelected()

    # Create a path following command using AutoBuilder. This will also trigger event markers.
        return self.autoChooser.getSelected()

    def configureButtonBindings(self):
        pass
        
        # Default Commands
        # 2 seperate driver
        self.drivetrainSub.setDefaultCommand(driveWithJoystickCommand(self.drivetrainSub))
        # Single controller driver
        #self.drivetrainSub.setDefaultCommand(singledriveWithJoystickCommand(self.drivetrainSub))
        
        # # Intake Intake Commands
        self.OperatorController.leftBumper().onTrue(IntakeCommand(self.Intakesub))
        self.OperatorController.leftBumper().onFalse(IntakeStop(self.Intakesub))
        self.OperatorController.rightBumper().onTrue(OutakeCommand(self.Intakesub))
        self.OperatorController.rightBumper().onFalse(IntakeStop(self.Intakesub))
        
        # # Hang Commands
        self.DriverController.povDown().whileTrue(hangBackwards(self.hangSub))
        self.DriverController.povDown().whileFalse(hangStop(self.hangSub))
        self.DriverController.povUp().whileTrue(hangForward(self.hangSub))
        self.DriverController.povUp().whileFalse(hangStop(self.hangSub))
        
        # # Elevator and Wrist Teleop PID Commands (Considering making it to "on true" to only have to press once)
        self.OperatorController.a().whileTrue(self.teleopL2) # Alge L2 & coral L2
        self.OperatorController.x().whileTrue(self.teleopL3) # Alge L3 & coral L3
        self.OperatorController.y().whileTrue(self.teleopL4) # Barge & coral L4
        self.OperatorController.b().whileTrue(self.teleopStation) # Human Player & Processor
        self.OperatorController.povDown().whileTrue(self.teleopHome) # Home robot
        self.OperatorController.povUp().whileTrue(self.teleopGroundIntake) # Home robot
        
        # Change target mode for wrist
        self.OperatorController.start().onTrue(CoralMode(self.wristsub, self.ledsub))
        self.OperatorController.button(7).onTrue(AlgaeMode(self.wristsub, self.ledsub))

        # Buttons for single controller on port 3
        #self.SingleController.start().onTrue(CoralMode(self.wristsub, self.ledsub))
        #self.SingleController.button(7).onTrue(AlgaeMode(self.wristsub, self.ledsub))
        #self.SingleController.a().whileTrue(self.teleopL2) # Alge L2 & coral L2
        #self.SingleController.x().whileTrue(self.teleopL3) # Alge L3 & coral L3
        #self.SingleController.y().whileTrue(self.teleopL4) # Barge & coral L4
        #self.SingleController.b().whileTrue(self.teleopStation) # Human Player & Processor
        #self.SingleController.povDown().whileTrue(self.teleopHome) # Home robot
        #self.SingleController.povUp().whileTrue(self.teleopGroundIntake) # Home robot
        #self.SingleController.povLeft().whileTrue(hangBackwards(self.hangSub))
        #self.SingleController.povLeft().whileFalse(hangStop(self.hangSub))
        #self.SingleController.povRight().whileTrue(hangForward(self.hangSub))
        #self.SingleController.povRight().whileFalse(hangStop(self.hangSub))
        #self.SingleController.leftBumper().onTrue(IntakeCommand(self.Intakesub))
        #self.SingleController.leftBumper().onFalse(IntakeStop(self.Intakesub))
        #self.SingleController.rightBumper().onTrue(OutakeCommand(self.Intakesub))
        #self.SingleController.rightBumper().onFalse(IntakeStop(self.Intakesub))
        
        # # LEDS
        # self.OperatorController.button(7).onTrue(SetLEDColorCommand(self.ledsub, (0, 255, 255)))  # cyan
        # self.OperatorController.start().onTrue(SetLEDColorCommand(self.ledsub, (255, 255, 255)))  # white
        # self.OperatorController.povDown().onTrue(SetLEDColorCommand(self.ledsub, (0, 0, 0)))  # Off