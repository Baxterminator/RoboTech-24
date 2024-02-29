from dataclasses import dataclass
from scipy.spatial.transform.rotation import Rotation
import math

EULER_CONV = "xyz"


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

    def __repr__(self) -> str:
        u = "°" if self.in_deg else " rad"
        s = "JointState:\n"
        s += f'\t\t\t{f"Base: {self.base}{u}".ljust(20)}'
        s += f'{f"Shoulder: {self.shoulder}{u}".ljust(20)}'
        s += f'{f"Elbow: {self.elbow}{u}".ljust(20)}\n'
        s += f'\t\t\t{f"Wrist 1: {self.wrist1}{u}".ljust(20)}'
        s += f'{f"Wrist 2: {self.wrist2}{u}".ljust(20)}'
        s += f'{f"Wrist 3: {self.wrist3}{u}".ljust(20)}'
        return s


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
                EULER_CONV,
                (math.pi, 0, math.atan2(-self.x, self.y) - 3 * math.pi / 4),
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
