'''
Picks up a field value from one field (sourceField) in an entry and copies it to a different field (destField).

For all entries of a content type in a defined language.
Optionally also publishes the entry after updating.

WARNING: Make sure you're not overwriting anything valuable!

Read comments below to better understand.

oskar.eiriksson@contentstack.com

2021-03-20
'''

import cma
import config

locale = 'en-us' # Locale of the entries that will be iterated over and updated
contentType = 'landing_page' # UID of the content type that will be iterated over and updated
sourceField = 'title' # Source field that will be copied from
destField = 'text_field' # Destination field that will be pasted to

publishEntries = True # If set to True, it tries to publish the entries. Else, it just updates them
environments = ['development'] # If you choose to publish - You can add more environments if needed
locales = [locale] # If you choose to publish, it will publish on these languages. Note: You can append more languages to the array to publish to than the updated one, if needed.

entries = cma.getAllEntries(contentType, locale)

for entry in entries['entries']:
    entry[destField] = entry[sourceField]
    body = {'entry': entry}
    updatedEntry = cma.updateEntry(contentType, locale, body)
    if publishEntries:
        cma.publishEntry(contentType, entry['uid'], environments, locales, locale, updatedEntry['entry']['_version'])