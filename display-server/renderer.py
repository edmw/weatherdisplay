# coding: utf-8

# 8. Data Types
import collections
from datetime import datetime
# 16. Generic Operating System Services
import os
import logging
# 29. Python Runtime Services
import sys


# 3rd Party Libraries
from PIL import Image, ImageFont, ImageDraw


class Box(collections.namedtuple('Box', 'x0 y0 x1 y1')):
    __slots__ = ()

    def width(self):
        return self.x1 - self.x0

    def height(self):
        return self.y1 - self.y0

    def center_x(self):
        return self.x0 + self.width() / 2

    def center_y(self):
        return self.y0 + self.height() / 2

    def inset(self, dx=0, dy=0, dx0=None, dy0=None, dx1=None, dy1=None):
        return Box(
            self.x0 + (dx0 if dx0 else dx),
            self.y0 + (dy0 if dy0 else dy),
            self.x1 - (dx1 if dx1 else dx),
            self.y1 - (dy1 if dy1 else dy)
        )

    def with_top(self, top):
        return Box(self.x0, top, self.x1, self.y1)

    def with_bottom(self, bottom):
        return Box(self.x0, self.y0, self.x1, bottom)

    def with_left(self, left):
        return Box(left, self.y0, self.x1, self.y1)

    def with_right(self, right):
        return Box(self.x0, self.y0, right, self.y1)

    def with_width(self, width):
        return Box(self.x0, self.y0, self.x0 + width, self.y1)

    def with_height(self, height):
        return Box(self.x0, self.y0, self.x1, self.y0 + height)


