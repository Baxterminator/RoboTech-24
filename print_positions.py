import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.transform.rotation import Rotation

world_origin = (0, 0, 0)


def draw_axis(ax, position, rotation, label):
    x_arrow = np.array(rotation[0, :])
    y_arrow = np.array(rotation[1, :])
    z_arrow = np.array(rotation[2, :])
    ax.quiver(*position, *x_arrow, color="red", arrow_length_ratio=0.1)
    ax.quiver(*position, *y_arrow, color="green", arrow_length_ratio=0.1)
    ax.quiver(*position, *z_arrow, color="blue", arrow_length_ratio=0.1)
    ax.text(*(position + x_arrow), f"{label}_x")
    ax.text(*(position + y_arrow), f"{label}_y")
    ax.text(*(position + z_arrow), f"{label}_z")


positions = [
    (0, 0, 0, 0, 0, 0),
]

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection="3d")
draw_axis(ax, world_origin, np.eye(3), "W", color="blue")

i = 0
for p in positions:
    # Rot matrix
    rmat = Rotation.from_euler("xyz", (p[3], p[4], p[5]), degres=True).as_matrix()
    draw_axis(ax, p, rmat, f"P{0}")
