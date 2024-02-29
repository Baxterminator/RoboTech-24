from typing import Tuple
from ._mqtt_proxy import MQTTProxy
from enum import Enum


class LectorProxy(MQTTProxy):

    class Messages(Enum):
        # Lector
        TRIG_ON = "1"
        TRIG_OFF = "2"

    def __init__(self, broker_ip: str, topic: str, timeout_s: float = 1) -> None:
        super().__init__(broker_ip, topic)

    # =========================================================================
    # Lector specialized functions
    # =========================================================================
    def _trigger_on(self):
        """
        Launch a call for a a trigger on for the Lector
        """
        self._send_msg(LectorProxy.Messages.TRIG_ON)

    def _trigger_off(self):
        """
        Launch a call for a a trigger off for the Lector
        """
        self._send_msg(LectorProxy.Messages.TRIG_OFF)

    def read_qr_code(self) -> Tuple[int, int]:
        """
        Return the QR code descripion as (batch, n°)
        """
        self._reset()
        self._trigger_on()
        self._reset()
        self._trigger_off()
        self._publish()
        result: bytes = self._receive_msg()
        self._reset()

        if result == b"\x00":
            return (0, 0)

        # Process the
        batch = int(result[:3].decode())
        number = int(result[3:].decode())

        return (batch, number)
