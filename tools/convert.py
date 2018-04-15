#!/usr/bin/python
# coding: utf-8

import sys
import os
import locale
import argparse
import logging
import collections
import gzip

import struct

from datetime import datetime

from influxdb import InfluxDBClient

from PIL import Image, ImageFont, ImageDraw

def convert(name):
    image = Image.open("{}.png".format(name)).rotate(90, expand=True)
    rgb565 = bytes()
    for p in image.getdata():
        r = (p[0] >> 3) & 0x1F
        g = (p[1] >> 2) & 0x3F
        b = (p[2] >> 3) & 0x1F
        rgb565 = rgb565 + struct.pack('H', (r << 11) + (g << 5) + b)
    #with open("{}.image".format(name), 'wb') as f:
    #    f.write(rgb565)
    with gzip.open("{}.image.gz".format(name), 'wb') as f:
        f.write(rgb565)

def main():
    convert("display/screens/clear")
    convert("display/screens/init")
    convert("display/screens/init-wait")
    convert("display/screens/download")
    convert("display/screens/error-download")
    convert("display/screens/error-time")
    convert("display/screens/developer")

if __name__ == "__main__":
    locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
    main()
