import math
from typing import Iterator
from _custom_types import Vec3, Vec2, Pose


def generate_grid_pos(
    origin: Vec3, drow: Vec2, dcol: Vec2, nrow: int, ncol: int, idx: int
) -> Pose:
    """
    Generate the right position in the nest corresponding to the given idx.
    Params:
        - origin: the position of cartridge number 0
        - drow: the displacement in meters between each row
        - dcol: the displacement in meters between each colum,
        - nrow: the number of row of the nest
        - ncol: the number of column of the next
        - idx: the index of the cartridge to grab / place
    """

    # Compute the (row, col) nest coordinates
    idx = idx % 25  # Mod 25 since that the number of cartridges per nest
    idx_col = idx // nrow  # Compute the column index
    idx_row = idx % nrow

    # Compute real world coordinates
    return Pose(
        origin.x
        + (idx_row if idx_col % 2 == 0 else idx_row + 0.5) * drow.x
        + idx_col * dcol.x,
        origin.y
        + (idx_row if idx_col % 2 == 0 else idx_row + 0.5) * drow.y
        + idx_col * dcol.y,
        origin.z,
    )


def gen_circle_path(fr: Pose, to: Pose, dtheta: float) -> Iterator[Pose]:
    """
    Generate a circle path between the two given points (circle center is a robot origin).
    """

    # Get the angles of both
    fr_thz = math.atan2(fr.y, fr.x)
    fr_r = math.sqrt(fr.x * fr.x + fr.y * fr.y)
    to_thz = math.atan2(to.y, to.x)
    to_r = math.sqrt(to.x * to.x + to.y * to.y)
    dth_step = dtheta if to_thz > fr_thz else -dtheta
    n = math.floor((to_thz - fr_thz) / dth_step)

    for i in range(1, n):

        # Interpolate new radius
        factor = float(i) / float(n)
        new_r = factor * to_r + (1 - factor) * fr_r

        yield Pose(
            new_r * math.cos(i * dth_step),
            new_r * math.sin(i * dth_step),
            factor * to.z + (1 - factor) * fr.z,
        )
