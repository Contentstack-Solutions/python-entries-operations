'''
Uses a query to find entries using the Content Management API.
Note: Queries documented inside the Content Delivery API docs: https://www.contentstack.com/docs/developers/apis/content-delivery-api/#queries

oskar.eiriksson@contentstack.com
'''

import cma
import config

query = '{"title": "Hello world"}'
contentType = 'landing_page'
locale = 'en-us'
environment = None

entries = cma.getAllEntries(contentType, locale, environment, query)

config.logging.info('Number of Entries Found: {}'.format(entries['count']))

for entry in entries['entries']:
    print(entry)
    print('----')