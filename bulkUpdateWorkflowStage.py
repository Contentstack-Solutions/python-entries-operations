'''
To bulk update the workflow stage on a defined set of entries - Using queries.
See more on queries here: https://www.contentstack.com/docs/developers/apis/content-delivery-api/#queries

oskar.eiriksson@contentstack.com
2022-01-17

Needs the CS_USERNAME and CS_PASSWORD environmental variables to be defined in addition to the variables mentioned in README

Approaches finding entries are the following:
1. All entries of one or more content type in one or more language.
2. All entries of one or more content type in one or more language that are currently in a defined workflow stage.
3. All entries of one or more content type in one or more language that are published to a defined environment
4. All entries of one or more content type in one or more language based on a search query.

'''

import cma
import config

contentTypes = ['landing_page'] # What content types are you looking at. One or more - Needs to be an array.
locales = ['is-is'] # What languages are you looking at. One or more - Needs to be an array.
workflowStage = 'blta0494129443f9b46'  # The UID of workflow stage you plan to move all the entries to.

'''
See Below Approaches 1 to 4 - Comment out the approaches you don't want to test.
'''

'''
 -> 1. All entries of a certain content type(s) and language(s).
'''
entriesArr = []
for contentType in contentTypes:
    for locale in locales:
        query = '{"locale": "' + locale + '"}'
        entries = cma.getAllEntries(contentType, locale, None, query)
        if entries:
            entriesArr = entriesArr + entries['entries']

for entry in entriesArr:
    res = cma.setWorkflowStage(contentType, entry['uid'], locale, workflowStage)
    config.logging.info('{contentType} - {title} ({uid}) in language: {locale} - Response from Contentstack: {res}'.format(contentType=contentType, title=entry['title'], uid=entry['uid'], locale=locale, res=res))

'''
 -> 2. All entries of a certain content type(s) and language(s) that are currently in a defined workflow stage
'''

# entriesArr = []
# workflowStageQueryUid = 'blta0494129443f9b46' # The UID of the workflow we want to query all entries from
# for contentType in contentTypes:
#     for locale in locales:
#         query = '{"$and":[{"locale": "' + locale  + '"},{"_workflow.uid": "' + workflowStageQueryUid + '"}]}'
#         entries = cma.getAllEntries(contentType, locale, None, query)
#         if entries:
#             entriesArr = entriesArr + entries['entries']
# for entry in entriesArr:
#     res = cma.setWorkflowStage(contentType, entry['uid'], locale, workflowStage)
#     config.logging.info('{contentType} - {title} ({uid}) in language: {locale} - Response from Contentstack: {res}'.format(contentType=contentType, title=entry['title'], uid=entry['uid'], locale=locale, res=res))

'''
-> 3. All entries of a certain content type(s) and language(s) that are published to a defined environment
'''
# entriesArr = []
# environment = 'development' # The name of the environment
# for contentType in contentTypes:
#     for locale in locales:
#         query = '{"locale": "' + locale + '"}'
#         entries = cma.getAllEntries(contentType, locale, environment, query)
#         if entries:
#             entriesArr = entriesArr + entries['entries']
# for entry in entriesArr:
#     res = cma.setWorkflowStage(contentType, entry['uid'], locale, workflowStage)
#     config.logging.info('{contentType} - {title} ({uid}) in language: {locale} - Response from Contentstack: {res}'.format(contentType=contentType, title=entry['title'], uid=entry['uid'], locale=locale, res=res))

'''
-> 4. All entries of a certain content type(s) and language(s) based on a search query
'''
# entriesArr = []
# for contentType in contentTypes:
#     for locale in locales:
#         query = '{"$and":[{"locale": "' + locale  + '"},{"title": "Prófa!!!!"}]}'
#         entries = cma.getAllEntries(contentType, locale, None, query)
#         if entries:
#             entriesArr = entriesArr + entries['entries']
# for entry in entriesArr:
#     res = cma.setWorkflowStage(contentType, entry['uid'], locale, workflowStage)
#     config.logging.info('{contentType} - {title} ({uid}) in language: {locale} - Response from Contentstack: {res}'.format(contentType=contentType, title=entry['title'], uid=entry['uid'], locale=locale, res=res))