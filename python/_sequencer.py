from _robot_proxy import RobotProxy


class CartridgeSequencer:

    PREFIX = "CardtridgeSeq"

    def __init__(self, proxy: RobotProxy):
        pass

    def run(self):
        print(f"{CartridgeSequencer.PREFIX} Running sequence !")
