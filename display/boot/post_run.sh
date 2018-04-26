#/bin/sh
WD=/mnt/onboard/.weatherdisplay

if [ -e /tmp/bootselect ]; then
    SELECTED=$(cat /tmp/bootselect)

    if [ "$SELECTED" == "wd" ] || [ "$SELECTED" == "wd_dev" ]; then
        sleep 2

        killall on-animator.sh nickel sickel fickel hindenburg 2>/dev/null

        $WD/tools/led.sh OFF

        zcat $WD/screens/download.image.gz | /usr/local/Kobo/pickel showpic

        if [ "$SELECTED" == "wd" ]; then
            # start update cron
            $WD/busybox_custom crond -l 15 -c $WD/cron/

            # start update script
            sh $WD/update.sh >& $WD/update.out
        fi
        # do not start update cron and update script if in dev mode
    fi
fi
