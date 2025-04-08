'''
Find and Replace values in fields. Built on top of the findAndReplace.py script. It should be able to handle more complex use cases.
Search in the whole body of the entry and replace only certain values. 
(E.g. replace 'A B' with 'A B C' but not when 'A B C' or 'A B YEAH' is the whole original string)

Limitation: Only searches for entries in the default locale. - If an entry only exists in other locales, it will not be searched.
Limitation: This script is just a proof of concept - it does not update or publish entries - Just shows you how to find and replace.

----
DISCLAIMER: This script is provided as-is, without any warranties or guarantees. Use at your own risk.

Read comments below to better understand.

oskar.eiriksson@contentstack.com

2025-04-08
'''
import re
import cma
import copy
from pprint import pprint

defaultLocale = 'en-us' # Also known as master locale
branch = 'main' # Branch name is main here - I recommend branching out in Contentstack if you are planning to extend this script to update and publish entries (to test and verify)

#Match "A B" but NOT "A B C" or "A B YEAH"
pattern = re.compile(r'\bA B\b(?! (C|YEAH))')
replacementValue = "A B C"
# In short, we replace any A B with A B C, but we make sure we ignore A B C so we don't end up with A B C C
# We also ignore A B YEAH

# Recursive replacement
def replaceValuesInDict(data, path=""):
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            result[key] = replaceValuesInDict(value, path + f".{key}")
        return result
    elif isinstance(data, list):
        return [replaceValuesInDict(item, path + f"[{i}]") for i, item in enumerate(data)]
    elif isinstance(data, str):
        if pattern.search(data):
            return pattern.sub(replacementValue, data)
        return data
    return data


contentTypes = cma.getAllContentTypes(branch) 

auditLog = []

for contentType in contentTypes['content_types']:
    print(f"\nProcessing content type: {contentType['uid']}")
    entries = cma.getAllEntries(contentType['uid'], defaultLocale, None, branch)
    if entries:
        for entry in entries['entries']:
            # Create a deep copy of the entry before modifying
            modifiedEntry = replaceValuesInDict(copy.deepcopy(entry))
            
            # We create an audit log if the original entry is different from the modified entry - And then we print it out in the end
            if entry != modifiedEntry:
                auditLog.append({
                    'uid': entry['uid'],
                    'contentType': contentType['uid'],
                    'locale': defaultLocale,
                    'original': entry,
                    'modified': modifiedEntry
                })
            availableLocales = []
            localesAvailable = cma.getEntryLanguages(contentType['uid'], entry['uid'], branch)
            if localesAvailable:
                for locale in localesAvailable['locales']:
                    if 'localised' in locale:
                        if locale['localised'] == True:
                            availableLocales.append(locale['locale'])
            if availableLocales:
                for locale in availableLocales:
                    entry = cma.getSingleEntry(contentType['uid'], locale, entry['uid'], branch)
                    # Create a deep copy of the entry before modifying
                    modifiedEntry = replaceValuesInDict(copy.deepcopy(entry))
                    if entry != modifiedEntry:
                        auditLog.append({
                            'uid': entry['uid'],
                            'contentType': contentType['uid'],
                            'locale': locale,
                            'original': entry,
                            'modified': modifiedEntry
                        })

# Below we print out the whole summary of changes and a detailed audit log
print("\n=== Find and Replace Summary ===")
print(f"Total entries that would be modified: {len(auditLog)}")
if auditLog:
    print("\nDetailed changes:")
    for entry_log in auditLog:
        print(f"\nEntry UID: {entry_log['uid']}")
        print(f"Content Type: {entry_log['contentType']}")
        print(f"Locale: {entry_log['locale']}")
        print("\nChanges found:")
        
        # Compare original and modified entries to show specific changes
        def find_string_differences(original, modified, path=""):
            if isinstance(original, dict) and isinstance(modified, dict):
                for key in original:
                    if key in modified:
                        find_string_differences(original[key], modified[key], f"{path}.{key}" if path else key)
            elif isinstance(original, list) and isinstance(modified, list):
                for i in range(min(len(original), len(modified))):
                    find_string_differences(original[i], modified[i], f"{path}[{i}]")
            elif isinstance(original, str) and isinstance(modified, str) and original != modified:
                print(f"  Path: {path}")
                print(f"  - Original: {original}")
                print(f"  - Modified: {modified}\n")
        
        find_string_differences(entry_log['original'], entry_log['modified'])
        print('\n--------------------------------\n')
else:
    print("\nNo entries would be modified.")
            

