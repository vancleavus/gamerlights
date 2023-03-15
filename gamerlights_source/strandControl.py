#!/usr/bin/env python3
# rpi_ws281x library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from rpi_ws281x import *
import argparse
import json

# LED strip configuration:
LED_COUNT      = 148      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53



# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms):
    """Wipe color across display a pixel at a time."""
    for j in range(0, strip.numPixels()):
        for i in range(0, int(strip.numPixels()/2)-1):
            strip.setPixelColor(i, strip.getPixelColor(i+1))
            y = strip.numPixels()-i-1
            strip.setPixelColor(y, strip.getPixelColor(y-1))
        strip.setPixelColor(int(strip.numPixels()/2)-1,color)
        strip.setPixelColor(int(strip.numPixels()/2),color)
        strip.show()
        time.sleep(wait_ms/1000.0)

# def colorFill(strip, color):
#     for i in range(strip.numPixels()):
#         strip.setPixelColor(i, color)
#     strip.show()

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(255 - pos * 3, 0, pos * 3)
    elif pos < 170:
        pos -= 85
        return Color(0, pos * 3, 255 - pos * 3)
    else:
        pos -= 170
        return Color(pos * 3, 255 - pos * 3, 0)
        

def progressStripOne(strip, color, wait_ms):
    for i in range(0, int(strip.numPixels()/2)-1):
        strip.setPixelColor(i, strip.getPixelColor(i+1))
        y = strip.numPixels()-i-1
        strip.setPixelColor(y, strip.getPixelColor(y-1))
    strip.setPixelColor(int(strip.numPixels()/2)-1,color)
    strip.setPixelColor(int(strip.numPixels()/2),color)
    strip.show()
    time.sleep(wait_ms/1000.0)


# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:
        rainbowI = 0
        fadeI = 0
        fadeDirection = 1
        staticColor = ''
        fadeColor1 = ''
        fadeColor2 = ''
        mode = ''
        colorData = {}
        colorCurrent = Color(0,0,0)
        while True:
            with open('/usr/local/gamerlights/gamerlights_source/colors.json', 'r') as openJSONFile:
                colorData = json.load(openJSONFile)
            if len(colorData['data']) >=2:
                # got new data from webpage
                colorData['data'].pop(0)
                with open('/usr/local/gamerlights/gamerlights_source/colors.json', 'w') as openJSONFile:
                    json.dump(colorData, openJSONFile)
                staticColor = colorData['data'][0]['staticColor']
                fadeColor1 = colorData['data'][0]['fadeColor1']
                fadeColor2 = colorData['data'][0]['fadeColor2']
                mode = colorData['data'][0]['mode']
                if mode=="rainbow":
                    rainbowI = 0
                elif mode=="fade":
                    fadeI = 0
                    fadeDirection = 1   
            else:
                # no new data from webpage, continue on
                if mode=="off":
                    colorCurrent=Color(0,0,0)
                elif mode=="static":
                    colorCurrent=Color(int(staticColor[1:3],16),int(staticColor[3:5],16),int(staticColor[5:7],16))
                elif mode=="fade":
                    fadeI += fadeDirection
                    if fadeI==255:
                        fadeDirection = -1
                    elif fadeI==0:
                        fadeDirection = 1
                    colorRedCurrent=int(fadeI * ((int(fadeColor2[1:3],16)-int(fadeColor1[1:3],16))/255)) + int(fadeColor1[1:3],16)
                    colorGrnCurrent=int(fadeI * ((int(fadeColor2[3:5],16)-int(fadeColor1[3:5],16))/255)) + int(fadeColor1[3:5],16)
                    colorBluCurrent=int(fadeI * ((int(fadeColor2[5:7],16)-int(fadeColor1[5:7],16))/255)) + int(fadeColor1[5:7],16)
                    colorCurrent= Color(colorRedCurrent, colorGrnCurrent, colorBluCurrent)
                elif mode=="rainbow":
                    colorCurrent=wheel(rainbowI)
                    rainbowI += 1
                    if rainbowI>=256:
                        rainbowI=0
            progressStripOne(strip, colorCurrent, 20)


    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 10)
