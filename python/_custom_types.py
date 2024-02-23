from dataclasses import dataclass
import math

def deg2rad(x: float) -> float:
    return math.pi*x/180

def rad2deg(x: float) -> float:
    return 180*x/math.pi

@dataclass
class JointState:
    base: float
    shoulder: float
    elbow: float
    wrist1: float
    wrist2: float
    wrist3: float

    deg: bool = False

    def in_deg(self) -> "JointState":
        if self.deg:
            return self
        return JointState(
            rad2deg(self.base),
            rad2deg(self.shoulder),
            rad2deg(self.elbow),
            rad2deg(self.wrist1),
            rad2deg(self.wrist2),
            rad2deg(self.wrist3),
            True
        )
    
    def in_rad(self) -> "JointState":
        if not self.deg:
            return self
        return JointState(
            deg2rad(self.base),
            deg2rad(self.shoulder),
            deg2rad(self.elbow),
            deg2rad(self.wrist1),
            deg2rad(self.wrist2),
            deg2rad(self.wrist3),
            False
        )

@dataclass
class Pose:
    x: float
    y: float
    z: float
    rx: float
    ry: float
    rz: float

    deg: bool = False

    def in_deg(self) -> "Pose":
        if self.deg:
            return self
        return Pose(
            self.x,
            self.y,
            self.z,
            rad2deg(self.rx),
            rad2deg(self.ry),
            rad2deg(self.rz),
            True
        )
    
    def in_rad(self) -> "Pose":
        if not self.deg:
            return self
        return Pose(
            self.x,
            self.y,
            self.z,
            deg2rad(self.rx),
            deg2rad(self.ry),
            deg2rad(self.rz),
            False
        )