'''
Updates a field value in bulk - Finds a substring and replaces with a new string (Case sensitive). Simple example.
Built as a POC when somebody needed to replace a lot in the URL field for entries in a content type.

Limitation: Developed for a simple string field (e.g. single line text fields), does not work for complex field structures - but can easily be extended to fit other use cases.

For all entries of a content type in a defined language.
Optionally also publishes the entry after updating.

WARNING: Make sure you're not overwriting anything valuable!

Read comments below to better understand.

oskar.eiriksson@contentstack.com

2021-06-09
'''

import cma
import config

locale = 'en-us' # Locale of the entries that will be iterated over and updated
contentType = 'landing_page' # UID of the content type that will be iterated over and updated
fieldUid = 'url' # Source field that will be copied from

publishEntries = False # If set to True, it tries to publish the entries. Else, it just updates them
environments = ['development'] # If you choose to publish - You can add more environments if needed
locales = [locale] # If you choose to publish, it will publish on these languages. Note: You can append more languages to the array to publish to than the updated one, if needed.

oldSubString = 'article/' # What we will find and remove from the field value
newSubString = 'blog/' # We will replace the value above with this value

entries = cma.getAllEntries(contentType, locale) # Gets All the Entries of that content type in that locale - Iterates automatically to an array if the result has more than 100 entries

for entry in entries['entries']: # Iterates over the result
    updateEntry = False
    try:
        if oldSubString in entry[fieldUid]: # If the substring is found in the defined field
            updatedEntry = True
            body = {'entry': { 'uid': entry['uid'] }}
            body['entry'][fieldUid] = entry[fieldUid].replace(oldSubString, newSubString) # The actual replace is done here
            updatedEntry = cma.updateEntry(contentType, locale, body) # Updating the entry
            if updatedEntry:
                if publishEntries: # Optional boolean above
                    cma.publishEntry(contentType, entry['uid'], environments, locales, locale, updatedEntry['entry']['_version'])
        else:
            config.logging.info('No need to update entry: {} ({}) - Locale: {}'.format(entry['title'], entry['uid'], locale))
    except KeyError:
        config.logging.warning('{}KeyError - Possibly the source field ({}) does not exist in the content type schema, or does not have any value for this entry: {}{}'.format(config.YELLOW, sourceField, entry['uid'], config.END))