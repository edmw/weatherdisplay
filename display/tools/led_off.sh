#!/bin/sh
echo "ch 4" > /sys/devices/platform/pmic_light.1/lit
echo "cur 0" > /sys/devices/platform/pmic_light.1/lit
echo "dc 0" > /sys/devices/platform/pmic_light.1/lit
echo 0 > /sys/class/leds/pmic_ledsg/brightness
