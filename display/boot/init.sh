#/bin/sh
WD=/mnt/onboard/.weatherdisplay

# show boot image and wait five seconds
zcat $WD/screens/init.image.gz | /usr/local/Kobo/pickel showpic
sleep 5

# show boot image and select what to boot depending on the position of a touch
zcat $WD/screens/init-wait.image.gz | /usr/local/Kobo/pickel showpic
# wait-for-hit
# FB_MODE="$(fbset | grep '^mode' | cut -d \" -f 2)"
# FB_MODE="${FB_MODE%-*}"
# FB_W="${FB_MODE%x*}"
# FB_H="${FB_MODE#*x}"
# +-------------+
# |        (0,0)|
# |             |
# |   (100,200) |
# |             |
# | (500,600)   |
# |             |
# |(FB_W,FB_H)  |
# +-------------+
HIT=$(/usr/local/Kobo/pickel wait-for-hit 0 0 0 0 0 0 0 0)
HIT=$(echo $HIT | awk -F'[()]' '{print $8}')
HIT_X="${HIT#*, }"
HIT_Y="${HIT%, *}"
echo "X: $HIT_X Y: $HIT_Y"
if [ "$HIT_X" -gt "100" ] && [ "$HIT_X" -lt "500" ] && [ "$HIT_Y" -gt "200" ] && [ "$HIT_Y" -lt "600" ]; then
    echo "wd" > /tmp/bootselect
elif [ "$HIT_X" -gt "500" ] && [ "$HIT_Y" -gt "700" ]; then
    echo "wd_dev" > /tmp/bootselect
else
    echo "default" > /tmp/bootselect
fi
sync

# clear display
zcat $WD/screens/clear.image.gz | /usr/local/Kobo/pickel showpic 1
