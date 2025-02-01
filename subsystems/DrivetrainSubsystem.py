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
import wpimath.trajectory

import constants
from constants import OP, ELEC, PHYS, CVR, SW

import navx
import math

class SwerveModule:
    def __init__(self,
                 driveMotorID: int, 
                 turnMotorID: int, 
                 turnAbsoluteEncoderID: int,
                turnAbsoluteEncoderOffset: float) -> None:
        
        self.driveMotor = hardware.TalonFX(driveMotorID)
        self.turnMotor = hardware.TalonFX(turnMotorID)

        self.driveMotorOutput = controls.DutyCycleOut(0)
        self.TurnMotoOutput = controls.DutyCycleOut(0)

        self.driveMotor.setNeutralMode(ELEC.driveMotor_neutral)
        self.turnMotor.setNeutralMode(ELEC.steerMotor_neutral)

        self.turnAbsoluteEncoder = wpilib.DutyCycleEncoder(turnAbsoluteEncoderID)
        self.turnAbsoluteEncoderOffset = turnAbsoluteEncoderOffset

        self.drivePIDcontroller = wpimath.controller.PIDController(1,0,0)
        self.turnPIDcontroller = wpimath.controller.ProfiledPIDController(1,0,0,wpimath.trajectory.TrapezoidProfile.Constraints(OP.max_steering_velocity, OP.max_steering_acceleration))
        #self.turnPIDcontroller = wpimath.controller.PIDController(0.3,0,0)
        self.turnPIDcontroller.setTolerance(0.25)
        self.turnPIDcontroller.enableContinuousInput(-math.pi, math.pi)
        #self.turnPIDcontroller.enableContinuousInput(0, math.tau)

    def getState(self) -> SwerveModuleState:
        swerveModuleMeterPerSecond = (
            self.driveMotor.get_rotor_velocity().value / 
            (constants.MECH.swerve_module_driving_gearing_ratio) * 
            (constants.PHYS.wheel_circumference_in_inch) * 
            (constants.CVR.meterPerInch)
        )

        absoluteEncoderPositionInRadian = Rotation2d((self.turnAbsoluteEncoder.get() + self.turnAbsoluteEncoderOffset) * constants.CVR.radianPerRotation)

        return SwerveModuleState(swerveModuleMeterPerSecond, absoluteEncoderPositionInRadian)
    
    def getPosition(self) -> SwerveModulePosition:

        swerveModulePosition = (
            self.driveMotor.get_rotor_position().value /
            (constants.MECH.swerve_module_driving_gearing_ratio) * 
            (constants.PHYS.wheel_circumference_in_inch) * 
            (constants.CVR.meterPerInch)
        )

        absoluteEncoderPositionInRadian = Rotation2d((self.turnAbsoluteEncoder.get() + self.turnAbsoluteEncoderOffset) * constants.CVR.radianPerRotation)
        
        return SwerveModulePosition(swerveModulePosition, absoluteEncoderPositionInRadian)
    
    def getAbsoluteEncoderValue(self, encoderOffset: float):
        return self.turnAbsoluteEncoder.get() + encoderOffset
    
    def getAbsoluteEncoderValueInRadians(self, encoderOffset: float):
        return (self.turnAbsoluteEncoder.get() + encoderOffset) * constants.CVR.radianPerRotation
    
    def getSteeringSetpoint(self, desireState: SwerveModuleState):
        return desireState.angle.radians()

    
    def setDesiredState(self, desiredState: SwerveModuleState) -> None:

        turnEncoderPosition = Rotation2d(((self.turnAbsoluteEncoder.get() + self.turnAbsoluteEncoderOffset) * constants.CVR.radianPerRotation))
        desiredState.optimize(turnEncoderPosition)
        desiredState.cosineScale(turnEncoderPosition)

        swerveModuleMeterPerSecond = (
            self.driveMotor.get_rotor_velocity().value / 
            (constants.MECH.swerve_module_driving_gearing_ratio) * 
            (constants.PHYS.wheel_circumference_in_inch) * 
            (constants.CVR.meterPerInch)
        )

        swerveModuleTurnPosition = (self.turnAbsoluteEncoder.get() + self.turnAbsoluteEncoderOffset) * constants.CVR.radianPerRotation

        driveMotorOutput = self.drivePIDcontroller.calculate(swerveModuleMeterPerSecond, desiredState.speed)
        # turnMotorOutput = self.turnPIDcontroller.calculate((swerveModuleTurnPosition - math.pi), desiredState.angle.radians())
        turnMotorOutput = self.turnPIDcontroller.calculate((self.turnAbsoluteEncoder.get() - 1), (desiredState.angle.radians() / math.pi))

        self.driveMotor.setVoltage(driveMotorOutput)
        self.turnMotor.setVoltage(turnMotorOutput)
        #self.turnMotor.set(turnMotorOutput)

