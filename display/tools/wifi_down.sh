#!/bin/sh
killall udhcpc wpa_supplicant 2>/dev/null
wlarm_le -i eth0 down
ifconfig eth0 down
sleep 5
rmmod dhd
rmmod sdio_wifi_pwr
sync
sleep 2
