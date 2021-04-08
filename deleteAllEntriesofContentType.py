'''
Deletes all entries of a defined content type. If locale defined, then only in that locale, otherwise all entries of all languages

oskar.eiriksson@contentstack.com

BE CAREFUL!

See doc: https://www.contentstack.com/docs/developers/apis/content-management-api/?locale=north-america#delete-an-entry
'''
import cma
import config

contentType = 'landing_page'
locale = 'en-us'
deleteLocalized = False # If set to True, the locale variable above needs to be the master locale of the stack - It will then delete all entries, in all of the languages


entries = cma.getAllEntries(contentType, locale)
for entry in entries['entries']:
    config.logging.info('Deleting entry: {} - UID: {}'.format(entry['title'], entry['uid']))
    cma.deleteEntry(contentType, locale, entry['uid'], deleteLocalized)

