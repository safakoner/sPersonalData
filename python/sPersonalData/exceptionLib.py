#!/usr/bin/python
#
# ----------------------------------------------------------------------------------------------------
# DESCRIPTION
# ----------------------------------------------------------------------------------------------------
## @file    sPersonalData/exceptionLib.py [ FILE   ] - Exceptions.
## @package sPersonalData.exceptionLib    [ MODULE ] - Exceptions.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------

#
# ----------------------------------------------------------------------------------------------------
# CODE
# ----------------------------------------------------------------------------------------------------
#
## @brief [ EXCEPTION CLASS ] - Exception class.
class PersonAlreadyExistsError(Exception):

    pass

#
## @brief [ EXCEPTION CLASS ] - Exception class.
class UnsupportedFormatError(Exception):

    pass

#
## @brief [ EXCEPTION CLASS ] - Exception class.
class ConfigurationError(Exception):

    pass
