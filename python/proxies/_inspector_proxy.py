from enum import Enum
from time import sleep
from ._mqtt_proxy import MQTTProxy


class InspectorJob(Enum):
    BUBBLE = 0
    PISTON = 1
    SCRATCHES = 2


class InspectorProxy(MQTTProxy):

    class Messages:
        TRIGGER_ON = "4"
        TRIGGER_OFF = "8"

        JOB_BUBBLE = "5"
        JOB_SCRATCHES = "6"
        JOB_PISTON = "7"

    def __init__(self, broker_ip: str, topic: str) -> None:
        super().__init__(broker_ip, topic)

    # =========================================================================
    # Inspector specialized functions
    # =========================================================================
    def _trigger_on(self):
        """
        Launch a call for a a trigger on for the Lector
        """
        self._send_msg(InspectorProxy.Messages.TRIGGER_ON)

    def _trigger_off(self):
        """
        Launch a call for a a trigger off for the Lector
        """
        self._send_msg(InspectorProxy.Messages.TRIGGER_OFF)

    def _job_bubble(self):
        """
        Set the job to Bubble
        """
        self._send_msg(InspectorProxy.Messages.JOB_BUBBLE)

    def _job_piston(self):
        """
        Set the job piston
        """
        self._send_msg(InspectorProxy.Messages.JOB_PISTON)

    def _job_scratches(self):
        """
        Set the job to scratches
        """
        self._send_msg(InspectorProxy.Messages.JOB_SCRATCHES)

    def run_job(self, job: InspectorJob) -> bool:
        try:
            self._reset()
            sleep(0.3)
            match job:
                case InspectorJob.BUBBLE:
                    self._job_bubble()
                case InspectorJob.PISTON:
                    self._job_piston()
                case InspectorJob.SCRATCHES:
                    self._job_scratches()
            sleep(0.3)
            self._reset()
            sleep(0.3)
            self._trigger_on()
            sleep(0.3)
            self._reset()
            sleep(0.3)
            self._trigger_off()
            sleep(0.3)
            self._publish()
            result: str = self._receive_msg().decode()
            self._reset()
        except:
            return False

        if len(result) < 5:
            return False

        return bool(result[5])
