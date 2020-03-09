from tkinter import *
from tkinter import filedialog
import os


class GetCoordFromGcode:
    def __init__(self):
        self.filename = None

        self.x_list = []
        self.y_list = []
        self.op_list = []
        self.laser_list = []

        self.command_list = []

    def get_coords(self, file=None):
        if file == None:
            file = open(self.filename, 'r')
        else:
            file = open(file, 'r')

        gcode = file.readlines()


        # for each line in the gcode file, determine if it is an 'operation', 'coord' or 'pen_action' type
        # operation type: G1, G2, G3, etc
        # coord type: line that starts with 'X' after a 'G1' operation
        # pen_action: 'M300 S35' refers to the 'pen down' action. 'M300 S30' refers to the 'pen up' action

        for line in gcode:
            operation = re.findall(r'[G]\d', line)
            coords = re.findall(r'[XY].?\d+.\d+', line)
            pen_action = re.findall(r'[MS].?\d+.\d+', line)

            if (len(coords) == 0 or len(operation) == 0):
                if len(pen_action) > 1:
                    if pen_action[1][1:3] == '35':
                        self.command_list.append("ON")
                    elif pen_action[1][1:3] == '30':
                        self.command_list.append("OFF")
                    self.op_list.append(0)
                    self.x_list.append(0)
                    self.y_list.append(0)
                    continue

                continue

            if operation[0] == "G1" and coords[0][0] == "X":
                self.op_list.append(operation[0])
                self.x_list.append(coords[0][1:])
                self.y_list.append(coords[1][1:])
                self.command_list.append(0)

        g_list = [str(i) for i in self.op_list]
        x_list = [float(i) for i in self.x_list]
        y_list = [float(i) for i in self.y_list]
        c_list = [str(i) for i in self.command_list]

        # format of combined_list = [direction (mostly G1), x, y, laser_flag (on or off)]

        combined_list = zip(g_list, x_list, y_list, c_list)
        combined_list = list(combined_list)

        return combined_list

if __name__ == "__main__":
    get_coord = GetCoordFromGcode()
    filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                           title="Select Gcode file",
                                           filetypes=[("Gcode Files", "*.gco *.gcode")])
    get_coord.get_coords(file=filename)

