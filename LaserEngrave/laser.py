import argparse
from LaserEngrave.get_coord_from_gcode import GetCoordFromGcode
from LaserEngrave.dobot_control import DobotControl


def get_coord_list(gcode_file):
    get_coord_object = GetCoordFromGcode()
    combined_list = get_coord_object.get_coords(gcode_file)

    return combined_list


ap = argparse.ArgumentParser()
ap.add_argument('-p', '--port', default="COM4", help="COM port linked to Dobot")
ap.add_argument('-w', '--width', default=70, help="width (robot y) of image in mm")
ap.add_argument('-ht', '--height', default=50, help="height (robot x) of image in mm")
ap.add_argument('-x', '--startx', default=250, help="robot x coordinate of start position")
ap.add_argument('-y', '--starty', default=0, help="robot y coordinate of start position")
ap.add_argument('-g', '--gcode', default='gcode.gcode', help="path to gcode file")

args = vars(ap.parse_args())

# obtain the xy coordinates and laser action from gcode file
command_list = get_coord_list(args['gcode'])

# initialize DobotControl object
dobot_control = DobotControl(args['width'],
                             args['height'],
                             args['startx'],
                             args['starty'])

# connect to dobot
dobot_control.connect(args['port'])

# start move sequence
dobot_control.move_sequence(command_list)

# disconnect dobot
dobot_control.disconnect()


