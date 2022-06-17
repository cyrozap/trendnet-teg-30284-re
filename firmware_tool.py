#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later

# firmware_tool.py - A tool to parse TEG-30284 firmware update files.
# Copyright (C) 2019, 2022  Forest Crossman <cyrozap@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import argparse
import sys

try:
    import trendnet_teg30284_fw
except ModuleNotFoundError:
    sys.stderr.write("Error: Failed to import \"trendnet_teg30284_fw.py\". Please run \"make\" in this directory to generate that file, then try running this script again.\n")
    sys.exit(1)


def checksum(data : bytes):
    return sum(data) & 0xFFFFFFFF

def extract(filename, fw):
    split = filename.split('.')
    basename = '.'.join(split[:-1])
    update_count = len(fw.updates)
    for i in range(update_count):
        update = fw.updates[i]
        update.image._io.seek(0)
        f = open("{}.update_{}.{}.partition_{}.bin".format(basename, i, update.header.signature, update.header.partition), "wb")
        f.write(update.image._io.read_bytes_full())
        f.close()
        print("Extracted {} of {} images.".format(i+1, update_count))

    return 0

def info(filename, fw):
    update_count = len(fw.updates)
    for i in range(update_count):
        update = fw.updates[i]
        print("Update {} of {}:".format(i+1, update_count))
        update.image._io.seek(0)
        image = update.image._io.read_bytes_full()
        ic = checksum(image)
        ic_valid = False
        if ic == update.header.image_checksum:
            ic_valid = True
        print("  Image checksum: 0x{:08X} ({})".format(ic, "VALID" if ic_valid else "INVALID"))
        print("  Model: {}".format(update.header.model))
        print("  Signature: {}".format(update.header.signature))
        print("  Partition: {}".format(update.header.partition))
        print("  Customer signature: {}".format(update.header.customer_sig))
        print("  Board version: {}".format(update.header.board_ver))
        print("  Image size: {}".format(update.header.image_len))
        print("  Image firmware version: {}".format(update.image.fw_version))
        idc = checksum(image[:-4])
        idc_valid = False
        if idc == update.image.checksum:
            idc_valid = True
        print("  Image data checksum: 0x{:08X} ({})".format(idc, "VALID" if idc_valid else "INVALID"))
        print()

    return 0

def main():
    commands = {
        "extract": extract,
        "info": info,
    }

    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=commands.keys(), help="Subcommands.")
    parser.add_argument("firmware", type=str, help="The firmware update file.")
    args = parser.parse_args()

    fw = trendnet_teg30284_fw.TrendnetTeg30284Fw.from_file(args.firmware)
    return commands[args.command](args.firmware, fw)


if __name__ == "__main__":
    sys.exit(main())
