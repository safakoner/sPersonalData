# About This Package

I was asked to deliver a technical task for a job offering. I was offered a job upon providing this package, along with
API reference (Doxygen) and additional documentation like the one below. 

# Table of Contents

- [Requirements for the Task](#requirements-for-the-task)
- [Overview](#overview)
- [API Reference](#api-reference)
- [Setup](#setup)
- [Creating and Adding Personal Data](#creating-and-adding-personal-data)
- [Displaying Personal Data](#displaying-personal-data)
- [Converting Personal Data](#converting-personal-data)
- [Filtering Personal Data](#filtering-personal-data)
- [Adding a New Format](#adding-a-new-format)
- [Command Line Interface](#command-line-interface)
  * [spersonaldata-add](#spersonaldata-add)
  * [spersonaldata-convert](#spersonaldata-convert)
  * [spersonaldata-display](#spersonaldata-display)
  * [spersonaldata-filter](#spersonaldata-filter)
  
# Requirements for the Task

The brief for this challenge is as follows:

In Python or C++ write a module or small library which shows how you would take a set of personal data, where each
record contains:

- name
- address
- phone number

And:

build a simple API allowing you to add new records, filter users (e.g "name=Joe*") based on some simple search syntax
like Glob. Support serialisation in 2 or more formats (e.g JSON, Yaml, XML, CSV etc). Display the data in 2 or more
different output formats (no need to use a GUI Framework, use e.g text output/HTML or any other human readable format).
Add a command line interface to add records, and display/convert/filter the whole data set. Write it in such a way that
it would be easy for a developer to extend the system e.g

- to add support for additional storage formats
- to query a list of currently supported formats

This should ideally show Object-Oriented Design and Design Patterns Knowledge, we’re not looking for use of advanced
Language constructs.

Please provide reasonable Unit Test coverage and basic API documentation

The task is designed to allow you some flexibility in how you design and implement it, and you should submit something
that demonstrates your abilities and/or values as a Software Engineer. 

# Overview

This package contains tools and API, which you can use to operate on personal data.
Personal data is/can be kept by the supported formats. The API determines which format to use
based on the extension of the files being operated on, therefore no format manually/explicitly
need to be provided to the API.

## API Reference

API reference (Doxygen) of the package is available in `sPersonalData/doc/developerDoxygenPython/html` folder.

# Setup

**This package is developed with Python 2.7**

Add the following path to Python path.

- `sPersonalData/python`

Add the one of the following path to bin path.

- `sPersonalData/bin/darwin`
- `sPersonalData/bin/linux`

Import the modules.

```python
import sPersonalData.personLib
import sPersonalData.personalDataLib
```

Set the files, which we will use for serialization/deserialization.

```python
TEST_FOLDER = os.path.abspath(os.path.join(__file__, '..', '..', '..', 'test'))

JSON_FILE   = os.path.join(TEST_FOLDER, 'personalData.json')

XML_FILE    = os.path.join(TEST_FOLDER, 'personalData.xml')
```

# Creating and Adding Personal Data

```python

# Create an instance of sPersonalData.personLib.Person class like so

p1 = sPersonalData.personLib.Person(name='Safak Oner',
                                    phoneNumber='607 999 8822',
                                    address='Los Angeles, California')

# Create an instance of sPersonalData.personalDataLib.PersonalData
# class by providing a file that you want to work on. If provided file doesn't
# exist, it will be created.

personalData = sPersonalData.personalDataLib.PersonalData(filePath=JSON_FILE)

# Add the person to personal data like so
# allowDuplicate argument allows you to add duplicates into personal data

personalData.addByObject(p1, allowDuplicate=True)

# Now you can serialize the data into the file
# You can pass True to overwrite argument if you want to overwrite
# the file if it already exists
# Please remember, serialization format is determined by the extension of the
# provided file

personalData.serialize(overwrite=True)
```

Operating on an existing files is exactly the same.

You can also use `sPersonalData.personalDataLib.PersonalData.add` method to provide raw
information in order to add a new peron, which would look like;

```python
personalData = sPersonalData.personalDataLib.PersonalData(filePath=JSON_FILE)

personalData.add(name='Pete Mitchell',
                 phoneNumber='111 222 5566',
                 address='Miramar, San Diego, California',
                 allowDuplicate=True)

personalData.serialize(overwrite=True)
```

# Displaying Personal Data

In order to display personal data you can invoke `sPersonalData.personalDataLib.PersonalData.display` method, like so;

```python
personalData = sPersonalData.personalDataLib.PersonalData(filePath=JSON_FILE)

personalData.deserialize()

personalData.display()
```

You can customize the way personal data gets displayed by implementing abstract class method
`sPersonalData.personalDataSerializerAbs.Serializer.display` in your serialize child class, which
essentially provides formats. If this method is not implemented in the child class, default
display format of plain text will be used.

You can check `sPersonalData.personalDataSerializerXMLLib.Serializer.display` method for example implementation.

# Converting Personal Data

You can convert one format to another by using `sPersonalData.personalDataLib.PersonalData.convert` method.
Please note, this operation applies to supported formats only. Supported formats can be obtained by using
`sPersonalData.personalDataLib.PersonalData.getFormats` method, like so;

```python
print sPersonalData.personalDataLib.PersonalData.getFormats()

#['JSON', 'XML']
```

Conversion between two formats is done like so;

```python
personalData = sPersonalData.personalDataLib.PersonalData(filePath=JSON_FILE)

personalData.deserialize()

personalData.convert(toFile=XML_FILE, overwrite=True, display=True)
```

As you can see `convert` method accepts three arguments. Namely;

- `toFile` Destination file, format is determined automatically by the extension of the file.
- `overwrite` Whether `toFile` should be overwritten if it already exists.
- `display` Display converted data.

# Filtering Personal Data

Filtering personal data is done by using `sPersonalData.personalDataLib.PersonalData.filter` method.
Method accepts three arguments where wildcard filtering can be provided. Those arguments are;

- `name`
- `phoneNumber`
- `address`

Filtering can be done as its given in the example below.

```python
personalData = sPersonalData.personalDataLib.PersonalData(filePath=JSON_FILE)

personalData.deserialize()

print personalData.filter(name='Pete*'))

print personalData.filter(name='Pete*', phoneNumber='2*', address='*mar'))
```

# Adding a New Format

Adding a new format (supporting serialization/deserialization for a new format) is extremely easy.
Say you want to add CSV format, just follow the steps below.

- Create a Python module named `personalDataSerializer<FORMAT>Lib.py` in this package,
since in this example format is CSV, the name of the module must be `personalDataSerializerCSVLib.py`

**Note:** By doing this, you are actually creating/supporting a new format. The API will be using this
naming convention and extracting the format name from the name of the serializer modules dynamically in order
to operate on them. So no hard coded implementation needed in order to tell the API which formats are supported.

- Create a class named `Serializer` in this module that inherits `sPersonalData.personalDataSerializerAbs.Serializer`
abstract class.

- Overwrite `serialize` method of the abstract class to serialize the data.

- Overwrite `deserialize` method of the abstract class to deserialize the data.

- Optionally you can overwrite `display` method of the abstract class if you want to display the
 personal data in a very specific way for this format.

You can check `sPersonalData.personalDataSerializerJSONLib.Serializer` class implementation
as a very good and simple example.

Entire abstract class documentation can be found at `sPersonalData.personalDataSerializerAbs.Serializer`

# Command Line Interface

The package comes with some useful commands that you can use.

## spersonaldata-add

You will be prompted by several questions about the person namely name, phone number and address.
Once you entered the information new personal data will be saved into the file which being operated.

**Flags**

- `file`           File to be operated on.
- `-d --display`   Display data after the operation.

```shell script
spersonaldata-add personalData.json -d
```

## spersonaldata-convert

You can convert between formats by using this command. Formats that will be operated on will be
determined automatically based on the extensions of the provided files.

**Flags**

- `fromFile`          From file.
- `toFIle`            To file.
- `-o --overwrite`    Overwrite existing `toFile`
- `-d --display`      Display converted data after the operation.

```shell script
spersonaldata-convert personalData.json personalData.xml -o -d
```

## spersonaldata-display

This command displays the data from the file being operated on.

**Flags**

- `file` File to be operated on.

```shell script
spersonaldata-display personalData.json
```

## spersonaldata-filter

This command allows you to filter personal data from the file being operated on. You will be prompted
by several questions to filter the personal data by name, phone number and address. Non of these questions
are mandatory to answer. You can also use wildcard in your filters.

**Flags**

- `file` File to be operated on.

```shell script
spersonaldata-filter personalData.json
Name Filter: S*
Phone Number Filter: 2*
Address Filter:

# #Name        : Safak Oner
# #Address     : Los Angeles, California
# #Phone Number: 607 999 8822
#
# #Name        : Pete Mitchell
# #Address     : Miramar, San Diego, California
# #Phone Number: 111 222 5566
```