#!/bin/sh

gconftool-2 -s /maliit/onscreen/enabled -t list --list-type strings [pymaliit.py,]
gconftool-2 -s /maliit/onscreen/active -t list --list-type strings [pymaliit.py,ExamplePluginSubview1]
