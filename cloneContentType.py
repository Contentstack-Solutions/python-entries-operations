'''
Do you need to clone a content type? E.g. change the uid? Or create a new one to make changes to it and then put it live?

This script clones a content type and all its entries.

LIMITATION: The newest version of the entries is only cloned. 
LIMITATION: This does not set the workflow stage or publish the cloned entry - This script could be extended to do that

WARNING: Make sure you're not overwriting anything valuable!

Read comments below to better understand.

oskar.eiriksson@contentstack.com

2022-10-26
'''

import cma
import config

sourceContentType = 'page' # UID of the content type that will be iterated over and updated
newContentTypeUid = 'page_v2' # UID of the new cloned content type
newContentTypeTitle = 'Page v2' # Title of the new cloned content type
masterLocale = 'en-us' # Exporting and importing the entries from that language - Then finding if the entry has been localised in others

# Getting the schema of the content type be cloned
sourceSchema = cma.getSingleContentType(sourceContentType)

# Replacing the content type schema with the new values
sourceSchema['content_type']['uid'] = newContentTypeUid
sourceSchema['content_type']['title'] = newContentTypeTitle

# Creating the new content type
cma.createContentType(sourceSchema)

entries = cma.getAllEntries(sourceContentType, masterLocale) # Getting all entries in the master locale from the source Content Type
if entries:
    for entry in entries['entries']:
        newEntry = cma.createEntry(newContentTypeUid, masterLocale, {'entry': entry}) # Creating the entry in the master locale in the new Content type
        entryLanguages = cma.getEntryLanguages(sourceContentType, entry['uid'])
        for language in entryLanguages['locales']:
            if 'localized' in language: # If localized is True, the entry is localised in that language
                localisedEntry = cma.getSingleEntry(sourceContentType, language['code'], entry['uid']) # Getting the entry in that language
                localisedEntry['entry']['uid'] = newEntry['entry']['uid'] # Setting the correct entry uid in the localised entry
                cma.updateEntry(newContentTypeUid, language['code'], localisedEntry) # Updating/Localising the entry in the new content type in that language
else:
    config.logging.error('No entries found in language: {}'.format(masterLocale))