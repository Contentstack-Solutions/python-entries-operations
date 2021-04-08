'''
Get all content types

oskar.eiriksson@contentstack.com
'''
import cma
import config
contentTypes = cma.getAllContentTypes()

config.logging.info('Number of Content Types: {}'.format(contentTypes['count']))
for contentType in contentTypes['content_types']:
    print(contentType)
    print('----')