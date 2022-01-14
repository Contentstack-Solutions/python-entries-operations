'''
Gets the newest version of a content type. Grabs the version and fetches the content type again (current version - 1).

Finally updates the content type with that prior version - that is, creates a new version identical to that older one.

So it reverts the last change.

oskar.eiriksson@contentstack.com

2021-04-12

'''
import cma
import config

contentType = 'landing_page'

contentTypeObjLatest = cma.getSingleContentType(contentType)


if contentTypeObjLatest:
    contentTypeObjLatest = contentTypeObjLatest['content_type']
    newestVersion = contentTypeObjLatest['_version']
    config.logging.info('Newest version of content type {}: {}.'.format(contentType, newestVersion))
    config.logging.info('Reverting {} to prior version: {}.'.format(contentType, newestVersion-1))
    contentTypeObjOlder = cma.getSingleContentType(contentType, newestVersion-1)
    update = cma.updateContentType(contentTypeObjOlder, contentType)
    if update:
        config.logging.info('Updated {} to new version {}, identical to version {}.'.format(contentType, newestVersion+1, newestVersion-1))