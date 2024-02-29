from ._mqtt_proxy import MQTTProxy
from enum import Enum


class LectorProxy(MQTTProxy):

    class Messages(Enum):
        # Lector
        LECTOR_TRIG_ON = "1"
        LECTOR_TRIG_OFF = "2"
        LECTOR_PUBLISH = "3"

    def __init__(self, broker_ip: str, topic: str) -> None:
        super().__init__(broker_ip, topic)

    # =========================================================================
    # Lector specialized functions
    # =========================================================================
    def _trigger_on(self):
        """
        Launch a call for a a trigger on for the Lector
        """
        self._send_msg(LectorProxy.Messages.LECTOR_TRIG_ON)

    def _trigger_off(self):
        """
        Launch a call for a a trigger off for the Lector
        """
        self._send_msg(LectorProxy.Messages.LECTOR_TRIG_OFF)

    def _publish(self):
        """
        Ask for data publishing
        """
        self._send_msg(LectorProxy.Messages.LECTOR_PUBLISH)

    def read_qr_code(self) -> str:
        self._reset()
        self._trigger_on()
        self._reset()
        self._trigger_off()
        self._publish()
        qr = self._receive_msg()
        self._reset()
        return qr
