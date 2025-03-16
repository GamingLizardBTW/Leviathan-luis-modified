import wpilib
from phoenix6 import controls, hardware, configs, StatusSignal
from phoenix6.base_status_signal import BaseStatusSignal
import commands2
import wpilib.drive
import wpilib.shuffleboard
import wpimath
import wpimath.controller
from wpimath.geometry import Pose2d, Rotation2d, Translation2d
from wpimath.kinematics import (
    SwerveDrive4Kinematics,
    SwerveDrive4Odometry,
    ChassisSpeeds,
    SwerveModuleState,
    SwerveModulePosition
)
from navx import AHRS
from wpilib import SPI
from wpilib import SmartDashboard, shuffleboard, Field2d
import wpimath.trajectory

import constants
from constants import OP, ELEC, PHYS, CVR, SW, MECH, SW

import navx
import math

from pathplannerlib.auto import AutoBuilder
from pathplannerlib.controller import PPHolonomicDriveController
from pathplannerlib.config import RobotConfig, PIDConstants
from wpilib import DriverStation

import logging
logger = logging.getLogger("drivetrain")

class SwerveModule:
    def __init__(self,
                 driveMotorID: int, 
                 turnMotorID: int, 
                 turnAbsoluteEncoderID: int,
                turnAbsoluteEncoderOffset: float) -> None:
        
        self.driveMotor = hardware.TalonFX(driveMotorID)
        self.turnMotor = hardware.TalonFX(turnMotorID)

        self.driveMotor.setNeutralMode(ELEC.driveMotor_neutral)
        self.turnMotor.setNeutralMode(ELEC.steerMotor_neutral)

        self.turnAbsoluteEncoder = wpilib.DutyCycleEncoder(turnAbsoluteEncoderID, 1, turnAbsoluteEncoderOffset)
        self.turnAbsoluteEncoderOffset = turnAbsoluteEncoderOffset

        self.driveMotorOutput = controls.VelocityVoltage(0).with_slot(0)
        driveMotorConfig = configs.TalonFXConfiguration()
        driveMotorConfig.slot0.k_s = SW.swerve_drive_kS
        driveMotorConfig.slot0.k_v = SW.swerve_drive_kV
        driveMotorConfig.slot0.k_p = SW.swerve_drive_kP
        driveMotorConfig.slot0.k_i = SW.swerve_drive_kI
        driveMotorConfig.slot0.k_d = SW.swerve_drive_kD
        # driveMotorConfig.voltage.peak_forward_voltage = 8
        # driveMotorConfig.voltage.peak_reverse_voltage = -8
        self.driveMotor.configurator.apply(driveMotorConfig)

        self.turnPIDcontroller = wpimath.controller.PIDController(SW.swerve_steer_kP,
                                                                   SW.swerve_steer_kI,
                                                                   SW.swerve_steer_kD)
        self.turnPIDcontroller.enableContinuousInput(-math.pi, math.pi)

    def getState(self) -> SwerveModuleState:
        swerveModuleMeterPerSecond = (
            self.driveMotor.get_rotor_velocity().value / 
            (MECH.swerve_module_driving_gearing_ratio) * 
            (PHYS.wheel_circumference_in_inch) * 
            (CVR.meterPerInch)
        )

        absoluteEncoderPositionInRadian = Rotation2d(self.turnAbsoluteEncoder.get() * CVR.radianPerRotation - math.pi)

        return SwerveModuleState(swerveModuleMeterPerSecond, absoluteEncoderPositionInRadian)
    
    def getPosition(self) -> SwerveModulePosition:

        swerveModulePosition = (
            self.driveMotor.get_rotor_position().value /
            (MECH.swerve_module_driving_gearing_ratio) * 
            (PHYS.wheel_circumference_in_inch) * 
            (CVR.meterPerInch)
        )

        absoluteEncoderPositionInRadian = Rotation2d(self.turnAbsoluteEncoder.get() * CVR.radianPerRotation - math.pi)
        
        return SwerveModulePosition(swerveModulePosition, absoluteEncoderPositionInRadian)
    
    def getAbsoluteEncoderValue(self):
        return self.turnAbsoluteEncoder.get()

        # return self.turnAbsoluteEncoder.get() + self.turnAbsoluteEncoderOffset
    
    def getAbsoluteEncoderValueInRadians(self):
        return (self.turnAbsoluteEncoder.get() + self.turnAbsoluteEncoderOffset) * CVR.radianPerRotation
    
    def getTurnMotorEncoderValue(self):
        # if self.turnMotor.get_rotor_position().value >= MECH.swerve_module_steering_gearing_ratio or self.turnMotor.get_rotor_position().value <= 0:
        #     self.turnMotor.set_position(0)
        return self.turnMotor.get_rotor_position().value / MECH.swerve_module_steering_gearing_ratio
    
    def getSteeringSetpoint(self, desireState: SwerveModuleState):
        return desireState.angle.radians()
    
    def getTurnMotorPositionInRadian(self) -> float:
        # if self.turnMotor.get_rotor_position().value >= MECH.swerve_module_steering_gearing_ratio or self.turnMotor.get_rotor_position().value <= 0:
        #     self.turnMotor.set_position(0)
        # if (self.turnMotor.get_rotor_position().value / MECH.swerve_module_steering_gearing_ratio) >= 1 or (self.turnMotor.get_rotor_position().value / MECH.swerve_module_steering_gearing_ratio) <= 0:
        #     self.turnMotor.set_position(0)
        return self.turnMotor.get_rotor_position().value / MECH.swerve_module_steering_gearing_ratio * math.tau - math.pi
    
    def resetEncoders(self):
        self.driveMotor.set_position(0)
        #Calibrate turnMotor's built-in encoder value based on the reading of the absolute encoder, 
        #convert from a 0 to 1 scale to a 0 to 150/7(about 21.4) scale because 150 motor rotation is 7 drivetrain rotation
        #In this case, absolute encoder increase value by turning ccw, while built-in encoder increase value by turning cw,
        #so you have to subtract 1 by the absolute encoder value to have it increase by turning cw.
        self.turnMotor.set_position(self.getAbsoluteEncoderValue() * MECH.swerve_module_steering_gearing_ratio)

    def getDrivingSpeed(self):
        swerveModuleMeterPerSecond = (
            self.driveMotor.get_rotor_velocity().value / 
            (MECH.swerve_module_driving_gearing_ratio) * 
            (PHYS.wheel_circumference_in_inch) * 
            (CVR.meterPerInch)
        )
        return swerveModuleMeterPerSecond

    def getDesiredSpeed(self, desiredState: SwerveModuleState):
        return desiredState.speed

    def setDesiredState(self, desiredState: SwerveModuleState) -> None:

        turnEncoderPosition = Rotation2d(self.turnAbsoluteEncoder.get() * math.tau - math.pi)
        desiredState.optimize(turnEncoderPosition)
        desiredState.cosineScale(turnEncoderPosition)

        desiredDrivingSpeed = (desiredState.speed / 
                               CVR.meterPerInch /
                               PHYS.wheel_circumference_in_inch *
                               MECH.swerve_module_driving_gearing_ratio)

        turnMotorOutput = self.turnPIDcontroller.calculate(self.turnAbsoluteEncoder.get() * math.tau - math.pi, desiredState.angle.radians())

        self.driveMotor.set_control(self.driveMotorOutput.with_velocity(desiredDrivingSpeed))
        self.turnMotor.set(turnMotorOutput)

