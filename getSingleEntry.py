'''
Gets a single entry
'''
import json
import cma

contentType = 'landing_page'
locale = 'en-us'
version = None # If None, it just gets the newest version of the entry
uid = 'blt3d9fe6f76e416d1b' # Uid of the entry that we want to get

entry = cma.getSingleEntry(contentType, locale, uid, version)

print(json.dumps(entry, indent=1))