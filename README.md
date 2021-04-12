# python-entries-operations

This collection uses the Content Management API from Contentstack. Functions found in the `cma/` folder.

Scripts in this repository:
* Copy Field Value - `copyFieldValue.py` (In case you want to rename the field uid or clone a value to a different field)
* Create an Entry - `createEntry.py`
* Delete All Entries of a Content Type - `deleteAllEntriesofContentType.py` (Be careful with this one)
* Get all entries - `getAllEntries.py`
* Get a Single Entry - `getSingleEntry.py`
* Publish all Entries - `publishAllEntries.py`
* Publish all Entries of a Certain Content Type - `publishAllEntriesFromContentType.py`
* Use a Query to Find an Entry - `queryEntries.py`

Comments at the top of every script describes what it does. Feel free to extend any script to fit your use case.

*NOT OFFICIALLY SUPPORTED BY CONTENTSTACK*

## Prerequisites:
* Contentstack Account.
* Install Python 3 (Developed using Python 3.9.1 on Macbook).
* Install Python package:
  * `pip install requests`

## Define environmental variables
e.g. `variables.env` file:
```
CS_REGION=NA (Either NA or EU)
CS_APIKEY=blt972.....
CS_MANAGEMENTOKEN=cs....

export CS_REGION CS_APIKEY CS_MANAGEMENTOKEN
```
and run `source variables.env` in the terminal.

