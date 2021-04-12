'''
Get all content types

oskar.eiriksson@contentstack.com
'''
import json
import cma
import config
contentTypes = cma.getAllContentTypes()

config.logging.info('Number of Content Types: {}'.format(contentTypes['count']))
for contentType in contentTypes['content_types']:
    print(json.dumps(contentType, indent=1))
    print('----')