#/bin/sh
WD=/mnt/onboard/.weatherdisplay

#zcat $WD/screens/download.image.gz | /usr/local/Kobo/pickel showpic

$WD/tools/wifi_up.sh

wget -q http://192.168.178.111/weather.image.gz -O - >/tmp/weather.image.gz
if [[ $? -eq 0 ]] && [ -e /tmp/weather.image.gz ]; then
    zcat /tmp/weather.image.gz | /usr/local/Kobo/pickel showpic
else
    zcat $WD/screens/error-download.image.gz | /usr/local/Kobo/pickel showpic
fi

$WD/tools/wifi_down.sh

# suspend for 10 minutes which will also pause minute-by-minute cron job
$WD/busybox_custom rtcwake -a -m mem -s 600