class Renderer:
    WIDTH = 600
    HEIGHT = 800
    PADDING = 20
    SUPERSAMPLING = 4

    BLACK = (0, 0, 0)
    GRAY = (104, 104, 104)
    WHITE = (255, 255, 255)
    RED = (204, 0, 0)

    def __init__(self):
        self.debug = logging.getLogger().getEffectiveLevel() == logging.DEBUG

        self.width = self.WIDTH * self.SUPERSAMPLING
        self.height = self.HEIGHT * self.SUPERSAMPLING
        self.padding = self.PADDING * self.SUPERSAMPLING

        self.image = Image.new('RGB', (self.width, self.height), self.WHITE)

        self.draw = ImageDraw.Draw(self.image)

        self.font = self.__get_font("Dosis-Bold", 200)
        self.font_date = self.__get_font("Dosis-Bold", 200)
        self.font_temperature = self.__get_font("Dosis-SemiBold", 420)
        self.font_humidity = self.__get_font("Dosis-Medium", 280)
        self.font_pressure = self.__get_font("Dosis-SemiBold", 280)

    def __get_font(self, name, size):
        return ImageFont.truetype(
            os.path.join(sys.path[0], "fonts", "{}.otf".format(name)),
            size
        )

    def line(self, xy, fill=None):
        self.draw.line(xy, fill=fill if fill else self.BLACK, width=8)

    def rectangle(self, xy, fill=None):
        self.draw.rectangle(xy, fill=fill if fill else self.BLACK)

    def ellipse(self, xy, fill=None):
        self.draw.ellipse(xy, fill=fill if fill else self.BLACK)

    def text(self, box, text, align='tl', fill=None, font=None):
        align = align.lower()

        if font is None:
            font = self.font
        a = font.getsize("$")[1]

        w, h = self.draw.textsize(text, font)

        if 'l' in align:
            x = box.x0
        elif 'r' in align:
            x = box.x1 - w
        else:  # 'c'
            x = (box.x1 - box.x0) / 2 - w / 2 + box.x0
        if 't' in align:
            y = box.y0 - a / 4
        elif 'b' in align:
            y = box.y1 - a
        else:  # 'm'
            y = (box.y1 - box.y0) / 2 - a / 2 + box.y0

        self.draw.text(
            (x, y),
            text,
            font=font,
            fill=fill if fill else self.BLACK
        )

        return y + h

    def draw_temperature_visual(self, box, value, min_value, max_value):
        if self.debug:
            self.draw.rectangle(box, outline=self.RED)

        if value is None:
            value = min_value
        value = (max(min(value, max_value), min_value) - min_value)
        value = value / (max_value - min_value)

        w = box.width()
        h = box.height()
        s = w * 0.08
        box_bulb = box.inset(dy0=h/3*2)
        box_tube = box.inset(dx0=w/4, dx1=w/4, dy1=h/6)
        box_tube_top = box_tube.with_height(box_tube.width())
        box_tube_middle = box_tube.with_top(box_tube_top.center_y())
        self.ellipse(box_bulb)
        self.ellipse(box_tube_top)
        self.rectangle(box_tube_middle)
        self.ellipse(box_bulb.inset(dx=s, dy=s), fill=self.WHITE)
        self.ellipse(box_tube_top.inset(dx=s, dy=s), fill=self.WHITE)
        self.rectangle(box_tube_middle.inset(dx=s), fill=self.WHITE)
        self.ellipse(box_bulb.inset(dx=s*2, dy=s*2), fill=self.BLACK)
        box_value = box_tube \
            .with_top(box_tube_top.center_y()) \
            .with_bottom(box_tube.y1 - h / 3 * 1 / 4) \
            .inset(dx=s*2)
        self.rectangle(box_value.inset(dy0=box_value.height() * (1 - value)))

        return box

    def draw_temperature(self, box, value):
        if self.debug:
            self.draw.rectangle(box, outline=self.RED)

        if value is None:
            text = "---°"
        else:
            text = "{:.1f}°".format(value)
        return self.text(box, text, align='lt', font=self.font_temperature)

    def draw_humidity(self, box, value):
        if self.debug:
            self.draw.rectangle(box, outline=self.RED)

        if value is None:
            text = "--- %"
        else:
            text = "{:.0f} %".format(value)
        return self.text(box, text, align='lb', font=self.font_humidity)

    def draw_pressure(self, box, value):
        if self.debug:
            self.draw.rectangle(box, outline=self.RED)

        if value is None:
            text = "--- hPa"
        else:
            text = "{:.2f} hPa".format(value/100)
        return self.text(box, text, align='ct', font=self.font_pressure)

    def draw_headline(self, box, text):
        if self.debug:
            self.draw.rectangle(box, outline=self.RED)

        return self.text(box, "{}".format(text), align='ct', fill=self.GRAY)

    def draw_datetime(self, box, dt):
        if self.debug:
            self.draw.rectangle(box, outline=self.RED)

        text = '{dt.day}. {dt:%B}   {dt.hour}:{dt:%M} Uhr'.format(dt=dt)
        return self.text(box, text, align='cb', fill=self.GRAY)

    def render(self, data):
        row = self.height / 5

        # outside
        y = self.draw_headline(
            Box(
                1.0 * self.padding,
                0.5 * self.padding,
                self.width - 1.0 * self.padding,
                row + 0.5 * self.padding
            ),
            "Außenklima"
        )
        # temperature & humidity
        b = self.draw_temperature_visual(
            Box(
                2.0 * self.padding,
                2.0 * self.padding + y,
                2.0 * self.padding + row / 3,
                2.0 * self.padding + y + row
            ),
            data.outdoor_temperature.value, -15, 45
        )
        y = self.draw_temperature(
            b.inset(dx0=b.width()+1.0*self.padding).with_right(self.width/2),
            data.outdoor_temperature.value
        )
        y = self.draw_humidity(
            b.inset(dx0=b.width()+2.0*self.padding).with_right(self.width/2),
            data.outdoor_humidity.value
        )
        # inside
        y = self.draw_headline(
            Box(
                1.0 * self.padding,
                y + 2.0 * self.padding,
                self.width - 1.0 * self.padding,
                row + y + 1.0 * self.padding
            ),
            "Innenklima"
        )
        # temperature & humidity
        b = self.draw_temperature_visual(
            Box(
                2.0 * self.padding,
                2.0 * self.padding + y,
                2.0 * self.padding + row / 3,
                2.0 * self.padding + y + row
            ),
            data.indoor_temperature.value, -15, 45
        )
        y = self.draw_temperature(
            b.inset(dx0=b.width()+1.0*self.padding).with_right(self.width/2),
            data.indoor_temperature.value
        )
        y = self.draw_humidity(
            b.inset(dx0=b.width()+2.0*self.padding).with_right(self.width/2),
            data.indoor_humidity.value
        )
        # air pressure
        b = Box(
            1.0 * self.padding,
            y + 2.0 * self.padding,
            self.width - 1.0 * self.padding,
            row + y + 1.0 * self.padding
        )
        y = self.draw_headline(b, "Luftdruck")
        y = self.draw_pressure(
            b.with_top(y).inset(dy0=2.0*self.padding).with_height(row),
            data.outdoor_pressure.value
        )
        # datetime
        b = Box(
            1.0 * self.padding,
            y + 1.0 * self.padding,
            self.width - 1.0 * self.padding,
            self.height - self.padding
        )
        y = self.draw_datetime(b, datetime.now())

        return self.image.resize(
            (self.WIDTH, self.HEIGHT),
            resample=Image.LANCZOS
        )
