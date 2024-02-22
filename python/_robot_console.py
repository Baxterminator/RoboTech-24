from _robot_proxy import RobotProxy
import signal


STOP = False


def stop_console(sig, _):
    global STOP
    STOP = True


def robot_console(proxy: RobotProxy):
    global STOP
    proxy.wait_client()

    signal.signal(signal.SIGTERM, stop_console)
    while not STOP:
        cmd = input("[ ][Console] > ").strip()
        if cmd.startswith("close"):
            proxy.close_connection()

        # Send command
        result = proxy.send(cmd)

        if not result:
            STOP = True
            break
        else:
            proxy.info(f"Response: {result}")
    proxy.close_socket()