class drivetrainSubsystemClass(commands2.Subsystem):

    def __init__(self) -> None:
        trackwidth = constants.PHYS.track_width_in_inch * constants.CVR.meterPerInch
        wheelbase = constants.PHYS.wheel_base_in_inch * constants.CVR.meterPerInch
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

    def drive(self, 
              xSpeed: float, 
              ySpeed: float, 
              rotation: float, 
              fieldRelative: bool, 
              periodSeconds: float):
        
    # def drive(self, 
    #           xSpeed: float, 
    #           ySpeed: float, 
    #           rotation: float, 
    #           periodSeconds: float):

    # def drive(self, 
    #           xSpeed: float, 
    #           ySpeed: float, 
    #           rotation: float, 
    #         ):

        # self.swerveModuleState = self.kinematics.toSwerveModuleStates(
        #     ChassisSpeeds.discretize(
        #         (
        #         ChassisSpeeds.fromFieldRelativeSpeeds(
        #             xSpeed, ySpeed, rotation, self.gyro.getRotation2d()
        #         )
        #         if fieldRelative
        #         else ChassisSpeeds(xSpeed, ySpeed, rotation)
        #         ),
        #     periodSeconds,
        #     )
        # )


        self.swerveModuleState = self.kinematics.toSwerveModuleStates(
                (
                ChassisSpeeds.fromFieldRelativeSpeeds(
                    xSpeed, ySpeed, rotation, self.gyro.getRotation2d()
                )
                if fieldRelative
                else ChassisSpeeds(xSpeed, ySpeed, rotation)
                ),
        )

        # swerveModuleState = self.kinematics.toSwerveModuleStates(
        #         ChassisSpeeds.fromFieldRelativeSpeeds(
        #             xSpeed, ySpeed, rotation, self.gyro.getRotation2d()
        #         )
        # )
        #forward is positive X and left is positive Y.
        SwerveDrive4Kinematics.desaturateWheelSpeeds(self.swerveModuleState, OP.max_speed)

        self.frontLeftModule.setDesiredState(self.swerveModuleState[0])
        self.frontRightModule.setDesiredState(self.swerveModuleState[1])
        self.backLeftModule.setDesiredState(self.swerveModuleState[2])
        self.backRightModule.setDesiredState(self.swerveModuleState[3])

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

    def showAbsoluteEncoderValues(self) -> None:
        wpilib.SmartDashboard.putNumber("frontLeftEncoder", self.frontLeftModule.getAbsoluteEncoderValue(SW.lf_enc_zeropos))
        wpilib.SmartDashboard.putNumber("frontRightEncoder", self.frontLeftModule.getAbsoluteEncoderValue(SW.rf_enc_zeropos))
        wpilib.SmartDashboard.putNumber("backLeftEncoder", self.backLeftModule.getAbsoluteEncoderValue(SW.lb_enc_zeropos))
        wpilib.SmartDashboard.putNumber("backRightEncoder", self.backRightModule.getAbsoluteEncoderValue(SW.rb_enc_zeropos))

    def showAbsoluteEncoderValuesInRadians(self) -> None:
        wpilib.SmartDashboard.putNumber("frontLeftRadian", (self.frontLeftModule.getAbsoluteEncoderValueInRadians(SW.lf_enc_zeropos) - math.pi))
        wpilib.SmartDashboard.putNumber("frontRightRadian", (self.frontRightModule.getAbsoluteEncoderValueInRadians(SW.rf_enc_zeropos) - math.pi))
        wpilib.SmartDashboard.putNumber("backLeftRadian", (self.backLeftModule.getAbsoluteEncoderValueInRadians(SW.lb_enc_zeropos) - math.pi))
        wpilib.SmartDashboard.putNumber("backRightRadian", (self.backRightModule.getAbsoluteEncoderValueInRadians(SW.rb_enc_zeropos) - math.pi))

    def showSteeringSetpoint(self) -> None:
        wpilib.SmartDashboard.putNumber("frontLeftSetpoint", self.frontLeftModule.getSteeringSetpoint(self.swerveModuleState[0]))
        wpilib.SmartDashboard.putNumber("frontRightSetpoing", self.frontRightModule.getSteeringSetpoint(self.swerveModuleState[1]))
        wpilib.SmartDashboard.putNumber("backLeftSetpoint", self.backLeftModule.getSteeringSetpoint(self.swerveModuleState[2]))
        wpilib.SmartDashboard.putNumber("backRightSetpoint", self.backRightModule.getSteeringSetpoint(self.swerveModuleState[3]))