#!/bin/sh
WD=/mnt/onboard/.weatherdisplay

if [ -e /tmp/bootselect ]; then
    SELECTED=$(cat /tmp/bootselect)

    if [ "$SELECTED" == "wd" ] || [ "$SELECTED" == "wd_dev" ]; then
        sleep 2

        /sbin/hwclock -s -u

    fi
    if [ "$SELECTED" == "wd_dev" ]; then
        /sbin/syslogd

        $WD/tools/usbnet.sh

        zcat $WD/screens/developer.image.gz | /usr/local/Kobo/pickel showpic

        sleep 2
    fi
fi
