from time import sleep
import signal

from _robot_proxy import RobotProxy
from _calibration import CalibrationData
from _custom_logger import LoggingInterface
from _state import Step, State


class CartridgeSequencer(LoggingInterface):

    def __init__(self, proxy: RobotProxy, calib_path: str):
        super().__init__("Sequencer")
        self._proxy = proxy
        self.state = State(CalibrationData.load_from_file(calib_path))
        self.STOP = False
        signal.signal(signal.SIGTERM, self.stop_sequence)

    def stop_sequence(self, sig_n, frame) -> None:
        self._error(f"Got signal {signal.strsignal(sig_n)}")
        self.STOP = True

    def run(self):
        self._info("Beginning sequence!")
        self._info(f"Loaded calibration data:\n{self.state.calib}")
        self._info("Test")

        self.state.step = Step.IDLE
        self.STOP = False
        while self.state.step != Step.DONE and not self.STOP:
            # If no client, wait for a new one
            if not self._proxy.has_client():
                self._proxy.wait_client()

            match self.state.step:
                case Step.IDLE:
                    self.idle()
                case Step.MV_INPUT:
                    self.go_input()
                case Step.CHECK_QR:
                    self.check_qr()
                case Step.CHECK_ANOMALIES:
                    self.check_anomaly()
                case Step.MV_GOOD_BIN:
                    self.go_good_bin()
                case Step.MV_BAD_BIN:
                    self.go_bad_bin()
                case Step.END_CARTRIDGE:
                    self.cartridge_done()

    def idle(self):
        """
        Robot is idle, should launch
        """
        self._info("Waiting for input to begin...")
        input()
        self.state.step = Step.MV_INPUT

    def go_input(self):
        """
        Let's go to input
        """
        self._info("Going to input bin")
        # self._proxy.open_gripper()
        self._proxy.movej(self.state.get_input_grabbing_approach_pos())
        self._proxy.movel(self.state.get_input_grabbing_pos())
        self._proxy.wait_steady()
        # self._proxy.close_gripper()
        sleep(0.05)
        self._proxy.movel(self.state.get_input_grabbing_approach_pos())
        self.state.step = Step.CHECK_QR

    def check_qr(self):
        """
        Checking the QR codegood
        """
        # self._info("Checking cartridge QR-Code")
        # self._proxy.movel(self.state.get_checking_approach_pos())
        # self._proxy.movej(self.state.get_qr_checking_pos())
        # self._proxy.wait_steady()
        # TODO: Check QR Code
        defect = True
        if defect:
            self._info("QR-Code anomaly detected, moving it to the defect bin!")
            self.state.step = Step.MV_BAD_BIN
        else:
            self._info("No anomalies for the QR-Code, continuing checking")
            self.state.step = Step.CHECK_ANOMALIES

    def check_anomaly(self):
        """
        Checking for anomalies
        """
        self._info("Checking for anomalies")
        # self._proxy.movej(self.state.get_defect_checking_pos())
        # self._proxy.wait_steady()
        # TODO: Check defects
        defect = False
        if defect:
            self._info("Cartridge anomaly detected, moving it to the defect bin.")
            self.state.step = Step.MV_BAD_BIN
        else:
            self._info("No cartridge anomaly detected, moving it to the good  bin.")
            self.state.step = Step.MV_GOOD_BIN

        # self._proxy.movel(self.state.get_checking_approach_pos())

    def go_good_bin(self):
        """
        Go to the good bin
        """
        self._info("Dropping inside good bin")
        self._proxy.movej(self.state.get_good_dropping_approach_pos())
        self._proxy.movel(self.state.get_good_dropping_pos())
        self._proxy.wait_steady()
        # self._proxy.open_gripper()
        sleep(0.05)
        self._proxy.movel(self.state.get_good_dropping_approach_pos())
        self.state.step = Step.END_CARTRIDGE

    def go_bad_bin(self):
        """
        Go to the bad bin
        """
        self._info("Dropping inside defect bin")
        self._proxy.movej(self.state.get_defect_middle_pos())
        self._proxy.movej(self.state.get_defect_dropping_approach_pos())
        self._proxy.movel(self.state.get_defect_dropping_pos())
        self._proxy.wait_steady()
        # self._proxy.open_gripper()
        sleep(0.05)
        self._proxy.movel(self.state.get_defect_dropping_approach_pos())
        self._proxy.movej(self.state.get_defect_middle_pos())
        self.state.step = Step.END_CARTRIDGE

    def cartridge_done(self):
        """
        The cartridge is done, now what ?
        """
        self.state.input_idx += 1

        # If over to number of input cells, stop
        if self.state.is_done():
            self._info("Sequence is over, closing everything.")
            self.state.step = Step.DONE
        else:
            self._info("Cartridge done, moving on to the next one.")
            self.state.step = Step.MV_INPUT
