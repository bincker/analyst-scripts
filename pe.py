#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import pefile
import argparse
import sys
import hashlib

"""Display infos about a PE file
Author : Tek <tek@randhome.io>
Date : 5/10/2016
"""


def display_hashes(data):
    """Display md5, sha1 and sh256 of the data given"""
    for algo in ["md5", "sha1", "sha256"]:
        m = getattr(hashlib, algo)()
        m.update(data)
        print("%s\t%s" % (algo.upper(), m.hexdigest()))


def display_sections(pe):
    """Display information about the PE sections"""
    print("Name\tVirtualSize\tVirtualAddress\tRawSize\t\tRawAddress")
    for section in pe.sections:
        print("%s\t%s\t\t%s\t\t%s\t\t%s" % (
                section.Name,
                hex(section.Misc_VirtualSize),
                hex(section.VirtualAddress),
                hex(section.PointerToRawData),
                hex(section.SizeOfRawData)
        ))


def display_imports(pe):
    """Display imports"""
    for entry in pe.DIRECTORY_ENTRY_IMPORT:
        print(entry.dll)
        for imp in entry.imports:
            print('\t%s %s' % (hex(imp.address), imp.name))


def display_exports(pe):
    """Display exports"""
    try:
        for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
            print("%s %s %s" % (
                hex(pe.OPTIONAL_HEADER.ImageBase + exp.address),
                exp.name,
                exp.ordinal
            ))
    except AttributeError:
        return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Display information about a PE file')
    parser.add_argument('FILE', help='a PE file')
    parser.add_argument('--sections', '-s', action='store_true', help='Only display sections')
    parser.add_argument('--imports', '-i',  action='store_true', help='Display imports only')
    parser.add_argument('--exports', '-e',  action='store_true', help='Display exports only')
    parser.add_argument('--full', '-f',  action='store_true', help='Full dump of all pefile infos')
    args = parser.parse_args()

    fin = open(args.FILE, 'rb')
    data = fin.read()
    fin.close()
    pe = pefile.PE(data=data)

    if args.sections:
        display_sections(pe)
        sys.exit(0)
    if args.imports:
        display_imports(pe)
        sys.exit(0)
    if args.exports:
        display_exports(pe)
        sys.exit(0)
    if args.full:
        print(pe.dump_info())
        sys.exit(0)

    display_hashes(data)
    print("")
    display_sections(pe)
    print("")
    display_imports(pe)
    print("")
    display_exports(pe)
