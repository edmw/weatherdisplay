# coding: utf-8

import sys
import os

from datetime import datetime

from PIL import Image, ImageFont, ImageDraw

def width(xy):
    return xy[1][0] - xy[0][0]

def height(xy):
    return xy[1][1] - xy[0][1]

def x1(xy):
    return xy[0][0]
def y1(xy):
    return xy[0][1]
def x2(xy):
    return xy[1][0]
def y2(xy):
    return xy[1][1]

def mod(xy, w=None, h=None, y1=None, y2=None):
    if w: xy = [(xy[0][0], xy[0][1]), (xy[0][0] + w, xy[1][1])]
    if h: xy = [(xy[0][0], xy[0][1]), (xy[1][0], xy[0][1] + h)]
    if y1: xy = [(xy[0][0], y1), (xy[1][0], xy[1][1])]
    if y2: xy = [(xy[0][0], xy[0][1]), (xy[1][0], y2)]
    return xy

def inset(xy, dx=0, dy=0, dx1=None, dy1=None, dx2=None, dy2=None):
    if not dx1: dx1 = dx
    if not dy1: dy1 = dy
    if not dx2: dx2 = dx
    if not dy2: dy2 = dy
    return [(x1(xy)+dx1, y1(xy)+dy1), (x2(xy)-dx2, y2(xy)-dy2)]

def scale(xy, s=1, sx=None, sy=None):
    if not sx: sx = s
    if not sy: sy = s
    dx = width(xy)*(1-sx)/2
    dy = height(xy)*(1-sy)/2
    scaled = inset(xy, dx1=dx, dy1=dy, dx2=dx, dy2=dy)
    return scaled


