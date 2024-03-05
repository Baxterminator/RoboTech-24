from typing import Tuple
from ._mqtt_proxy import MQTTProxy
from enum import Enum
from time import sleep


class LectorProxy(MQTTProxy):

    class Messages:
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
        result = ""
        try:
            self._reset()
            sleep(0.1)
            self._trigger_on()
            sleep(0.3)
            self._reset()
            sleep(0.3)
            self._trigger_off()
            sleep(0.1)
            self._publish()
            result: str = self._receive_msg().decode()
            print(result)
            self._reset()

            # Process the
            if len(result) < 5:
                return (0, 0)

            batch = int(result[:3])
            number = int(result[3:5])
            print(result[:3], result[3:5])
            print(batch, number)
            return (batch, number)

        except:
            return (0, 0)
