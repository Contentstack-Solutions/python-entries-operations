'''
Publishes all entries of a certain content type and in a language to one or more environments. Optionally also publishes that entry to other locales (They cannot be localised).

Note: This is not bulk publishing
oskar.eiriksson@contentstack.com
2021-04-09
'''
import cma
import config

contentType = 'landing_page'
environments = ['development'] # You can append to this if more environments are needed
locale = 'en-us' # The source locale to be published
locales = [locale] # You can append to this if you want to publish the 'locale' from above to more locales.

entries = cma.getAllEntries(contentType, locale) # First, getting all the entries

for entry in entries['entries']:
    cma.publishEntry(contentType, entry['uid'], environments, locales, locale, entry['_version']) # Iterating over the result and publishing one at a time