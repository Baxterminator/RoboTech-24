import socket
from _custom_types import JointState, Pose, rad2deg
from _custom_logger import LoggingInterface


class RobotProxy(LoggingInterface):
    """
    Class for communicating between the robot via TCP/IP socket
    """

    PREFIX = r"RobotProxy"

    DEGREES_BY_DEFAULT = True
    PARAM_SEP = ","
    LINE_END = ";"

    # Command patterns
    GET_JOINT_POS = "gjp"
    GET_TCP_POS = "gtp"
    MOVE_J = "mvj,{},{},{},{},{},{}"
    MOVE_J_RESP = "mvjok"
    MOVE_L = "mvl,{},{},{},{},{},{}"
    MOVE_L_RESP = "mvlok"
    OPEN_GRIPPER = "gop"
    CLOSE_GRIPPER = "gcl"
    WAIT_STEADY = "std"
    STOP = "stp"
    STOP_RESP = "stpok"

    def __init__(self, srv_ip: str, srv_port: int) -> None:
        super().__init__(RobotProxy.PREFIX)
        self.__binding_ip = (srv_ip, srv_port)
        self.__socket: socket.socket | None = None
        self.__client: socket.socket | None = None
        self.open_socket()

    # =========================================================================
    # General Purpose Functions
    # =========================================================================

    def open_socket(self) -> None:
        self.__socket = socket.socket()
        self.__socket.bind(self.__binding_ip)

    def wait_client(self) -> None:
        """
        Wait for a client to connect to the socket server.
        """
        if self.__client is not None:
            return

        if self.__socket is None:
            self.error("Wanted to connect when socket is closed!")
            return

        self.info("Waiting for client ...")
        self.__socket.listen()
        self.__client, add = self.__socket.accept()
        self.info(f"Client found with IP {add}")

    def send(self, msg: str) -> str | None:
        """
        Send a message to the client (if client connected).
        Return the response string, or None if there is a problem with the client.
        """
        if self.__client == None:
            self.warn("Trying to send message when client not connected!")
            return None

        if self.__socket is None:
            self.error("Trying to send a message when socket is closed!")
            return None

        # Send message
        self.debug(f"Sending cmd '{msg}'")
        self.__socket.sendall(f"{msg}{RobotProxy.LINE_END}".encode())

        # Wait for response
        while True:
            data = self.__client.recv(1024)
            if not data:
                break
            if len(data.decode()) > 1:
                return (
                    data.decode()
                    .split(RobotProxy.LINE_END)[0]
                    .replace(RobotProxy.LINE_END, "")
                )

        # In case of communication error
        self.warn("Robot disconnected!")
        return None

    def close_connection(self) -> None:
        """
        Close the connection with the current client.
        """
        if self.__client is None:
            return
        self.info("Closing client connection")
        result = self.send(RobotProxy.STOP)

        # Check if result is right:
        if result is not None and not result.startswith(RobotProxy.STOP_RESP):
            self.error(f"Robot server problem when stopping: {result}")

        self.__client = None

    def close_socket(self) -> None:
        """
        Close the socket server.
        """
        if self.__socket is None:
            return
        self.info("Closing socket")
        self.close_connection()
        self.__socket.close()
        self.__socket = None

    def __del__(self):
        self.close_socket()

    # =========================================================================
    # Robotech specialized functions
    # =========================================================================

    def get_joint_state(self, degrees: bool = DEGREES_BY_DEFAULT) -> JointState | None:
        """
        Fetch the actual joint state of the robot and return it as a JointState object.
        Return None in case of communication error.

        Sends:    gjp;
        Receive:  gjp,q1,q2,q3,q4,q5,q6;
        """
        result = self.send(RobotProxy.GET_JOINT_POS)

        # If com error
        if result is None:
            return None

        elems = result.split(RobotProxy.PARAM_SEP)
        if len(elems) <= 7 or elems[0] != RobotProxy.GET_JOINT_POS:
            self.error(f"Malformed result for GetJoinState : '{result}'")
            return None

        return JointState(
            rad2deg(float(elems[1])) if degrees else float(elems[1]),
            rad2deg(float(elems[2])) if degrees else float(elems[2]),
            rad2deg(float(elems[3])) if degrees else float(elems[3]),
            rad2deg(float(elems[4])) if degrees else float(elems[4]),
            rad2deg(float(elems[5])) if degrees else float(elems[5]),
            rad2deg(float(elems[6])) if degrees else float(elems[6]),
            False,
        )

    def get_tcp_pose(self, degrees: bool = DEGREES_BY_DEFAULT) -> Pose | None:
        """
        Fetch the actual joint state of the robot and return it as a JointState object.
        Return None in case of communication error.

        Sends:    gtp;
        Receive:  gtp,x,y,z,rx,ry,rz;
        """
        result = self.send(RobotProxy.GET_TCP_POS)

        # If com error
        if result is None:
            return None

        elems = result.split(RobotProxy.PARAM_SEP)
        if len(elems) <= 7 or elems[0] != RobotProxy.GET_TCP_POS:
            self.error(f"Malformed result for GetJoinState : '{result}'")
            return None

        return Pose(
            float(elems[1]),
            float(elems[2]),
            float(elems[3]),
            rad2deg(float(elems[4])) if degrees else float(elems[4]),
            rad2deg(float(elems[5])) if degrees else float(elems[5]),
            rad2deg(float(elems[6])) if degrees else float(elems[6]),
            False,
        )

    def movej(self, joints: JointState) -> bool:
        """
        Launch a straight move in joint space.
        Returns whether the command was executed successfully or not.

        Sends:    mvj,q1,q2,q3,q4,q5,q6;
        Receives: mvjok;
        """
        # Send the move command
        rad_joints = joints.in_rad()
        cmd = RobotProxy.MOVE_J.format(
            rad_joints.base,
            rad_joints.shoulder,
            rad_joints.elbow,
            rad_joints.wrist1,
            rad_joints.wrist2,
            rad_joints.wrist3,
        )
        result = self.send(cmd)

        # Check if client was connected
        if result == None:
            return False

        # Check if result is right:
        if not result.startswith(RobotProxy.MOVE_J_RESP):
            self.error(f"Robot server problem when MoveJ: {cmd} -> {result}")
            return False

        return True

    def movel(self, pose: Pose) -> bool:
        """
        Launch a straight move in world space.
        Returns whether the command was executed successfully or not.

        Sends:    mvl,x,y,z,rx,ry,rz;
        Receives: mvlok;
        """
        # Send the move command
        rad_pose = pose.in_rad()
        cmd = RobotProxy.MOVE_L.format(
            rad_pose.x,
            rad_pose.y,
            rad_pose.z,
            rad_pose.rx,
            rad_pose.ry,
            rad_pose.rz,
        )
        result = self.send(cmd)

        # Check if client was connected
        if result == None:
            return False

        # Check if result is right:
        if not result.startswith(RobotProxy.MOVE_L_RESP):
            self.error(f"Robot server problem when MoveL: {cmd} -> {result}")
            return False

        return True

    def open_gripper(self) -> bool:
        """
        Open the gripper.
        Returns whether the command was executed successfully or not.

        Sends:    gop;
        Receives: gop;
        """
        result = self.send(RobotProxy.OPEN_GRIPPER)

        # Check if client was connected
        if result == None:
            return False

        # Check if result is right:
        if not result.startswith(RobotProxy.OPEN_GRIPPER):
            self.error(f"Robot server problem when opening gripper: {result}")
            return False

        return True

    def close_gripper(self) -> bool:
        """
        Close the gripper.
        Returns whether the command was executed successfully or not.

        Sends:    gcl;
        Receives: gcl;
        """
        result = self.send(RobotProxy.CLOSE_GRIPPER)

        # Check if client was connected
        if result == None:
            return False

        # Check if result is right:
        if not result.startswith(RobotProxy.CLOSE_GRIPPER):
            self.error(f"Robot server problem when closing gripper: {result}")
            return False

        return True

    def wait_steady(self) -> bool:
        """
        Blocking method to wait until the robot is steady.
        Returns whether the command is successful (True = success, False = error)

        Sends:    std;
        Receives: std;
        """
        result = self.send(RobotProxy.WAIT_STEADY)

        # Check if client was connected
        if result == None:
            return False

        # Check if result is right:
        if not result.startswith(RobotProxy.WAIT_STEADY):
            self.error(f"Robot server problem when waiting for steadiness: {result}")
            return False

        return True
