import wpilib
import commands2
import photonlibpy
import logging
import wpinet
# from wpilib import SmartDashboard, Field2d
from constants import OP
import time

# Math
import wpimath.geometry
from wpimath.geometry import Pose3d, Transform3d, Translation3d
from wpimath.units import metersToFeet, metersToInches, inchesToMeters

# Import cam and pose estimation libraries
from photonlibpy import PhotonCamera, PhotonPoseEstimator, PoseStrategy
from robotpy_apriltag import AprilTagField, AprilTagFieldLayout

# Might Use
# from photonlibpy import estimation
# from photonlibpy import generated
# from photonlibpy import networktables
# from photonlibpy import packet
# from photonlibpy import simulation
# from photonlibpy import targeting
# from photonlibpy import estimatedRobotPose

logger = logging.getLogger("Vision")

# Measurement from center of robot to cam
kRobotToCam = wpimath.geometry.Transform3d(
    wpimath.geometry.Translation3d(inchesToMeters(10.375), inchesToMeters(2.5), inchesToMeters(6.25)),
    wpimath.geometry.Rotation3d.fromDegrees(0.0, 0, 0.0),
)

class visionSubsystem(commands2.Subsystem):
    
    def __init__(self) -> None:
        
        # Create coral camera instance
        self.camera = PhotonCamera("Coral_Cam")
        
        # gets latest result from coral camera
        self.result = self.camera.getLatestResult()
        
        # Checks if coral camera detects targets
        self.hasTargets = self.result.hasTargets()
        
        # Recieves the latest targets seen by the coral camera
        self.targets = self.result.getTargets()
        
        # Pose Estimation
        self.camPoseEst = PhotonPoseEstimator(                            # Create PoseEstimation based off cam 
            AprilTagFieldLayout.loadField(AprilTagField.kDefaultField),
            PoseStrategy.LOWEST_AMBIGUITY,
            self.camera,
            kRobotToCam,
        )
        
        # Booleans used for vision
        self.targetVisible = False
        
    def periodic(self) -> None:
        
        # Update Vision Data
        self.result = self.camera.getLatestResult()
        self.hasTargets = self.result.hasTargets()
        self.targets = self.result.getTargets()
        
        # Print Values
        self.printData()
        
    def getTargetIDs(self, id: int): # Return a list of tags beeing seen (untested)
        """
        Returns all the aprilTag id's it currently sees.
        """
        results = self.targets
        if len(results) > 0:
            for i in results:
                if results[-1].getFiducialId() > id:
                    return results[-2].getFiducialId()
    
    def getClosestData(self, dataType: str) -> float:  #Returns the data for the closest/best april tag seen (not a specific ID)
        """
        Returns aprilTag data for the closest aprilTag. If no april tags are seen by camera, returned value is 0.
        
        :param dataType: The type of data you want returned. Current data it can retrun: `Yaw`, `Pitch`, `Skew`, `Area`, `X-Dist`, `Y-Dist`, `Z-Dist`, `ID`.
        """
        
        result = self.targets
        if len(result) == 0: # returns 0 if no apriltags are seen
            return 0
        else:
            result = result[-1] # Get most recent data
            for target in self.targets:
                self.targetVisible = True
                # Return the desired type of data
                if dataType == "Yaw":
                    Data = target.getYaw() # Use this if you want the yaw to zero by pointing at tag
                elif dataType == "Pitch":
                    Data = target.getPitch()
                elif dataType == "Skew":
                    Data = target.getSkew()
                elif dataType == "Area":
                    Data = target.getArea()
                elif dataType == "X-Dist":
                    Data = target.getBestCameraToTarget().X()
                elif dataType == "Y-Dist":
                    Data = target.getBestCameraToTarget().Y()
                elif dataType == "Z-Dist":
                    Data = target.getBestCameraToTarget().Z()
                elif dataType == "X-Rot":
                    Data = target.getBestCameraToTarget().rotation().X()
                elif dataType == "Y-Rot":
                    Data = target.getBestCameraToTarget().rotation().Y()
                elif dataType == "Z-Rot":
                    Data = target.getBestCameraToTarget().rotation().Z() # Use this if you want it to zero when perpendicular to tag
                elif dataType == "ID":
                    Data = target.getFiducialId()
        # logger.info(f"target {dataType}: {Data} ")
        return Data
        

  
    def getTragetData(self, id: int, dataType: str) -> float: # Simpler version to get target data of a specific ID (Trying to fix minor bug but works)
        """
        Returns desired aprilTag data. If desired april tag is not seen by camera, default returned value is 0.
        
        :param ID:       The aprilTag ID you want to get data from.
        :param dataType: The type of data you want returned. Current data it can retrun: `Yaw`, `Pitch`, `Skew`, `Area`, `X-Dist`, `Y-Dist`, `Z-Dist`.
        """
        
        result = self.targets
        if len(result) > 0: # Checks to see if any AprilTags are seen
            # result = result[-1] # Get most recent data
            for target in self.targets:
                if target.getFiducialId() == id: # looks for desired AprilTag ID
                    self.targetVisible = True
                    # Return the desired type of data
                    if dataType == "Yaw":
                        Data = target.getYaw()
                    elif dataType == "Pitch":
                        Data = target.getPitch()
                    elif dataType == "Skew":
                        Data = target.getSkew()
                    elif dataType == "Area":
                        Data = target.getArea()
                    elif dataType == "X-Dist":
                        Data = target.getBestCameraToTarget().X()
                    elif dataType == "Y-Dist":
                        Data = target.getBestCameraToTarget().Y()
                    elif dataType == "Z-Dist":
                        Data = target.getBestCameraToTarget().Z()
                else:
                    return 0
        else:
            return 0
        return Data
  
    def getTragetData2(self, id: int, dataType: str) -> float: # An ettempt to fix this
        """
        Returns desired aprilTag data. If desired april tag is not seen by camera, default returned value is 0.
        
        :param ID:       The aprilTag ID you want to get data from.
        :param dataType: The type of data you want returned. Current data it can retrun: `Yaw`, `Pitch`, `Skew`, `Area`, `X-Dist`, `Y-Dist`, `Z-Dist`.
        """
        
        result = self.targets
        if len(result) == 0: # returns 0 if no apriltags are seen
            return 0
        else:
            for target in self.targets:
                if target.getFiducialId() == id: # looks for desired AprilTag ID
                    self.targetVisible = True
                    # Return the desired type of data
                    if dataType == "Yaw":
                        Data = target.getYaw()
                    elif dataType == "Pitch":
                        Data = target.getPitch()
                    elif dataType == "Skew":
                        Data = target.getSkew()
                    elif dataType == "Area":
                        Data = target.getArea()
                    elif dataType == "X-Dist":
                        Data = target.getBestCameraToTarget().X()
                    elif dataType == "Y-Dist":
                        Data = target.getBestCameraToTarget().Y()
                    elif dataType == "Z-Dist":
                        Data = target.getBestCameraToTarget().Z()
                else:
                    # return 0
                    continue
        return Data
        
    def printData(self): # Using this to test getting target Data
        
        # logger.info(f" Target ID: {self.getClosestData("ID")}")
        # logger.info(f" Target Yaw: {self.getClosestData("Yaw")}")
        # logger.info(f" Target Skew: {self.getClosestData("Skew")}")
        # logger.info(f" Target Pitch: {self.getClosestData("Pitch")}")
        # logger.info(f" Target X: {self.getClosestData("X-Dist")}")
        # logger.info(f" Target Y: {self.getClosestData("Y-Dist")}")
        # logger.info(f" Target Z: {self.getClosestData("Z-Dist")}")
        # logger.info(f"Target Amount: {len(self.targets)}")
        
        wpilib.SmartDashboard.putNumber("X-Dist", self.getClosestData("X-Dist"))
        wpilib.SmartDashboard.putNumber("Y-Dist", self.getClosestData("Y-Dist"))
        wpilib.SmartDashboard.putNumber("Z-Dist", self.getClosestData("Z-Dist"))
        wpilib.SmartDashboard.putNumber("Yaw", self.getClosestData("Yaw"))
        wpilib.SmartDashboard.putNumber("Skew", self.getClosestData("Skew"))
        wpilib.SmartDashboard.putNumber("Pitch", self.getClosestData("Pitch"))
        wpilib.SmartDashboard.putNumber("X-Rot", self.getClosestData("X-Rot"))
        wpilib.SmartDashboard.putNumber("Y-Rot", self.getClosestData("Y-Rot"))
        wpilib.SmartDashboard.putNumber("Z-Rot", self.getClosestData("Z-Rot"))