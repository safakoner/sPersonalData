#!/usr/bin/python
#
# ----------------------------------------------------------------------------------------------------
# DESCRIPTION
# ----------------------------------------------------------------------------------------------------
## @file    sPersonalData/personalDataSerializerXMLLib.py [ FILE   ] - XML serializer class module.
## @package sPersonalData.personalDataSerializerXMLLib    [ MODULE ] - XML serializer class module.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import xml.etree.ElementTree as ET

import sPersonalData.personLib
import sPersonalData.personalDataSerializerAbs


#
# ----------------------------------------------------------------------------------------------------
# CODE
# ----------------------------------------------------------------------------------------------------
#
## @brief [ SERIALIZER CLASS ] - XML serializer class.
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

        sPersonalData.personalDataSerializerAbs.Serializer.__init__(self, personList)

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

        root = ET.Element('personList')

        for person in self._personList:

            personElement = ET.SubElement(root, 'person')
            personElement.set('name', person.name())
            personElement.set('phoneNumber', person.phoneNumber())
            personElement.set('address', person.address())

        tree = ET.ElementTree(root)
        tree.write(filePath, method='xml')

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

        root = ET.parse(filePath).getroot()

        self._personList[:] = []

        for elem in root:
            self._personList.append(sPersonalData.personLib.Person(name=elem.attrib['name'],
                                                                   address=elem.attrib['address'],
                                                                   phoneNumber=elem.attrib['phoneNumber']))

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
            print '<b>Name:</b><span>{}</span><br>'.format(person.name())
            print '<b>Phone Number:</b><span>{}</span><br>'.format(person.phoneNumber())
            print '<b>Address:</b><span>{}</span><br><br>\n'.format(person.address())
