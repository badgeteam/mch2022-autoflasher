MCH2022 badge autoflasher package
=================================
This is intended for use during the sweatshop and at camp.

## How to use
1. `sudo apt-get install libusb-1.0-0` (or something alike)
2. Clone this repository
3. `pip install pyserial`
4. ~~Copy [build files](https://github.com/badgeteam/mch2022-image-compile),
   including `flashargs`, to the `esp32` folder~~
5. Run `./prepare` (needs sudo to install udev rules)
6. Run `./flash`
7. Flash badges
8. When done, `./remove_udev_rules`

## How it works
When the udev rules are installed, connecting a badge with the RP2040 in boot
select mode[1] will trigger the first rule which runs `picotool` with the bus
and device number as arguments. This flashes the RP2040 after which it will
reboot.

Running `./flash` starts `esp32/badge_multiflash_daemon.py`, which continuously
looks for newly connected serial devices. When one is connected, it checks the
minor node number on the `tty` device to distinguish between the different
serial interfaces on the badge. If the minor node number is 0, that means it is
the serial bus to the ESP32 and it will use `esptool.py` to flash the ESP32.
After flashing, it waits for the device to disconnect before going back to
checking for a connected device.

<hr/>
1: Blank badges will be in boot select mode when they are powered on. To get a
badge which already has firmware into boot select mode, power it up while
pressing SELECT.
