'''
Gets all entries of a certain content type in a defined language

oskar.eiriksson@contentstack.com
'''

import cma
import config

contentType = 'landing_page'
locale = 'en-us'
environment = None # If specified, only fetches the entries published in that environment. If None, fetches all entries in the content type

entries = cma.getAllEntries(contentType, locale, environment)

config.logging.info('Total Number of Entries in Response: {}'.format(entries['count']))

for entry in entries['entries']:
    print(entry)
    print('---')
