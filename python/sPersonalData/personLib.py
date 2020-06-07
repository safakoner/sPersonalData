#!/usr/bin/python
#
# ----------------------------------------------------------------------------------------------------
# DESCRIPTION
# ----------------------------------------------------------------------------------------------------
## @file    sPersonalData/personLib.py [ FILE   ] - Person module.
## @package sPersonalData.personLib    [ MODULE ] - Person module.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
#
## @brief [ CLASS ] - Person class.
class Person(object):

    #
    ## @brief Constructor.
    #
    #  @param name          [ str | None | in  ] - Name of the person.
    #  @param phoneNumber   [ str | None | in  ] - Phone number.
    #  @param address       [ str | None | in  ] - Address.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __init__(self, name=None, phoneNumber=None, address=None):

        ## [ str ] - Name of the person.
        self._name          = name
        ## [ str ] - Phone number.
        self._phoneNumber   = phoneNumber
        ## [ str ] - Address.
        self._address       = address

    #
    ## @brief Equal method.
    #
    #  @param other [ object | None | in  ] - Instance of sPersonalData.personLib.Person class.
    #  
    #  @exception N/A
    #  
    #  @return bool - Result.
    def __eq__(self, other):

        return self._name == other.name() and self._address == other.address() and self._phoneNumber == other.phoneNumber()

    #
    ## @brief String representation.
    #
    #  @exception N/A
    #
    #  @return str - Result.
    def __str__(self):

        return '\nName        : {}\nAddress     : {}\nPhone Number: {}'.format(self._name, self._address, self._phoneNumber)

    ## @name Properties

    # @{
    #
    ## @brief Name.
    #
    #  @exception N/A
    #
    #  @return str - Result.
    def name(self):

        return self._name

    #
    ## @brief Phone number.
    #
    #  @exception N/A
    #
    #  @return str - Result.
    def phoneNumber(self):

        return self._phoneNumber

    #
    ## @brief Address.
    #
    #  @exception N/A
    #
    #  @return str - Result.
    def address(self):

        return self._address

    #
    ## @}
