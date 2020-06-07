#!/usr/bin/python
#
# ----------------------------------------------------------------------------------------------------
# DESCRIPTION
# ----------------------------------------------------------------------------------------------------
## @file    sPersonalData/personalDataCmd.py [ FILE   ] - Command module.
## @package sPersonalData.personalDataCmd    [ MODULE ] - Command module.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import os
import argparse

import sPersonalData.personalDataLib


#
# ----------------------------------------------------------------------------------------------------
# CODE
# ----------------------------------------------------------------------------------------------------
#
## @brief Display personal data.
#
#  @exception N/A
#
#  @return None - None.
def display():

    parser = argparse.ArgumentParser(description='Display personal data')

    parser.add_argument('file',
                        type=str,
                        help='File to be read')

    _args   = parser.parse_args()

    filePath = _args.file

    pd = sPersonalData.personalDataLib.PersonalData(filePath)
    pd.deserialize()
    pd.display()

#
## @brief Convert personal data formats.
#
#  @exception N/A
#
#  @return None - None.
def convert():

    parser = argparse.ArgumentParser(description='Convert personal data one format to another')

    parser.add_argument('fromFile',
                        type=str,
                        help='From file')

    parser.add_argument('toFile',
                        type=str,
                        help='To file')

    parser.add_argument('-o',
                        '--overwrite',
                        action='store_true',
                        help='Overwrite existing file')

    parser.add_argument('-d',
                        '--display',
                        action='store_true',
                        help='Display personal data after conversion')

    _args   = parser.parse_args()

    fromFilePath = _args.fromFile
    toFilePath   = _args.toFile
    overwrite    = _args.overwrite
    display      = _args.display

    pd = sPersonalData.personalDataLib.PersonalData(fromFilePath)
    pd.convert(toFilePath, overwrite, display)

#
## @brief Add new record to personal data.
#
#  @exception N/A
#
#  @return None - None.
def add():

    parser = argparse.ArgumentParser(description='Add personal data')

    parser.add_argument('file',
                        type=str,
                        help='File')

    parser.add_argument('-d',
                        '--display',
                        action='store_true',
                        help='Display personal data after conversion')

    _args   = parser.parse_args()

    filePath = _args.file
    display  = _args.display

    name = None
    phoneNumber = None
    address = None

    while not name:
        name = raw_input('Name: ')

    while not phoneNumber:
        phoneNumber = raw_input('Phone Number: ')

    while not address:
        address = raw_input('Address: ')

    pd = sPersonalData.personalDataLib.PersonalData(filePath)

    if os.path.isfile(filePath):
        pd.deserialize()

    pd.add(name=name, phoneNumber=phoneNumber, address=address)
    pd.serialize(overwrite=True)

    if display:
        pd.display()

#
## @brief Display filtered personal data.
#
#  @exception N/A
#
#  @return None - None.
def filter():

    parser = argparse.ArgumentParser(description='Filter personal data')

    parser.add_argument('file',
                        type=str,
                        help='File')

    _args   = parser.parse_args()

    filePath = _args.file

    name = raw_input('Name Filter: ')
    phoneNumber = raw_input('Phone Number Filter: ')
    address = raw_input('Address Filter: ')

    pd = sPersonalData.personalDataLib.PersonalData(filePath)

    if os.path.isfile(filePath):
        pd.deserialize()

    filteredPersonalData = pd.filter(name=name, phoneNumber=phoneNumber, address=address)

    if not filteredPersonalData:
        print '\nNo personal data with given filter(s) found.\n'
        return

    pd.setPersonList(filteredPersonalData)

    pd.display()