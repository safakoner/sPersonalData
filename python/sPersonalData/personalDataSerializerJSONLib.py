#!/usr/bin/python
#
# ----------------------------------------------------------------------------------------------------
# DESCRIPTION
# ----------------------------------------------------------------------------------------------------
## @file    sPersonalData/personalDataSerializerJSONLib.py [ FILE   ] - JSON serializer class module.
## @package sPersonalData.personalDataSerializerJSONLib    [ MODULE ] - JSON serializer class module.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import json
from   pprint import pprint

import sPersonalData.personLib
import sPersonalData.personalDataSerializerAbs


#
# ----------------------------------------------------------------------------------------------------
# CODE
# ----------------------------------------------------------------------------------------------------
#
## @brief [ SERIALIZER CLASS ] - JSON serializer class.
class Serializer(sPersonalData.personalDataSerializerAbs.Serializer):

    #
    ## @brief Constructor.
    #
    #  @param personList [ list | None | in  ] - List of sPersonalData.personLib.Person class.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __init__(self, personList=[]):

        sPersonalData.personalDataSerializerAbs.Serializer.__dict__['__init__'](self, personList)

    #
    ## @brief Serialize person list and write it out into the given file.
    #
    #  @param filePath  [ str  | None  | in  ] - Path of a file.
    #  @param overwrite [ bool | False | in  ] - Overwrite existing file.
    #
    #  @exception N/A
    #
    #  @return Bool - Result.
    def serialize(self, filePath, overwrite=False):

        sPersonalData.personalDataSerializerAbs.Serializer.__dict__['serialize'](self, filePath, overwrite)

        personList = [{'name':x.name(), 'phoneNumber':x.phoneNumber(), 'address':x.address()} for x in self._personList]

        with open(filePath, 'w') as outFile:
            json.dump(personList, outFile, sort_keys=True, indent=4)

        return True

    #
    ## @brief Deserialize from given file.
    #
    #  Method should return list of deserialized objects when its implemented
    #  in child class.
    #
    #  @param filePath [ str | None | in  ] - Path of a file.
    #
    #  @exception N/A
    #
    #  @return list - List of sPersonalData.personLib.Person class.
    def deserialize(self, filePath):

        personList = None

        with open(filePath) as inFile:
            personList = json.load(inFile)

        if not personList:
            return None

        self._personList[:] = []

        self._personList = [sPersonalData.personLib.Person(name=x['name'],
                                                           phoneNumber=x['phoneNumber'],
                                                           address=x['address']) for x in personList]

        return self._personList

    #
    ## @brief Display person list.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def display(self):

        if not self._personList:
            print '\nNo person data to display.\n'
            return

        for person in self._personList:
            # Remove _ at the beginning of the attributes and display
            pprint([(v[1:], k) for v, k in person.__dict__.iteritems()])

