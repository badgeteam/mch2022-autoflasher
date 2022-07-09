#!/usr/bin/env python3

# Derived from batchflash.py by Tom Clement

import sys, threading, time
import os
from os.path import exists

# import serial

running = True

os.chdir(os.path.dirname(os.path.realpath(__file__)))
with open('flashargs') as f: flashargs = f.read().replace('\n', ' ')

def find_device(number):
    # Because each badge with complete RP2040 exposes two devices,
    # Multiply thread number by two to get port number.
    number *= 2
    devices = ['/dev/ttyUSB%d' % number,
               '/dev/ttyACM%d' % number,
               '/dev/tty.usbserial-14%d0' % number,
               '/dev/tty.usbserial-144%d0' % number,
               '/dev/tty.usbmodem123456%d' % number,
               '/dev/tty.usbmodem%d' % number,
               '/dev/tty.usbmodem1%d' % number,
               '/dev/tty.usbmodem2%d' % number,
               '/dev/tty.usbmodem3%d' % number,
               '/dev/tty.usbmodem4%d' % number,
               '/dev/tty.usbmodem5%d' % number,
               '/dev/tty.usbmodem6%d' % number,
               '/dev/tty.usbmodem7%d' % number,
               '/dev/tty.usbmodem8%d' % number,
               '/dev/tty.usbmodem9%d' % number,
               '/dev/tty.usbmodem123456%d' % number]
    for device in devices:
        # Filtering by minor node number == 0 gives the first USB endpoint/interface on a device.
        # On the MCH2022 badge, the first interface is the serial bus to the ESP32.
        if exists(device) and os.minor(os.stat(device).st_rdev) % 2 == 0:
            return device
    return None

def flash_daemon(number):
    global running, flashargs
    print('Starting flash thread for %s' % number)
    sys.stdout.flush()
    while running:
        try:
            device = find_device(number)
            if device is not None:
                print('Flashing %s' % device)
                sys.stdout.flush()
                flash = [
                    f'esptool/esptool.py --chip ESP32 --port {device} --baud 1000000 --before=default_reset --after=hard_reset write_flash {flashargs}'
                ]
                cmd = ' && '.join(flash)
                print(cmd)
                res = os.system(cmd)
                if res == 2:
                    running = False
                    break
                elif res != 0:
                    print('Failed to flash device')
                    time.sleep(1)
                    continue

                # conn = serial.Serial(device, baudrate=115200)

                # print('Waiting for console to come up')
                # conn.timeout = 0.5
                # conn.write(b'\r\n'*5)
                # line = b''
                # while b'>>> ' not in line:
                #     line = conn.readline()
                #     print('Got:', line.decode('ascii'))
                #     conn.write(b'\r\n')
                print('Done')


                # Give system time to adjust
                time.sleep(1)

                # Wait for device to detach
                while exists(device):
                    time.sleep(0.1)
        except KeyboardInterrupt:
            running = False
        except BaseException:
            pass

        time.sleep(0.1)


input("Press enter to start flashing any connected ESP32")
threads = [threading.Thread(target=flash_daemon, args=(i,)) for i in range(16)]
[t.start() for t in threads]
[t.join() for t in threads]
