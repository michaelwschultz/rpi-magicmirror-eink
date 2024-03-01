#!/usr/bin/python

##
 #  @filename   :   main.cpp
 #  @brief      :   7.5inch e-paper display demo
 #  @author     :   Yehui from Waveshare
 #
 #  Copyright (C) Waveshare     July 28 2017
 #
 # Permission is hereby granted, free of charge, to any person obtaining a copy
 # of this software and associated documnetation files (the "Software"), to deal
 # in the Software without restriction, including without limitation the rights
 # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 # copies of the Software, and to permit persons to  whom the Software is
 # furished to do so, subject to the following conditions:
 #
 # The above copyright notice and this permission notice shall be included in
 # all copies or substantial portions of the Software.
 #
 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 # FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 # LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 # THE SOFTWARE.
 ##

import logging
from waveshare_epd import epd7in5b_V2

from PIL import Image, ImageDraw, ImageOps
#import imagedata

logging.basicConfig(level=logging.DEBUG)

EPD_WIDTH = 800
EPD_HEIGHT = 480

try:
    epd = epd7in5b_V2.EPD()
    epd.init()

    # display image
    screenshot = Image.open('screenshot.png')

    # Create a new image with RGBA mode to strip out the red channel
    red_image = Image.new("RGBA", screenshot.size)
    pixels = screenshot.load()
    new_pixels = red_image.load()

   # loop through every pixel to determine the red pixels and remove the ones that aren't
    for i in range(screenshot.size[0]):
      for j in range(screenshot.size[1]):
        r, g, b, a = pixels[i, j]
        # Check if red is the dominant color
        if r > g and r > b:
            # Keep the red pixel as is, make it fully opaque in the new image
            new_pixels[i, j] = (0, 0, 0, 255)
        else:
            # Make non-red pixels transparent or set to a background color
            # For transparency, set the alpha to 0
            new_pixels[i, j] = (255, 255, 255, 0)  # This makes non-red areas white "transparent"

    frame_black = epd.getbuffer(screenshot)
    frame_red = epd.getbuffer(red_image)

   # send frames to display
    epd.display(frame_black, frame_red)

except KeyboardInterrupt:
	logging.info("ctrl + c:")
	epd.init()
	epd.Clear()
	exit()
