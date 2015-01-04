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
from datetime import datetime
import urllib2
import json


# We can't print on mac, so we have to fake it for testing.
IS_MAC = os.getenv('IS_MAC', False)
if not IS_MAC:
    from escpos import *

URL = 'https://fax-machine.herokuapp.com/messages'
DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'

if not IS_MAC:
    Generic = printer.Usb(0x519,0x0001)
    Generic.set(size='2x', bold=True, font='b', underline=None)
    Generic.text("Hello World\n")


# Print a block of text
def text(text):
    if IS_MAC:
        print text
        return

    Generic.set(bold=False, underline=None)
    Generic.text(text + "\n\n")


# Print a title
def title(title):
    if IS_MAC:
        print "TITLE: " + title
        return

    Generic.set(bold=True, underline=1)
    Generic.text(title + "\n")


# Print a single line of text
def oneline(line):
    if IS_MAC:
        print line
        return

    Generic.text(line + "\n")


# Print a couple linefeeds so we can easily tear off the paper
def eom():
    if IS_MAC:
        return

    Generic.text("\n\n\n")

    # doesn't work :-(
    # Generic.control("LF")

###
# Printing
###

def print_message(message):
    title(message[u'sender'])
    message_date = datetime.strptime(message[u'date'][:19], DATETIME_FORMAT)
    oneline(datetime.strftime(message_date, '%H:%M'))
    text(message[u'body'])

def delete_message(message_id):
    url = 'http://0.0.0.0:5000/messages/{id}'.format(id = message_id)
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request(url)
    request.get_method = lambda: 'DELETE'
    opener.open(request)

# Get the messaege ids so we know which messages to get
response = urllib2.urlopen('http://0.0.0.0:5000/messages')
data = json.load(response)
message_ids = [d["message_id"] for d in data]

# Print the messages
for m in message_ids:
    url = 'http://0.0.0.0:5000/messages/{id}'.format(id = m)
    message = json.load(urllib2.urlopen(url))
    print_message(message)
    delete_message(m)



eom()
eom()
