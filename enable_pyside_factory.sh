#!/bin/sh

gconftool-2 -s /maliit/factories -t list --list-type strings [libpymaliit.so]
