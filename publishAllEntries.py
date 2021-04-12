'''
Publishes ALL entries from ALL content types in a language to one or more environments. Optionally also publishes the entries in other locales (They cannot be localised).

Note: This is not bulk publishing
oskar.eiriksson@contentstack.com
2021-04-09
'''
import cma
import config

contentTypes = cma.getAllContentTypes() # Getting all content types
environments = ['development'] # You can append to this if more environments are needed
locale = 'en-us' # The source locale to be published
locales = [locale] # You can append to this if you want to publish the 'locale' from above to more locales.

for contentType in contentTypes['content_types']: # First, iterating and getting all the content types
    entries = cma.getAllEntries(contentType['uid'], locale) # Getting all the entries from that content type
    if entries:
        for entry in entries['entries']:
            cma.publishEntry(contentType['uid'], entry['uid'], environments, locales, locale, entry['_version']) # Iterating over the result and publishing one at a time
    else:
        config.logging.info('No Entries in Content Type: {}'.format(contentType['uid']))