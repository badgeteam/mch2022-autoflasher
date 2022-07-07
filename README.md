MCH2022 badge autoflasher package
=================================
This is intended for use during the sweatshop and at camp.

## How to use
1. `sudo apt-get install libusb-1.0-0` (or something alike)
2. Clone this repository
3. Copy [build files](https://github.com/badgeteam/mch2022-image-compile), including `flashargs`, to the `esp32` folder
3. Run `./prepare` (needs sudo to install udev rules)
4. Run `./flash`
5. Flash badges
6. When done, `./remove_udev_rules`
