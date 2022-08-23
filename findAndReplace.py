'''
Find and Replace values in fields. Only works on simple fields but can be extended using queries to search within groups and modular blocks.

---
In case of regular expression search:
See more:
    * https://www.contentstack.com/docs/developers/apis/content-delivery-api/#search-by-regex
    * https://www.contentstack.com/docs/developers/apis/content-delivery-api/#search-by-regex-within-group
    * https://www.contentstack.com/docs/developers/apis/content-delivery-api/#search-by-regex-within-modular-blocks

The defined regular expression in the code is on the format: "^.*foo.*$" (searches for the foo value anywhere in the string - The value does not need to be a whole word)
Feel free to change the regular expression to match your needs. I recommend trying them out in Postman (A Postman Collection for the Content Delivery API is available)

See variable "regularExpression" in code below. Make sure regexSearch is set to True to use regular expression in the search.
---

WARNING: Make sure you're not overwriting anything valuable!

Read comments below to better understand.

oskar.eiriksson@contentstack.com

2022-08-22
'''

import cma
import config

updateContentstack = False # If False it only prints out the value before and after replace - If True it updates the values in Contentstack and optionally publishes.
regexSearch = True # If False it only mathes the whole value of the field. If True it searches using regular expression and finds it if the field value starts with that string.

locale = 'en-us' # Locale of the entries that will be iterated over and updated.
contentType = 'landing_page' # UID of the content type that will be iterated over and updated.
fieldUid = 'title' # Field UID where value will be searched and optionally updated if found.

searchString = 'Hello' # The value you are looking for.
replaceString = 'goodbye' # The value you want to replace with.


publishEntries = False # If set to True, it tries to publish the entries. Else, it just updates them
environments = ['development'] # If you choose to publish - You can add more environments if needed
locales = [locale] # If you choose to publish, it will publish on these languages. Note: You can append more languages to the array to publish to than the updated one, if needed.

regularExpression = "^.*{}.*$".format(searchString)
if regexSearch:
    query = '{{ "{}": {{ "$regex": "{}"}} }}'.format(fieldUid, regularExpression)
else: 
    query = '{{"{}": "{}"}}'.format(fieldUid, searchString)

entries = cma.getAllEntries(contentType, locale, None, query)

if entries:
    config.logging.info('Number of found entries in response: {}'.format(entries['count']))
    for entry in entries['entries']:
        newValue = entry[fieldUid].replace(searchString, replaceString)
        config.logging.info('Entry UID: {}{}{} - Value found in field {}: {}{}{} - New value: {}{}{}'.format(config.UNDERLINE, entry['uid'], config.END, fieldUid, config.YELLOW, entry[fieldUid], config.END, config.GREEN, newValue, config.END))
        if updateContentstack:
            entry[fieldUid] = newValue
            body = {'entry': entry}
            updatedEntry = cma.updateEntry(contentType, locale, body)
            if updatedEntry:
                config.logging.info('Entry {} in language {} updated to version {}'.format(entry['uid'], locale, updatedEntry['entry']['_version']))
            if publishEntries:
                cma.publishEntry(contentType, entry['uid'], environments, locales, locale, updatedEntry['entry']['_version'])

else:
    config.logging.warning('{}Search term {} returned 0 results.{}'.format(config.BOLD, searchString, config.END))       
        

if not updateContentstack:
    config.logging.info('Not updating Contentstack - Just FYI for testing purposes. Modify the "updateContentstack" variable in code to update entries.'