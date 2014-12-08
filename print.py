# https://code.google.com/p/python-escpos/wiki/Usage

# lsub
# http://stackoverflow.com/questions/17058134/is-there-an-equivalent-of-lsusb-for-os-x
# Bus 020 Device 001: ID 0519:0001 Star Micronics Co., LTD Composite Device
#
# 2. You'll need libusb for mac
# Hard to find
# http://www.ellert.se/twain-sane/
#
# 3. Then install http://walac.github.io/pyusb/
#
# 4. Then sudo pip install python-escpos

#       Host Controller Location: Built-in USB
#       Host Controller Driver: AppleUSBXHCI
#       PCI Device ID: 0x1e31
#       PCI Revision ID: 0x0004
#       PCI Vendor ID: 0x8086
#       Bus Number: 0x0a
#
#         Composite Device:
#
#           Product ID: 0x0001
#           Vendor ID: 0x0519  (Star Micronics Co., LTD)
#           Version:  2.01
#           Speed: Up to 12 Mb/sec
#           Location ID: 0x14300000 / 1
#           Current Available (mA): 500
#           Current Required (mA): 10
#           1284 Device ID: MFG:Star;CMD:STAR;MDL:TSP600 (STR_T-U001);CLS:PRINTER;

from datetime import datetime
from escpos import *
import urllib2
import json

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'

Generic = printer.Usb(0x519,0x0001)
Generic.set(size='2x', bold=True, font='b', underline=1)
Generic.text("Hello World\n")

response = urllib2.urlopen('https://fax-machine.herokuapp.com/messages')
data = json.load(response)
print data

for message in data:
    date = datetime.strptime(message[u'date'], DATETIME_FORMAT)
    print "Hi"
    Generic.set(size='2x', bold=True, font='b', underline=1)
    Generic.text(message[u'sender'] + "\n")
    Generic.text(message[date] + "\n")

    Generic.set(bold=False)
    Generic.text(message[u'body'] + "\n")
