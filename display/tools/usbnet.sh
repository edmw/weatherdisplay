#!/bin/sh
/bin/busybox insmod /drivers/ntx508/usb/gadget/arcotg_udc.ko
/bin/busybox insmod /drivers/ntx508/usb/gadget/g_ether.ko
ifconfig usb0 172.16.0.2
