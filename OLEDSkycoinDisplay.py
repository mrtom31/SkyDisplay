#!/usr/bin/env python3
"""
Display on OLED SSD1306 each nodes IP and their connection status
"""
import time
from PIL import Image
from PIL import ImageFont
from SkyAPI import SkyAPI
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from luma.core.virtual import viewport
import operator
import os

#Save pid for crontab to kil process
file = open("pid.txt", "w")
file.write(str(os.getpid()))
file.close()

dirname = os.path.dirname(__file__)
img_path = os.path.join(dirname, 'images/skycoin.png')

serial = i2c(port=1, address=0x3c)
device = ssd1306(serial, rotate=0)

sizeChar = 12   #Size font 
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", sizeChar)

# Load and display Skycoin logo
logo = Image.open(img_path).convert(device.mode)
w, h = logo.size
virtual = viewport(device, width=device.width, height=h)

y = 0
while y < (h-device.height):
    virtual.set_position((0, y))
    virtual.display(logo)
    y += 4

maskStatus = {0 : 'FAIL', 1 : 'GOOD'}
secret_path = os.path.join(dirname, 'secret.txt')
api = SkyAPI(secret=open(secret_path, 'r').readline().rstrip())
api.update()
nbNodes = len(api.nodesInfo)
virtual = viewport(device, width=device.width, height=(nbNodes + 1) * sizeChar)
while True:
    api.update()
    info= ""
    # Loop sorted following IP address value {'kty value': {IP value ; Bool }}
    for node in sorted(api.nodesInfo.items(), key=lambda kv : kv[1][0]):
        # convert to "IP  GOOD/FAIL"
        info += str(node[1][0].split(':')[0]) + " " + str(maskStatus[node[1][1]]) + "\n"
    with canvas(virtual) as draw:
        for i, line in enumerate(info.split("\n")):
            draw.text((0, i * sizeChar), text=line, font=font, fill="white")
    virtual.set_position((0, 0))
    time.sleep(2)
    y = 0
    while y < nbNodes * sizeChar - device.height:
        y += 2
        virtual.set_position((0, y))
        time.sleep(0.01)
    time.sleep(2)
    
