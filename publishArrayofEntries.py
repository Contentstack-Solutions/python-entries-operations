'''
Publishes ALL entries from ALL content types in a language to one or more environments. Optionally also publishes the entries in other locales (They cannot be localised).

Note: This is not bulk publishing
oskar.eiriksson@contentstack.com
2023-04-12
'''
import cma
import config

contentType = 'landing_page' # The content type - all entries need to be of this content type
environments = ['development'] # You can append to this if more environments are needed
entryUids = ['blt...', 'blt...'] # The entries to be published
locale = 'en-us' # The source locale to be published
locales = [locale] # You can append to this if you want to publish the 'locale' from above to more locales.

for uid in entryUids:
    try:
        cma.publishEntry(contentType, uid, environments, locales, locale) # Iterating over the entry uids and publishing one at a time
        config.logging.info('Published entry: ' + uid)
    except Exception as e:
        config.logging.error('Failed to publish entry: ' + uid + ' - ' + str(e))