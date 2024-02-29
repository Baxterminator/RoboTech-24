from python.proxies._robot_proxy import RobotProxy
from python.proxies._lector_proxy import LectorProxy
import signal
from common._state import State
from python.common.configs._calibration import CalibrationData
from ._lector import lector_action
from ._robot import robot_action
from ..common.utils._custom_logger import LoggingInterface


STOP = False


def stop_console(sig, _):
    global STOP
    STOP = True


def robot_console(robot: RobotProxy, lector: LectorProxy, calib_data: CalibrationData):
    global STOP
    robot.wait_client()
    state = State(calib_data)

    signal.signal(signal.SIGTERM, stop_console)
    while not STOP:
        cmd = input("[ ][Console] > ").strip().split(" ")
        match cmd[0]:
            case "close":
                robot.close_connection()
            case "robot":
                STOP = robot_action(robot, state, cmd[1:])
            case "lector":
                lector_action(lector, cmd[1:])
            case _:
                LoggingInterface.sinfo(
                    "Unkown command %s:".format(cmd[0])
                    + ", choices are {robot, lector, close}"
                )
