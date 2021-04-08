'''
Gets a single entry
'''
import cma

contentType = 'landing_page'
locale = 'en-us'
version = None # If None, it just gets the newest version of the entry
uid = 'blt38a41c6dab858f9a' # Uid of the entry that we want to get

entry = cma.getSingleEntry(contentType, locale, uid, version)

print(entry)