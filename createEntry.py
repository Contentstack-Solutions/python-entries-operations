'''
Creates an entry.

To determine how the body should look like, it could be clever to run the getAllContentTypes.py or getSingleEntry.py first

oskar.eiriksson@contentstack.com

'''

import cma

contentType = 'landing_page'
locale = 'en-us'
body = {
    'entry': {
        'title': 'Well Hello!!'
    }
}

cma.createEntry(contentType, locale, body)