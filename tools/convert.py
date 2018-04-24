#!/usr/bin/python
# coding: utf-8

import locale
import gzip

# 3rd Party Libraries
import numpy
from PIL import Image


def convert(name):
    image = Image.open("{}.png".format(name)).rotate(90, expand=True)
    rgb = numpy.array(image, dtype="uint16")
    rgb565 = (
        ((rgb[:, :, 0] & 0b11111000) << 8) |
        ((rgb[:, :, 1] & 0b11111100) << 3) |
        ((rgb[:, :, 2] & 0b11111111) >> 3)
    )
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
