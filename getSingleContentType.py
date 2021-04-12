'''
Get all content types

oskar.eiriksson@contentstack.com
'''
import json
import cma
contentType = 'landing_page'
version = None # If None: Gets the newest version. If an Integer, it gets that specific version
contentType = cma.getSingleContentType(contentType, version)

print(json.dumps(contentType, indent=1))