class drivetrainSubsystemClass(commands2.Subsystem):

    def __init__(self) -> None:
        trackwidth = PHYS.track_width_in_inch * CVR.meterPerInch
        wheelbase = PHYS.wheel_base_in_inch * CVR.meterPerInch
        self.frontLeftModuleLocation = Translation2d((wheelbase/2), (trackwidth/2))
        self.frontRightModuleLocation = Translation2d((wheelbase/2), -(trackwidth/2))
        self.backLeftModuleLocation = Translation2d(-(wheelbase/2), (trackwidth/2))
        self.backRightModuleLocation = Translation2d(-(wheelbase/2), -(trackwidth/2))
        #forward is positive X and left is positive Y.

        self.frontLeftModule = SwerveModule(ELEC.LF_drive_CAN_ID, ELEC.LF_steer_CAN_ID, ELEC.LF_encoder_DIO, SW.lf_enc_zeropos)
        self.frontRightModule = SwerveModule(ELEC.RF_drive_CAN_ID, ELEC.RF_steer_CAN_ID, ELEC.RF_encoder_DIO, SW.rf_enc_zeropos)
        self.backLeftModule = SwerveModule(ELEC.LB_drive_CAN_ID, ELEC.LB_steer_CAN_ID, ELEC.LB_encoder_DIO, SW.lb_enc_zeropos)
        self.backRightModule = SwerveModule(ELEC.RB_drive_CAN_ID, ELEC.RB_steer_CAN_ID, ELEC.RB_encoder_DIO, SW.rb_enc_zeropos)

        self.gyro = navx.AHRS.create_spi()

        self.kinematics = SwerveDrive4Kinematics(
            self.frontLeftModuleLocation,
            self.frontRightModuleLocation,
            self.backLeftModuleLocation,
            self.backRightModuleLocation
            )
        
        self.odometry = SwerveDrive4Odometry(
            self.kinematics,
            self.gyro.getRotation2d(),
            (
            self.frontLeftModule.getPosition(),
            self.frontRightModule.getPosition(),
            self.backLeftModule.getPosition(),
            self.backRightModule.getPosition()
            ),
        )

        self.gyro.reset()

        if not AutoBuilder.isConfigured():
            logger.info("About to configure AutoBuilder...")
            AutoBuilder.configure(
                self.getRobotPose,
                self.odometry.resetPose,
                lambda: self.kinematics.toChassisSpeeds((self.frontLeftModule.getState(),
                                                        self.frontRightModule.getState(),
                                                        self.backLeftModule.getState(),
                                                        self.backRightModule.getState())),
                self.driveRobotRelative,
                PPHolonomicDriveController(PIDConstants(2,0,0),
                                        PIDConstants(2,0,0)),
                SW.path_planner_config,
                self.shouldFlipPath,
                #If the alliance is red, this line will return true which flips the path(primary path are made based on blue)
                self
            )

    def drive(self, 
              xSpeed: float, 
              ySpeed: float, 
              rotation: float, 
              fieldRelative: bool, 
              periodSeconds: float,
              resetGyro: bool):

        self.swerveModuleState = self.kinematics.toSwerveModuleStates(
            ChassisSpeeds.discretize(
                (
                ChassisSpeeds.fromFieldRelativeSpeeds(
                    xSpeed, ySpeed, rotation, self.gyro.getRotation2d()
                )
                if fieldRelative
                else ChassisSpeeds(xSpeed, ySpeed, rotation)
                ),
            periodSeconds,
            )
        )
        SwerveDrive4Kinematics.desaturateWheelSpeeds(self.swerveModuleState, OP.max_speed)

        self.frontLeftModule.setDesiredState(self.swerveModuleState[0])
        self.frontRightModule.setDesiredState(self.swerveModuleState[1])
        self.backLeftModule.setDesiredState(self.swerveModuleState[2])
        self.backRightModule.setDesiredState(self.swerveModuleState[3])
        
        if resetGyro == True:
            self.gyro.reset()

    def driveRobotRelative(self, robotRelativeSpeed: ChassisSpeeds, feedForward) -> None:
        swerveModuleState = self.kinematics.toSwerveModuleStates(ChassisSpeeds.discretize(robotRelativeSpeed, 0.02))

        self.frontLeftModule.setDesiredState(swerveModuleState[0])
        self.frontRightModule.setDesiredState(swerveModuleState[1])
        self.backLeftModule.setDesiredState(swerveModuleState[2])
        self.backRightModule.setDesiredState(swerveModuleState[3])
        
        self.showRobotPose()

    def shouldFlipPath(self) -> bool:
        # return DriverStation.getAlliance() == DriverStation.Alliance.kRed
        return False


    def updateOdometry(self) -> None:
        self.odometry.update(            
            self.gyro.getRotation2d(),
            (
            self.frontLeftModule.getPosition(),
            self.frontRightModule.getPosition(),
            self.backLeftModule.getPosition(),
            self.backRightModule.getPosition()
            )
        )
        
    def getRobotPose(self) -> Pose2d:
        self.updateOdometry()
        pose = self.odometry.getPose()
        return pose

    def resetAllEncoders(self) -> None:
        self.frontLeftModule.resetEncoders()
        self.frontRightModule.resetEncoders()
        self.backLeftModule.resetEncoders()
        self.backRightModule.resetEncoders()

    def showAbsoluteEncoderValues(self) -> None:
        SmartDashboard.putNumber("frontLeftEncoder", self.frontLeftModule.getAbsoluteEncoderValue())
        SmartDashboard.putNumber("frontRightEncoder", self.frontRightModule.getAbsoluteEncoderValue())
        SmartDashboard.putNumber("backLeftEncoder", self.backLeftModule.getAbsoluteEncoderValue())
        SmartDashboard.putNumber("backRightEncoder", self.backRightModule.getAbsoluteEncoderValue())

    def showTurnMotorEncoderValues(self) -> None:
        SmartDashboard.putNumber("frontLeftMotorEncoder", self.frontLeftModule.getTurnMotorEncoderValue())
        SmartDashboard.putNumber("frontRightMotorEncoder", self.frontRightModule.getTurnMotorEncoderValue())
        SmartDashboard.putNumber("backLeftMotorEncoder", self.backLeftModule.getTurnMotorEncoderValue())
        SmartDashboard.putNumber("backRightMotorEncoder", self.backRightModule.getTurnMotorEncoderValue())

        # SmartDashboard.putNumber("frontLeftMotorEncoder", self.frontLeftModule.getTurnMotorEncoderValue() / MECH.swerve_module_steering_gearing_ratio)
        # SmartDashboard.putNumber("frontRightMotorEncoder", self.frontRightModule.getTurnMotorEncoderValue() / MECH.swerve_module_steering_gearing_ratio)
        # SmartDashboard.putNumber("backLeftMotorEncoder", self.backLeftModule.getTurnMotorEncoderValue() / MECH.swerve_module_steering_gearing_ratio)
        # SmartDashboard.putNumber("backRightMotorEncoder", self.backRightModule.getTurnMotorEncoderValue() / MECH.swerve_module_steering_gearing_ratio)

        # SmartDashboard.putNumber("frontLeftMotorEncoder", self.frontLeftModule.getTurnMotorPositionInRadian())
        # SmartDashboard.putNumber("frontRightMotorEncoder", self.frontRightModule.getTurnMotorPositionInRadian())
        # SmartDashboard.putNumber("backLeftMotorEncoder", self.backLeftModule.getTurnMotorPositionInRadian())
        # SmartDashboard.putNumber("backRightMotorEncoder", self.backRightModule.getTurnMotorPositionInRadian())

    def showAbsoluteEncoderValuesInRadians(self) -> None:
        SmartDashboard.putNumber("frontLeftRadian", (self.frontLeftModule.getAbsoluteEncoderValueInRadians() - math.pi))
        SmartDashboard.putNumber("frontRightRadian", (self.frontRightModule.getAbsoluteEncoderValueInRadians() - math.pi))
        SmartDashboard.putNumber("backLeftRadian", (self.backLeftModule.getAbsoluteEncoderValueInRadians() - math.pi))
        SmartDashboard.putNumber("backRightRadian", (self.backRightModule.getAbsoluteEncoderValueInRadians() - math.pi))

    def showSteeringSetpoint(self) -> None:
        SmartDashboard.putNumber("frontLeftSetpoint", self.frontLeftModule.getSteeringSetpoint(self.swerveModuleState[0]))
        SmartDashboard.putNumber("frontRightSetpoing", self.frontRightModule.getSteeringSetpoint(self.swerveModuleState[1]))
        SmartDashboard.putNumber("backLeftSetpoint", self.backLeftModule.getSteeringSetpoint(self.swerveModuleState[2]))
        SmartDashboard.putNumber("backRightSetpoint", self.backRightModule.getSteeringSetpoint(self.swerveModuleState[3]))

    def showDrivingSpeed(self) -> None:
        SmartDashboard.putNumber("frontLeftSpeed", self.frontLeftModule.getDrivingSpeed())
        SmartDashboard.putNumber("frontRightSpeed", self.frontRightModule.getDrivingSpeed())
        SmartDashboard.putNumber("backLeftSpeed", self.backLeftModule.getDrivingSpeed())
        SmartDashboard.putNumber("backRightSpeed", self.backRightModule.getDrivingSpeed())

    def showDesiredSpeed(self) -> None:
        SmartDashboard.putNumber("LFdesiredSpeed", self.frontLeftModule.getDesiredSpeed(self.swerveModuleState[0]))
        SmartDashboard.putNumber("RFdesiredSpeed", self.frontRightModule.getDesiredSpeed(self.swerveModuleState[1]))
        SmartDashboard.putNumber("LBdesiredSpeed", self.backLeftModule.getDesiredSpeed(self.swerveModuleState[2]))        
        SmartDashboard.putNumber("RBdesiredSpeed", self.backRightModule.getDesiredSpeed(self.swerveModuleState[3]))
    
    def showRobotPose(self) -> None:
        field = Field2d()
        field.setRobotPose(self.getRobotPose())
        SmartDashboard.putData("Field", field)
        
    def periodic(self) -> None:
        self.showRobotPose()
        
    # def showHeading(self) -> None:
    #     shuffleboard.Shuffleboard.getTab("Heading").add(self.gyro)
        
    # def log(self):
    #     table = "Drive/"

    #     pose = self.odometry.getPose
    #     wpilib.SmartDashboard.putNumber(table + "X", pose.X())
    #     wpilib.SmartDashboard.putNumber(table + "Y", pose.Y())
    #     wpilib.SmartDashboard.putNumber(table + "Heading", pose.rotation().degrees())

    #     chassisSpeeds = self.getChassisSpeeds()
    #     wpilib.SmartDashboard.putNumber(table + "VX", chassisSpeeds.vx)
    #     wpilib.SmartDashboard.putNumber(table + "VY", chassisSpeeds.vy)
    #     wpilib.SmartDashboard.putNumber(
    #         table + "Omega Degrees", chassisSpeeds.omega_dps
    #     )

    #     wpilib.SmartDashboard.putNumber(
    #         table + "Target VX", self.targetChassisSpeeds.vx
    #     )
    #     wpilib.SmartDashboard.putNumber(
    #         table + "Target VY", self.targetChassisSpeeds.vy
    #     )
    #     wpilib.SmartDashboard.putNumber(
    #         table + "Target Omega Degrees", self.targetChassisSpeeds.omega_dps
    #     )

    #     self.frontLeft.log()
    #     self.frontRight.log()
    #     self.backLeft.log()
    #     self.backRight.log()

    #     self.debugField.getRobotObject().setPose(self.poseEst.getEstimatedPosition())
    #     self.debugField.getObject("SwerveModules").setPoses(self.getModulePoses())