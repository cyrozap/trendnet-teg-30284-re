#!/usr/bin/env python3

import argparse
import struct
import sys

try:
    import trendnet_teg30284_fw
except ModuleNotFoundError:
    sys.stderr.write("Error: Failed to import \"trendnet_teg30284_fw.py\". Please run \"make\" in this directory to generate that file, then try running this script again.\n")
    sys.exit(1)


def checksum(data):
    temp = 0
    for i in range(len(data)):
        temp += struct.unpack_from('B', data, i)[0]

    return temp & 0xFFFFFFFF


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["info", "extract"], help="Subcommands.")
    parser.add_argument("firmware", type=str, help="The firmware update file.")
    args = parser.parse_args()

    fw = trendnet_teg30284_fw.TrendnetTeg30284Fw.from_file(args.firmware)
    update_count = len(fw.updates)
    if args.command == "info":
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
    if args.command == "extract":
        split = args.firmware.split('.')
        basename = '.'.join(split[:-1])
        for i in range(update_count):
            update = fw.updates[i]
            update.image._io.seek(0)
            f = open("{}.update_{}.{}.partition_{}.bin".format(basename, i, update.header.signature, update.header.partition), "wb")
            f.write(update.image._io.read_bytes_full())
            f.close()
            print("Extracted {} of {} images.".format(i+1, update_count))
