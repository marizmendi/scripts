#!/bin/bash
finch run -ti -v $(pwd):/example ghcr.io/zephyrproject-rtos/ci:latest bash -c "cd example && git config --global --add safe.directory '*' && west build --pristine -b nrf52840dongle_nrf52840 my-app/app"

nrfutil pkg generate --hw-version 52 --sd-req=0x00 --application build/zephyr/zephyr.hex --application-version 1 zephyr.zip

nrfutil dfu usb-serial -pkg zephyr.zip -p /dev/tty.usbmodemE741992908981
