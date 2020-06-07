#!/usr/bin/python
#
# ----------------------------------------------------------------------------------------------------
# DESCRIPTION
# ----------------------------------------------------------------------------------------------------
## @file    sPersonalData/personalDataSerializerAbs.py [ FILE   ] - Abstract serializer class module.
## @package sPersonalData.personalDataSerializerAbs    [ MODULE ] - Abstract serializer class module.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import os


#
# ----------------------------------------------------------------------------------------------------
# CODE
# ----------------------------------------------------------------------------------------------------
#
## @brief [ ABSTRACT CLASS ] - Format serializer abstract class.
class Serializer(object):
    
    #
    ## @brief Constructor.
    #
    #  @param personList [ list | None | in  ] - List of sPersonalData.personLib.Person class.
    #  
    #  @exception N/A
    #  
    #  @return None - None.
    def __init__(self, personList=[]):
        
        ## [ list ] - List of sPersonalData.personLib.Person class.
        self._personList = personList

    ## @name Properties

    # @{
    #
    ## @brief Set person list.
    #
    #  @param personList [ list | None | in  ] - List of sPersonalData.personLib.Person class.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def setPersonList(self, personList):

        self._personList = personList

    #
    ## @brief Get person list.
    #
    #  @exception N/A
    #
    #  @return list - List of sPersonalData.personLib.Person class.
    def personList(self):

        return self._personList

    #
    ## @}

    #
    ## @brief Serialize person list and write it out into the given file.
    #
    #  Method must return boolean value when implemented in child class.
    #
    #  @param filePath  [ str  | None  | in  ] - Path of a file.
    #  @param overwrite [ bool | False | in  ] - Overwrite existing file.
    #
    #  @exception IOError - If provided `filePath` does not exist.
    #
    #  @return Bool - Result.
    def serialize(self, filePath, overwrite=False):

        if not overwrite and os.path.isfile(filePath):
            raise IOError('File already exists: {}'.format(filePath))

        return False

    #
    ## @brief Deserialize from given file.
    #
    #  Method should return list of deserialized objects when its implemented
    #  in child class.
    #
    #  @param filePath [ str | None | in  ] - Path of a file.
    #
    #  @exception NotImplementedError - If this method is not implemented in child class.
    #
    #  @return list - List of sPersonalData.personLib.Person class.
    def deserialize(self, filePath):

        raise NotImplementedError('This method must be implemented in child class.')

    #
    ## @brief Display person list.
    #
    #  @exception NotImplementedError - If this method is not implemented in child class.
    #
    #  @return None - None.
    def display(self):

        raise NotImplementedError('This method must be implemented in child class.')