class Renderer:

    WIDTH=600
    HEIGHT=800
    PADDING=10
    SUPERSAMPLING=4

    BLACK=(0,0,0)
    GRAY=(104,104,104)
    WHITE=(255,255,255)

    def __init__(self):
        self.width = self.WIDTH * self.SUPERSAMPLING
        self.height = self.HEIGHT * self.SUPERSAMPLING
        self.padding = self.PADDING * self.SUPERSAMPLING

        self.image = Image.new('RGB', (self.width, self.height), self.WHITE)

        self.draw = ImageDraw.Draw(self.image)

        self.font = self.__get_font("Dosis-Bold", 240)
        self.font_temperature = self.__get_font("Dosis-Bold", 320)
        self.font_humidity = self.__get_font("Dosis-Bold", 200)

    def __get_font(self, name, size):
        return ImageFont.truetype(
            os.path.join(sys.path[0], "fonts", "{}.otf".format(name)),
            size
        )

    def draw_temperature_visual(self, xy, value, min_value, max_value):
        if value is None:
            value = min_value
        value = (max(min(value, max_value), min_value) - min_value) / (max_value - min_value)
        w = width(xy)
        h = height(xy)
        sw = w*0.08
        xy_bulb = inset(xy, dy1=h/3*2)
        xy_tube = inset(xy, dx1=w/4, dx2=w/4, dy2=h/3*1/2)
        xy_tube_top = mod(xy_tube, h=width(xy_tube))
        # draw bulb (back)
        self.draw.ellipse(xy_bulb, fill=self.BLACK)
        # draw tube (back)
        self.draw.ellipse(xy_tube_top, fill=self.BLACK)
        self.draw.rectangle(mod(xy_tube, y1=y1(xy_tube)+width(xy_tube)/2), fill=self.BLACK)
        # draw bulb
        self.draw.ellipse(inset(xy_bulb, dx=sw, dy=sw), fill=self.WHITE)
        # draw tube
        self.draw.ellipse(inset(xy_tube_top, dx=sw, dy=sw), fill=self.WHITE)
        self.draw.rectangle(inset(mod(xy_tube, y1=y1(xy_tube)+width(xy_tube)/4), dx=sw, dy=sw), fill=self.WHITE)
        # draw bulb (front)
        self.draw.ellipse(inset(xy_bulb, dx=sw*2, dy=sw*2), fill=self.BLACK)
        # draw tube (front)
        xy_tube_inner = inset(mod(xy_tube, y1=y1(xy_tube)+width(xy_tube)/2, y2=y2(xy_tube)-h/3*1/4), dx=sw*2)
        tube_inner_height = height(xy_tube_inner)
        tube_inner_value = tube_inner_height*value
        self.draw.rectangle(mod(xy_tube_inner, y1=y2(xy_tube_inner)-tube_inner_value), fill=self.BLACK)

    def draw_temperature(self, xy, value):
        if value is None:
            text = "----°"
        else:
            text = "{:.1f}°".format(value)
        w, h = self.draw.textsize(text, self.font_temperature)
        self.draw.text((x1(xy), y1(xy)), text, font=self.font_temperature, fill=self.BLACK)
        return y1(xy)+h

    def draw_humidity(self, xy, value):
        if value is None:
            text = "--- %"
        else:
            text = "{:.0f} %".format(value)
        w, h = self.draw.textsize(text, self.font_humidity)
        self.draw.text((x1(xy), y1(xy)), text, font=self.font_humidity, fill=self.BLACK)
        return y1(xy)+h

    def draw_headline(self, xy, text):
        text = "{}".format(text)
        w, h = self.draw.textsize(text, self.font)
        self.draw.text(((x2(xy)-x1(xy))/2-w/2, y1(xy)), text, font=self.font, fill=self.GRAY)
        return y1(xy)+h

    def draw_datetime(self, xy, dt):
        text = '{dt:%A}, {dt.day}. {dt:%B}\n{dt.hour}:{dt:%M} Uhr'.format(dt=dt)
        w, h = self.draw.textsize(text, self.font, spacing=50)
        self.draw.text(((x2(xy)-x1(xy))/2-w/2, y1(xy)), text, spacing=50, align="center", font=self.font, fill=self.GRAY)
        return y1(xy)+h

    def render(self, data):
        row = self.height / 5
        # outside
        x1 = 1*self.padding
        x2 = self.width-2*self.padding
        y1 = 1*self.padding
        y2 = 0
        y = self.draw_headline([(x1,y1), (x2,y2)], "Außenklima")
        # temperature
        x1 = 2*self.padding
        x2 = self.width/2-4*self.padding
        y1 = y+4*self.padding
        y2 = y1+row
        w1 = (y2-y1)/3
        self.draw_temperature_visual([(x1,y1),(x1+w1,y2)], data.outdoor_temperature, -15, 45)
        y = self.draw_temperature([(x1+w1+self.padding,y1),(x2,y2)], data.outdoor_temperature)
        x1 = x1+1*self.padding
        y1 = y+1*self.padding
        y = self.draw_humidity([(x1+w1+self.padding,y1),(x2,y2)], data.outdoor_humidity)
        # inside
        x1 = 1*self.padding
        x2 = self.width-2*self.padding
        y1 = y2+5*self.padding
        y2 = y1+row
        y = self.draw_headline([(x1,y1), (x2,y2)], "Innenklima")
        # temperature
        x1 = 2*self.padding
        x2 = self.width/2-4*self.padding
        y1 = y+4*self.padding
        y2 = y1+row
        w1 = (y2-y1)/3
        self.draw_temperature_visual([(x1,y1),(x1+w1,y2)], data.indoor_temperature, -15, 45)
        y = self.draw_temperature([(x1+w1+self.padding,y1),(x2,y2)], data.indoor_temperature)
        x1 = x1+1*self.padding
        y1 = y+1*self.padding
        y = self.draw_humidity([(x1+w1+self.padding,y1),(x2,y2)], data.indoor_humidity)
        # datetime
        x1 = 1*self.padding
        x2 = self.width-2*self.padding
        y1 = y2+5*self.padding
        y2 = y1+row
        y = self.draw_datetime([(x1,y1), (x2,y2)], datetime.now())

        return self.image.resize((self.WIDTH, self.HEIGHT), resample=Image.LANCZOS)
