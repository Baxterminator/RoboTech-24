import signal

from proxies import RobotProxy, LectorProxy, InspectorProxy
from common import State
from common.configs import CalibrationData
from common.utils import LoggingInterface
from ._lector import lector_action
from ._robot import robot_action
from ._generate import gen_action
from ._calib import calib_action


STOP = False


def stop_console(sig, _):
    global STOP
    STOP = True


def run_console(robot: RobotProxy, lector: LectorProxy, calib_data: CalibrationData):
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
            case "gen":
                gen_action(state, cmd[1:])
            case "calib":
                calib_action(robot, state, cmd[1:])
            case _:
                LoggingInterface.sinfo(
                    "Unkown command %s:".format(cmd[0])
                    + ", choices are {robot, lector, close, calib}"
                )
