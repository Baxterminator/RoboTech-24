from ..proxies._lector_proxy import LectorProxy
from ..common.utils._custom_logger import LoggingInterface


def lector_action(lector: LectorProxy, args: dict[str]):
    match args[0]:
        case "reset":
            lector._reset()
        case "trigon":
            lector._trigger_on()
        case "trigoff":
            lector._trigger_off()
        case "pub":
            lector._publish()
        case "read":
            LoggingInterface.sinfo("Got %s".format(lector._receive_msg()))
        case "getqr":
            LoggingInterface.sinfo("Got %s".format(lector.read_qr_code()))
        case _:
            LoggingInterface.sinfo(
                "Unkown command %s:".format(args[0])
                + ", choices are {reset, trigon, trigoff, pub, read, getqr"
            )
