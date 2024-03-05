from time import sleep
import signal

from python.proxies import RobotProxy, LectorProxy, InspectorProxy
from python.common.configs._calibration import CalibrationData
from python.common.utils._custom_logger import LoggingInterface
from common._state import Step, State


class CartridgeSequencer(LoggingInterface):

    def __init__(
        self,
        robot: RobotProxy,
        lector: LectorProxy,
        calib_data: CalibrationData,
        step: bool = False,
    ):
        super().__init__("Sequencer")
        self._robot = robot
        self._lector = lector
        self.step = step
        self.state = State(calib_data)
        self.STOP = False

        self.done_cell: list = []
        signal.signal(signal.SIGTERM, self.stop_sequence)

    def _step_pos(self) -> None:
        if self.step:
            input("Step ...\r")

    def stop_sequence(self, sig_n, frame) -> None:
        self._error(f"Got signal {signal.strsignal(sig_n)}")
        self.STOP = True

    def run(self):
        self.state.step = Step.IDLE
        self.STOP = False
        while self.state.step != Step.DONE and not self.STOP:
            # If no client, wait for a new one
            if not self._robot.has_client():
                self._robot.wait_client()

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
        self._info("Beginning sequence!")
        self._robot.close_gripper()
        self.state.step = Step.MV_INPUT

    def go_input(self):
        """
        Let's go to input
        """
        self._info("Going to input bin")
        self._robot.close_gripper()
        self._robot.open_gripper()
        self._robot.close_gripper()
        self._robot.open_gripper()
        self._robot.send_comment("Moving to input bin")
        self._robot.movej(self.state.get_safe_input_pos())
        self._step_pos()
        self._robot.movel(self.state.get_input_grabbing_approach_pos())
        self._step_pos()
        self._robot.movel(self.state.get_input_grabbing_pos())
        self._robot.wait_steady()
        self._step_pos()

        self._robot.send_comment("Grabbing cartridge")
        self._robot.close_gripper()
        sleep(self.state.calib.grabbing_time)

        self._robot.send_comment("Returning to approach position")
        self._robot.movel(self.state.get_input_grabbing_approach_pos())
        self._step_pos()
        self._robot.movej(self.state.get_safe_input_pos())
        self._step_pos()
        self.state.step = Step.CHECK_QR

    def check_qr(self):
        """
        Checking the QR codegood
        """
        self._info("Checking for QR code")
        self._robot.send_comment("Moving to QR checking")
        self._robot.movej(self.state.get_checking_approach_pos())
        self._robot.movej(self.state.get_qr_checking_pos())
        self._robot.wait_steady()
        self._step_pos()

        # Check QR-code
        batch, num = self._lector.read_qr_code()
        if num not in self.done_cell:
            print(batch, num)
            self.done_cell.append(num)
            if batch != 100 or num < 26 or num > 50:
                self._info("QR-Code anomaly detected, moving it to the defect bin!")
                self.state.step = Step.MV_BAD_BIN
            else:
                self.state.read_idx = num
                self._info("No anomalies for the QR-Code, continuing checking")
                self.state.step = Step.CHECK_ANOMALIES
        else:
            self._info("QR-Code anomaly detected, moving it to the defect bin!")
            self.state.step = Step.MV_BAD_BIN

        self._robot.movej(self.state.get_checking_approach_pos())

    def check_anomaly(self):
        """
        Checking for anomalies
        """
        self._info("Checking for anomalies")
        self._robot.send_comment("Moving to Anomalies checking")
        self._robot.movej(self.state.get_defect_checking_pos())
        self._robot.wait_steady()
        self._robot.movej(self.state.get_defect_checking_pos2())
        self._robot.wait_steady()
        self._step_pos()
        # TODO: Check defects
        defect = False
        if defect:
            self._info("Cartridge anomaly detected, moving it to the defect bin.")
            self.state.step = Step.MV_BAD_BIN
        else:
            self._info("No cartridge anomaly detected, moving it to the good  bin.")
            self.state.step = Step.MV_GOOD_BIN

        self._robot.movej(self.state.get_checking_approach_pos())
        self._step_pos()

    def go_good_bin(self):
        """
        Go to the good bin
        """
        self._info("Dropping inside good bin")

        self._robot.send_comment("Moving to good bin position")
        self._robot.movej(self.state.get_safe_good_pos())
        self._step_pos()
        self._robot.movej(self.state.get_good_dropping_approach_pos())
        self._step_pos()
        self._robot.movel(self.state.get_good_dropping_pos())
        self._robot.wait_steady()
        self._step_pos()

        self._robot.send_comment("Dropping catridge")
        self._robot.open_gripper()
        sleep(self.state.calib.grabbing_time)

        self._robot.send_comment("Returning to approach position")
        self._robot.movel(self.state.get_good_dropping_approach_pos())
        self._step_pos()
        self._robot.movej(self.state.get_safe_good_pos())
        self._step_pos()
        self.state.step = Step.END_CARTRIDGE

    def go_bad_bin(self):
        """
        Go to the bad bin
        """
        self._info("Dropping inside defect bin")
        self._robot.send_comment("Going to the defective bin ...")
        self._robot.movej(self.state.get_safe_good_pos())
        self._step_pos()
        self._robot.movej(self.state.get_safe_defect_pos())
        self._step_pos()

        self._robot.send_comment("Moving to defective bin approach position")
        self._robot.movej(self.state.get_defect_dropping_approach_pos())
        self._step_pos()
        self._robot.movel(self.state.get_defect_dropping_pos())
        self._robot.wait_steady()
        self._step_pos()

        self._robot.send_comment("Dropping catridge")
        self._robot.open_gripper()
        sleep(self.state.calib.grabbing_time)

        self._robot.send_comment("Returning to approach position")
        self._robot.movej(self.state.get_defect_dropping_approach_pos())
        self._step_pos()

        self._robot.send_comment("Going to the input bin ...")
        self._robot.movej(self.state.get_safe_defect_pos())
        self._step_pos()
        self._robot.movej(self.state.get_safe_good_pos())
        self._step_pos()

        self.state.step = Step.END_CARTRIDGE
        self.state.defect_idx += 1

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
