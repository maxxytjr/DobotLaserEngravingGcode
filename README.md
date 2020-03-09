# DobotLaserEngravingGcode
Laser Engraving with the Dobot Magician using Gcodes


# Background
The Dobot Magician comes with an in-built capability to laser-engrave uploaded images (JPG, PNG) with its 0.5W laser. 

All the user has to do is to start the Dobot Studio software, enter the 'Laser Engraving' Interface, upload the image file, and press 'Start' to begin the laser process.

The speed of the process mostly depends on the type of image uploaded; images with more detail will take more time, vice versa. Hence, the user does not have much control over the speed by this stage. 

It is the Dobot Studio Software's intention to maximize the quality of the result, with speed as its secondary concern. 

# Solution

If the user is willing to sacrifice quality over speed, the laser engraving process can be done via the usage of Gcodes and APIs, with the code in this repo.

# Setup Procedure
  * Download [Inkscape Portable](https://portableapps.com/apps/graphics_pictures/inkscape_portable)
  * Follow the instructions [here](https://github.com/martymcguire/inkscape-unicorn) to download the Gcode extension
  * Start the Inkscape software
  * Open the image on the canvas
  * Click on the image to make sure it is selected
  * Press 'OK' on the next window that pops up
  * On the canvas, drag out the original image and you shall see the traced bitmap image.
  * Delete the original image
  * Save as Gcode file
  * Upload gcode file into same directory as the main python file
  
# Running the Script

The script can be run from a shell terminal, and passing in the required argument values. 

The arguments are as follows:
  * `port`: COM port linked to the Dobot Magician
  * `width`: width (along robot y-axis) of the image in mm. Default value of 70.
  * `height`: height (along robot x-axis) of the image in mm. Default value of 50.
  * `startx`: robot x-coordinate of starting position. Default value of 250.
  * `starty`: robot y-coordinate of starting position. Default value of 0.
  * `gcode`: path to gcode file. Default value of 'gcode.gcode'.
  
Running in the terminal:

`python laser.py --port COM4 --width 100 --height 100 --startx 200 --starty 0 --gcode gcode.gcode`
