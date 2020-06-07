#!/usr/bin/python
#
# ----------------------------------------------------------------------------------------------------
# DESCRIPTION
# ----------------------------------------------------------------------------------------------------
## @file    sPersonalData/personalDataTest.py [ FILE   ] - Unit test module.
## @package sPersonalData.personalDataTest    [ MODULE ] - Unit test module.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import os
import unittest

import sPersonalData.personLib
import sPersonalData.personalDataLib
import sPersonalData.personalDataSerializerJSONLib
import sPersonalData.personalDataSerializerXMLLib


#
# ----------------------------------------------------------------------------------------------------
# CODE
# ----------------------------------------------------------------------------------------------------
TEST_FOLDER = os.path.abspath(os.path.join(__file__, '..', '..', '..', 'test'))

class Functionalities(unittest.TestCase):

    def test_getFormats(self):

        self.assertEquals(['JSON', 'XML'],
                          sPersonalData.personalDataLib.PersonalData.getFormats())

    def test_getSerializerJSON(self):

        self.assertFalse(isinstance(sPersonalData.personalDataLib.PersonalData.getSerializer('JSON'),
                         sPersonalData.personalDataSerializerJSONLib.Serializer))

    def test_getSerializerXML(self):

        self.assertFalse(isinstance(sPersonalData.personalDataLib.PersonalData.getSerializer('XML'),
                         sPersonalData.personalDataSerializerXMLLib.Serializer))


class JSON(unittest.TestCase):

    def setUp(self):

        self._jsonFile = os.path.join(TEST_FOLDER, 'personalData.json')
        self._xmlFile  = os.path.join(TEST_FOLDER, 'personalData.xml')

    def tearDown(self):

        if os.path.isfile(self._jsonFile):
            os.remove(self._jsonFile)

        if os.path.isfile(self._xmlFile):
            os.remove(self._xmlFile)

    def test_all(self):

        p1 = sPersonalData.personLib.Person(name='Hayri Safak Oner',
                                            phoneNumber='604 723 3547',
                                            address='West 3rd Ave')

        personalData = sPersonalData.personalDataLib.PersonalData(filePath=self._jsonFile)

        personalData.addByObject(p1, allowDuplicate=True)

        self.assertTrue(personalData.serialize(overwrite=True))

        #

        personalData = sPersonalData.personalDataLib.PersonalData(filePath=self._jsonFile)

        personalData.deserialize()

        personalData.add(name='Pete Mitchell',
                         phoneNumber='234',
                         address='Miramar',
                         allowDuplicate=True)

        self.assertTrue(personalData.serialize(overwrite=True))

        #

        self.assertTrue(personalData.hasPerson(p1))

        p2 = sPersonalData.personLib.Person(name='Tom Kazansky')

        self.assertFalse(personalData.hasPerson(p2))

        #

        self.assertTrue(personalData.convert(self._xmlFile, overwrite=True))

        #

        self.assertEquals(len(personalData.filter(name='Pete*')), 1)

        self.assertEquals(len(personalData.filter(phoneNumber='2*')), 1)


if __name__ == '__main__':

    unittest.main()
