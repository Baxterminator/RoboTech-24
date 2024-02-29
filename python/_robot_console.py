from _robot_proxy import RobotProxy
import signal
from typing import List
from _state import State
from _calibration import CalibrationData


STOP = False


def move_to(state: State, prox: RobotProxy, args: List[str]):
    match args[0]:
        case "input":
            state.input_idx = int(args[1])
            prox.movej(state.get_input_grabbing_approach_pos())
        case "good":
            state.read_idx = int(args[1])
            prox.movej(state.get_good_dropping_approach_pos())
        case "defect":
            state.defect_idx = int(args[1])
            prox.movej(state.get_defect_dropping_approach_pos)


def stop_console(sig, _):
    global STOP
    STOP = True


def robot_console(proxy: RobotProxy, calib_file: str):
    global STOP
    proxy.wait_client()
    state = State(CalibrationData(calib_file))

    signal.signal(signal.SIGTERM, stop_console)
    while not STOP:
        cmd = input("[ ][Console] > ").strip()
        if cmd.startswith("close"):
            proxy.close_connection()
        elif cmd.startswith("move"):
            move_to(state, proxy, cmd.split(" ")[1:])
        else:
            # Send command
            result = proxy.send(cmd)

        if not result:
            STOP = True
            break
        else:
            proxy._info(f"Response: {result}")
    proxy.close_socket()
