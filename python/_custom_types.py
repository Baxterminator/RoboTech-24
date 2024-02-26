from dataclasses import dataclass
from scipy.spatial.transform.rotation import Rotation
import math


def deg2rad(x: float) -> float:
    return math.pi * x / 180


def rad2deg(x: float) -> float:
    return 180 * x / math.pi


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
            True,
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
            False,
        )


@dataclass
class Pose:
    x: float
    y: float
    z: float
    rot: Rotation

    def __init__(self, _x: float, _y: float, _z: float, _r: Rotation = None):
        self.x = _x
        self.y = _y
        self.z = _z
        if _r is not None:
            self.rot = _r
        else:
            self.rot = Rotation.from_euler(
                "ZYX",
                (math.pi, 0, math.atan2(-self.x, self.y) - math.pi / 2),
                degrees=False,
            )


@dataclass
class Vec3:
    x: float
    y: float
    z: float


@dataclass
class Vec2:
    x: float
    y: float
