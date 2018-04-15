#!/bin/sh
insmod /drivers/ntx508/wifi/sdio_wifi_pwr.ko
insmod /drivers/ntx508/wifi/dhd.ko
sleep 2
ifconfig eth0 up
sleep 5
wlarm_le -i eth0 up
sleep 5
wpa_supplicant -s -i eth0 -Dwext -c /etc/wpa_supplicant/wpa_supplicant.conf -C /var/run/wpa_supplicant -B sleep 2
sleep 10
udhcpc -S -i eth0 -s /etc/udhcpc.d/default.script -t15 -T10 -A3 -f -q
sleep 2
