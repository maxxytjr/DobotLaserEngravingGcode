from dobot import DobotDllType as dType
import time

class DobotControl:

    def __init__(self, width, height, start_x, start_y):

        # initialize state
        self.state = None

        # scale factor
        self.scale_x = 1.0
        self.scale_y = 1.0

        # x-y coordinate of start position
        self.start_x = start_x
        self.start_y = start_y

        # load dll
        self.api = dType.load()

        self.CON_STR = {
            dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
            dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
            dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"
        }

        # dimensions of actual engraving area
        self.width = width
        self.height = height

    def connect(self, port):
        # Connect Dobot
        self.port = port
        self.state = dType.ConnectDobot(self.api, self.port, 115200)[0]
        print("Connect status:", self.CON_STR[self.state])

    def get_scale(self, command_list):
        """Takes the dimensions of the laser engraving area and obtains a scale factor"""
        min_x = min(list(zip(*command_list))[1])
        max_x = max(list(zip(*command_list))[1])
        min_y = min(list(zip(*command_list))[2])
        max_y = max(list(zip(*command_list))[2])

        width_scale = self.width / (max_x - min_x)
        height_scale = self.height / (max_y - min_y)

        self.scale_y = width_scale
        self.scale_x = height_scale

    def move_sequence(self, command_list):
        """command list contains 4-tuples in the form of (G.., x, y, on/off)"""
        self.command_list = command_list

        lastIndex = 0

        # calculate scaling
        self.get_scale(command_list)

        if self.state == dType.DobotConnect.DobotConnect_NoError:

            # Clean Command Queue
            dType.SetQueuedCmdClear(self.api)

            # Async Motion Params Setting
            dType.SetHOMEParams(self.api, 250, 0, 50, 0, isQueued=1)
            dType.SetPTPJointParams(self.api, 300, 300, 300, 300, 300, 300, 300, 300, isQueued=1)
            dType.SetPTPCommonParams(self.api, 100, 100, isQueued=1)

            # home the robot
            dType.SetHOMECmd(self.api, temp=0, isQueued=1)

            # start filling up command queue; first move robot to starting point
            lastIndex = dType.SetPTPCmd(self.api, dType.PTPMode.PTPMOVLXYZMode, self.start_x, self.start_y, 50, 0, isQueued=1)[0]

            # loop through list of gcode commands and create command queue
            for point in self.command_list:
                if point[3] == 'OFF':
                    lastIndex = dType.SetEndEffectorLaser(self.api, 1, 0, isQueued=1)[0]
                elif point[3] == 'ON':
                    lastIndex = dType.SetEndEffectorLaser(self.api, 1, 1, isQueued=1)[0]
                elif point[3] == '0':
                    x_offset = self.scale_x * point[2]
                    y_offset = self.scale_y * point[1]
                    # print(x_offset, y_offset)
                    # point coordinates from the start position
                    lastIndex = dType.SetPTPCmd(self.api,
                                                dType.PTPMode.PTPMOVLXYZMode,
                                                self.start_x + x_offset,
                                                self.start_y - y_offset,
                                                50,
                                                0,
                                                isQueued=1)[0]

            # end the command queue by turning off the laser and moving back to start position
            lastIndex = dType.SetEndEffectorLaser(self.api, 1, 0, isQueued=1)[0]
            lastIndex = dType.SetPTPCmd(self.api, dType.PTPMode.PTPMOVLXYZMode, self.start_x, self.start_y, 50, 0, isQueued=1)[0]


            # start the queue of commands
            dType.SetQueuedCmdStartExec(self.api)

            # Wait until last command (index) has been executed successfully
            while lastIndex > dType.GetQueuedCmdCurrentIndex(self.api)[0]:
                # must be 100 or more, if not steps will be skipped
                dType.dSleep(100)

            # Stop executing commands in command queue
            dType.SetQueuedCmdStopExec(self.api)

            # clean queued commands
            dType.SetQueuedCmdClear(self.api)
            time.sleep(1)

    def disconnect(self):
        # Disconnect Dobot
        dType.DisconnectDobot(self.api)


if __name__ == "__main__":
    dobot_control = DobotControl(70, 50)

    # connect
    dobot_control.connect('COM4')

    # dummy list of commands for debugging
    command_list = [
        ('0', 0.0, 0.0, 'ON'),
        ('G1', -205, 0, '0'),
        ('G1', 205, 0, '0'),
        ('0', 0.0, 0.0, 'OFF'),
        ('G1', -205, 0, '0'),
        ('G1', 205, 0, '0'),
        ('0', 0.0, 0.0, 'ON'),
        ('G1', 0, -113, '0'),
        ('G1', 0, 113, '0'),
        ('0', 0.0, 0.0, 'OFF'),
        ('G1', 0, -113, '0'),
        ('G1', 0, 113, '0')
    ]

    dobot_control.move_sequence(command_list)

    dobot_control.disconnect()