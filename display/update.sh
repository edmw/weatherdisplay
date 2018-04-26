#!/bin/sh
WD=/mnt/onboard/.weatherdisplay

running=`ps aux | grep -i "update.sh" | grep -v "grep" | wc -l`
if [ $running -ge 1 ]; then
    # script already running
    exit 0
fi

#zcat $WD/screens/download.image.gz | /usr/local/Kobo/pickel showpic

$WD/tools/wifi_up.sh

# try to get the timestamp of the generation of the weather image ...
timestamp=$(wget -q http://192.168.178.111/weather.ts -O -)
if [[ $? -ne 0 ]]; then
    # could not get timestamp; use current time effectively ignoring a timeout
    timestamp=$(date +%s)
fi
timestamp_isnumeric=$(expr match "$timestamp" '[0-9][0-9]*$')
if ! [[ $timestamp_isnumeric ]]; then
    # not a valid timestamp; use current time effectively ignoring a timeout
    timestamp=$(date +%s)
fi

# calculate the timedelta between the generation of the weather image and current time
timedelta=$(($(date +%s) - $timestamp))

if [ "$timedelta" -lt "108000" ]; then
    # weather image is less than 30 minutes old
    # try to get weather image ...
    wget -q http://192.168.178.111/weather.image.gz -O - >/tmp/weather.image.gz
    if [[ $? -eq 0 ]] && [ -e /tmp/weather.image.gz ]; then
        # got weather image
        # calculate checksum for weather image
        hash=$(sha1sum /tmp/weather.image.gz  | awk '{print $1}')
        if ! [[ -e update.hash ]] || [ "X${hash}X" != "X$(cat update.hash)X" ]; then
            echo "${hash}" > update.hash
            zcat /tmp/weather.image.gz | /usr/local/Kobo/pickel showpic
        fi
    else
        # could not get weather image
        zcat $WD/screens/error-download.image.gz | /usr/local/Kobo/pickel showpic
    fi
else
    # weather image is too old
    zcat $WD/screens/error-time.image.gz | /usr/local/Kobo/pickel showpic
fi

$WD/tools/wifi_down.sh

# suspend for 10 minutes which will also pause minute-by-minute cron job
$WD/busybox_custom rtcwake -a -m mem -s 600
