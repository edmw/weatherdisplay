# coding: utf-8

from PIL import Image

import struct

import gzip

class Writer:

    def __init__(self, path):
        self.path = path

    def write_png(self, image, name):
        image.save("{}.png".format(name), 'PNG')

    def write_raw(self, image, name, zipped=False):
        rgb565 = bytes()
        for p in image.getdata():
            r = (p[0] >> 3) & 0x1F
            g = (p[1] >> 2) & 0x3F
            b = (p[2] >> 3) & 0x1F
            rgb565 = rgb565 + struct.pack('H', (r << 11) + (g << 5) + b)
        if zipped:
            with gzip.open("{}.image.gz".format(name), 'wb') as f:
                f.write(rgb565)
        else:
            with open("{}.image".format(name), 'wb') as f:
                f.write(rgb565)

    def write(self, image, name="weather", zipped=False):
        image = image.rotate(90, expand=True)

        self.write_png(image, name)
        self.write_raw(image, name, zipped=zipped)
