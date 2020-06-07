#!/usr/bin/python
#
# ----------------------------------------------------------------------------------------------------
# DESCRIPTION
# ----------------------------------------------------------------------------------------------------
## @file    sPersonalData/personalDataLib.py [ FILE   ] - Personal data abstract class module.
## @package sPersonalData.personalDataLib    [ MODULE ] - Personal data abstract class module.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import os
import re
import fnmatch
import importlib

import sPersonalData.exceptionLib
import sPersonalData.personLib


#
# ----------------------------------------------------------------------------------------------------
# CODE
# ----------------------------------------------------------------------------------------------------
#
## @brief [ CLASS ] - Personal class.
class PersonalData(object):

    #
    ## @brief Constructor.
    #
    #  @param filePath [ str | None | in  ] - File to operate on.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __init__(self, filePath=None):
        
        ## [ str ] - File to be operate on.
        self._filePath   = filePath

        ## [ list ] - List of sPersonalData.personLib.Person class.
        self._personList = []

        ## [ object ] - Serializer object instance based on the format being operated on.
        self._serializer = None

    ## @name Properties

    # @{
    #
    ## @brief Get person list.
    #
    #  @exception N/A
    #
    #  @return list - List of sPersonalData.personLib.Person class.
    def personList(self):

        return self._personList

    #
    ## @brief Set person list.
    #
    #  @param personList [ list | None | in  ] - List of sPersonalData.personLib.Person class.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def setPersonList(self, personList):

        self._personList = personList[:]

        if not self._serializer:
            self._serializer = self.getSerializer(self._filePath)()

        self._serializer.setPersonList(self._personList)

    #
    ## @}

    #
    ## @brief Add new person.
    #
    #  Method only add new person, you must call serialize method to write the
    #  changes on file.
    #
    #  @param name              [ str  | None  | in  ] - Name.
    #  @param phoneNumber       [ str  | None  | in  ] - Phone number.
    #  @param address           [ str  | None  | in  ] - Address.
    #  @param allowDuplicate    [ bool | False | in  ] - Whether duplicate record should be allowed.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def add(self, name, phoneNumber, address, allowDuplicate=False):

        newPerson = sPersonalData.personLib.Person(name, phoneNumber, address)

        if not allowDuplicate:
            self.hasPerson(newPerson, raiseException=True)

        self._personList.append(newPerson)

        return True

    #
    ## @brief Add new person by providing Person object.
    #
    #  @param personInstance [ sPersonalData.personLib.Person | None  | in  ] - Instance of sPersonalData.personLib.Person class.
    #  @param allowDuplicate [ bool                           | False | in  ] - Whether duplicate record should be allowed.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def addByObject(self, personInstance, allowDuplicate=False):

        if not allowDuplicate:
            self.hasPerson(personInstance, raiseException=True)

        self._personList.append(personInstance)

        return True

    #
    ## @brief Check whether given person already exists.
    #
    #  @param personInstance [ sPersonalData.personLib.Person | None  | in  ] - Instance of sPersonalData.personLib.Person class.
    #  @param raiseException [ bool                           | False | in  ] - Raise sPersonalData.exceptionLib.PersonAlreadyExistsError exception if the given person exits.
    #
    #  @exception sPersonalData.exceptionLib.PersonAlreadyExistsError - If given person exists and `raiseException` provided True.
    #
    #  @return bool - Result.
    def hasPerson(self, personInstance, raiseException=False):

        if not self._personList:
            return False

        if [x for x in self._personList if personInstance == x]:
            if raiseException:
                raise sPersonalData.exceptionLib.PersonAlreadyExistsError('Person with the following data already exists, name: "{}", phone number: "{}", address: "{}"'.format(personInstance.name(),
                                                                                                                                                                                personInstance.phoneNumber(),
                                                                                                                                                                                personInstance.address()))
            return True

        return False

    #
    ## @brief Serialize person list into the file based on the format being operated on.
    #
    #  @param overwrite [ bool | False | in  ] - Whether existing file should be overwritten.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def serialize(self, overwrite=False):

        self._serializer = self.getSerializer(self._filePath)(self._personList)
        self._serializer.serialize(self._filePath, overwrite)

        return True

    #
    ## @brief Deserialize object from the file being operated on.
    #
    #  @exception N/A
    #
    #  @return list - List of sPersonalData.personLib.Person class.
    def deserialize(self):

        self._serializer = self.getSerializer(self._filePath)()
        self._personList = self._serializer.deserialize(self._filePath)

        return self._personList

    #
    ## @brief Display personal data.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def display(self):

        if not self._serializer:
            print 'You must call serialize or deserialize method in order to display data.'
            return

        try:
            self._serializer.display()
        except NotImplementedError as error:

            if not self._personList:
                print '\nNo person data to display.\n'
                return

            for person in self._personList:
                print person
    
    #
    ## @brief Convert the personal data into the format by provided by a file.
    #
    #  Convert format will be determined by the extension of `toFile` argument.
    #
    #  @param toFile    [ str  | None  | in  ] - File which will be written out with the new format determined by the extension
    #  @param overwrite [ bool | False | in  ] - Whether to overwrite the existing file.
    #  @param display   [ bool | False | in  ] - Whether to display converted data.
    #  
    #  @exception N/A
    #  
    #  @return object - Serializer object instance which would be used to convert the data will be returned.
    def convert(self, toFile, overwrite=False, display=False):

        toFormat = os.path.splitext(toFile)[1][1:].upper()

        formatList = PersonalData.getFormats()
        if not toFormat in formatList:
            raise sPersonalData.exceptionLib.UnsupportedFormatError('This format is not supported: {}'.format(toFormat))

        self.deserialize()

        serializer = PersonalData.getSerializer(toFormat)(self._personList)
        serializer.serialize(toFile, overwrite)

        if display:
            serializer.display()

        return serializer

    #
    ## @brief Filter personal data by using wildcards.
    #
    #  @param name          [ str | None | in  ] - Filter for name of the person.
    #  @param phoneNumber   [ str | None | in  ] - Filter for phone number.
    #  @param address       [ str | None | in  ] - Filter for address.
    #
    #  @exception N/A
    #
    #  @return list - Filtered list of sPersonalData.personLib.Person class.
    def filter(self, name=None, phoneNumber=None, address=None):

        if not self._serializer:
            raise sPersonalData.exceptionLib.ConfigurationError('You must call serialize or deserialize method in order to display data.')

        if not self._serializer.personList():
            return []

        filteredPersonList = []

        if name:
            filteredPersonList.extend([p for p in self._serializer.personList() if name and fnmatch.fnmatch(p.name(), name)])

        if phoneNumber:
            filteredPersonList.extend([p for p in self._serializer.personList() if phoneNumber and fnmatch.fnmatch(p.phoneNumber(), phoneNumber)])

        if address:
            filteredPersonList.extend([p for p in self._serializer.personList() if address and fnmatch.fnmatch(p.address(), address)])

        return filteredPersonList

    #
    ## @brief Get valid formats which can be operated with.
    #
    #  @exception N/A
    #
    #  @return list of str - Formats.
    @staticmethod
    def getFormats():

        pythonModuleList = os.listdir(os.path.dirname(__file__))
        if not pythonModuleList:
            return None

        formatList = []

        for moduleName in pythonModuleList:

            formatName = re.search(r'personalDataSerializer([A-Z]{2,})Lib.py$', moduleName)

            if formatName:
                formatList.append(formatName.groups()[0])

        return formatList
    
    #
    ## @brief Get serializer for given format.
    #
    #  If file path is provided as `formatName`, extension of it will be used to get the right serializer.
    #
    #  @param formatName [ str | None | in  ] - Either name of the format (JSON, XML) or file name with extension.
    #  
    #  @exception sPersonalData.exceptionLib.UnsupportedFormatError - If unsupported format provided.
    #  @exception sPersonalData.exceptionLib.ConfigurationError     - If serializer module doesn't have a class named "Serializer".
    #
    #  @return object - Serializer object (not an instance).
    @staticmethod
    def getSerializer(formatName):

        formatList = PersonalData.getFormats()

        if not formatName in formatList:
            formatName = os.path.splitext(formatName)[1][1:].upper()
            if not formatName:
                raise sPersonalData.exceptionLib.UnsupportedFormatError('No valid format found, valid formats are: {}'.format(', '.join(PersonalData.getFormats())))

        if not formatName in formatList:
            raise sPersonalData.exceptionLib.UnsupportedFormatError('This format is not supported: {}'.format(formatName))

        serializerModuleName = 'personalDataSerializer{}Lib'.format(formatName)
        module = None

        try:
            module = importlib.import_module('sPersonalData.{}'.format(serializerModuleName))
        except ImportError as error:
            raise sPersonalData.exceptionLib.UnsupportedFormatError('This format is not supported: {}\nError: {}'.format(formatName, error))

        reload(module)

        if not hasattr(module, 'Serializer'):
            raise sPersonalData.exceptionLib.ConfigurationError('Module does not have a class named "Serializer" {}'.format(str(module)))

        return getattr(module, 'Serializer')

