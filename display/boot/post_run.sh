#/bin/sh
WD=/mnt/onboard/.weatherdisplay

if [ -e /tmp/bootselect ]; then
    SELECTED=$(cat /tmp/bootselect)

    if [ "$SELECTED" == "wd" ] || [ "$SELECTED" == "wd_dev" ]; then
        sleep 2

        killall on-animator.sh nickel sickel fickel hindenburg 2>/dev/null

        $WD/tools/led.sh OFF

        $WD/busybox_custom crond -l 15 -c $WD/cron/

        zcat $WD/screens/download.image.gz | /usr/local/Kobo/pickel showpic

        sh $WD/update.sh >& $WD/update.out
    fi
fi
