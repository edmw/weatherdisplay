# coding: utf-8

# 7. Binary Data Services
import struct
# 13. Data Compression and Archiving
import gzip
# 16. Generic Operating System Services
import os


# 3rd Party Libraries
import numpy


class Writer:

    def __init__(self, path):
        self.path = path

    def write_png(self, image, name):
        filename = "{}.png".format(name)
        filepath = os.path.join(self.path, filename)
        image.save(filepath, 'PNG')

    def __write_raw(self, data, name, zipped):
        filename = "{}.image{}".format(name, ".gz" if zipped else "")
        filepath = os.path.join(self.path, filename)
        o = gzip.open if zipped else open
        with o(filepath, 'wb') as f:
            f.write(data)

    def write_raw(self, image, name, zipped=False):
        rgb = numpy.array(image, dtype="uint16")
        rgb565 = (
            ((rgb[:, :, 0] & 0b11111000) << 8) |
            ((rgb[:, :, 1] & 0b11111100) << 3) |
            ((rgb[:, :, 2] & 0b11111111) >> 3)
        )
        self.__write_raw(rgb565, name, zipped)

    def write_raw_py(self, image, name, zipped=False):
        rgb565 = bytes()
        for p in image.getdata():
            r = (p[0] >> 3) & 0x1F
            g = (p[1] >> 2) & 0x3F
            b = (p[2] >> 3) & 0x1F
            rgb565 = rgb565 + struct.pack('H', (r << 11) + (g << 5) + b)
        self.__write_raw(rgb565, name, zipped)

    def write(self, image, file_name="weather", file_format='PNG'):
        if image:
            file_format = file_format.upper()
            if file_format == 'PNG':
                self.write_png(image, file_name)
            elif file_format == 'RAW565':
                self.write_raw(image.rotate(90, expand=True), file_name, zipped=False)
            elif file_format == 'RAW565Z':
                self.write_raw(image.rotate(90, expand=True), file_name, zipped=True)
            else:
                raise ValueError("Invalid file format '{}'".format(file_format))
        return self

    def write_timestamp(self, timestamp, file_name="weather"):
        if timestamp:
            filename = "{}.ts".format(file_name)
            filepath = os.path.join(self.path, filename)
            with open(filepath, 'w') as f:
                f.write("{:.0f}".format(timestamp))
        return self
