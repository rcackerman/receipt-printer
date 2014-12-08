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

"""
:type bold:         bool
:param bold:        set bold font
:type underline:    [None, 1, 2]
:param underline:   underline text
:type size:         ['normal', '2w', '2h' or '2x']
:param size:        Text size
:type font:         ['a', 'b', 'c']
:param font:        Font type
:type align:        ['left', 'center', 'right']
:param align:       Text position
:type inverted:     boolean
:param inverted:    White on black text
:type color:        [1, 2]
:param color:       Text color
:rtype:             NoneType
:returns:            None
"""

import os
if os.environ['IS_MAC']:
    IS_MAC = True

from datetime import datetime
if not IS_MAC:
    from escpos import *

import urllib2
import json


if not IS_MAC:
    Generic = printer.Usb(0x519,0x0001)
    Generic.set(size='2x', bold=True, font='b', underline=None)
    Generic.text("Hello World\n")


def text(text):
    if IS_MAC:
        print text
        return

    Generic.set(bold=False)
    Generic.text(text + "\n\n")


def title(title):
    if IS_MAC:
        print "TITLE: " + title
        return

    Generic.set(size='2x', bold=True, font='b', inverted=True)
    Generic.text(title + "\n")

def oneline(line):
    if IS_MAC:
        print line
        return

    Generic.text(line + "\n")


def lf():
    if IS_MAC:
        return

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'


response = urllib2.urlopen('https://fax-machine.herokuapp.com/messages')
data = json.load(response)
print data

for message in data:
    title(message[u'sender'])
    date = datetime.strptime(message[u'date'][:19], DATETIME_FORMAT)
    oneline(datetime.strftime(date, '%H:%M'))
    text(message[u'body'])
