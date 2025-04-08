'''
Contentstack's Content Management API Python wrapper
https://www.contentstack.com/docs/developers/apis/content-management-api/
oskar.eiriksson@contentstack.com
2020-09-28

Environmental Variables needed:
 - CS_REGION = EU/NA (Europe/North-America)
 - CS_MANAGEMENTOKEN (Stack Management Token)
 - CS_APIKEY (Stack API Key)
 - CS_USERNAME (Only needed for some scripts - e.g. workflow related scripts)
 - CS_PASSWORD (Only needed for some scripts - e.g. workflow related scripts)
'''
import os
from sys import exit
from time import sleep
import requests
import config

regionMap = {
    'NA': 'https://api.contentstack.io/',
    'na': 'https://api.contentstack.io/',
    'EU': 'https://eu-api.contentstack.com/',
    'eu': 'https://eu-api.contentstack.com/'
}

try:
    region = regionMap[os.getenv('CS_REGION', None)]
except KeyError:
    config.logging.warning('{}No Region defined - Defaulting to North America.{}'.format(config.YELLOW, config.END))
    region = 'https://api.contentstack.io/'

managementToken = os.getenv('CS_MANAGEMENTOKEN', None)
if not managementToken:
    config.logging.critical('{}Management Token Missing as an Environment Variable. Exiting Script.{}'.format(config.RED, config.END))
    exit()

apiKey = os.getenv('CS_APIKEY', None)
if not apiKey:
    config.logging.critical('{}Stack API Key Missing as an Environment Variable. Exiting Script.{}'.format(config.RED, config.END))
    exit()

username = os.getenv('CS_USERNAME', None)
password = os.getenv('CS_PASSWORD', None)

def login():
    '''
    Login to get authtoken
    sample url: https://api.contentstack.io/v3/user-session
    '''
    if not username or not password:
        config.logging.warning('{}No user/password defined in environmental variables. Not possible to execute some parts of this script.{}'.format(config.YELLOW, config.END))
        return None
    body = {
	    'user': {
		    'email': username,
		    'password': password
	    }
    }
    url = '{}v3/user-session'.format(region)
    res = requests.post(url, headers={'Content-Type': 'application/json'}, json=body)
    if res.status_code in (200,201):
        config.logging.info('Login successful.')
        return res.json()['user']['authtoken']
    else:
        config.logging.error('{}{}{}'.format(config.RED, res.json()['error_message'], config.END))
        return None

if username and password:
    authToken = login()
    authTokenHeader = {
        'Content-Type': 'application/json',
        'authtoken': login(),
        'api_key': apiKey
    }
else:
    authTokenHeader = None

managementTokenHeader = {
    'authorization': managementToken,
    'api_key': apiKey
}

def logUrl(url):
    '''
    Logging out for debug purposes the constructed URL for any function
    '''
    config.logging.debug('-------')
    config.logging.debug('The CMA URL:')
    config.logging.debug(url)
    config.logging.debug('-------')


def logError(endpointName, name, url, res, msg='creating/updating'):
    config.logging.error('{}Failed {} {} (Name: {}){}'.format(config.RED, msg, endpointName, name, config.END))
    config.logging.error('{}URL: {}{}'.format(config.RED, url, config.END))
    config.logging.error('{}HTTP Status Code: {}{}'.format(config.RED, res.status_code, config.END))
    config.logging.error('{red}Error Message: {txt}{end}'.format(red=config.RED, txt=res.text, end=config.END))
    return None

def iterateURL(url, skip=0):
    return url + '&skip={}'.format(skip)

def typicalGetSimple(url, environment=None, branch="main"):
    '''
    Re-usable function to GET objects that never include more than 100 items
    '''
    if environment:
        url = url + '&environment={}'.format(environment)
    logUrl(url)
    managementTokenHeader['branch'] = branch
    res = requests.get(url, headers=managementTokenHeader)
    if res.status_code in (200, 201):
        config.logging.debug('Result: {}'.format(res.json()))
        return res.json()
    config.logging.error('{red}Export failed.{end}'.format(red=config.RED, end=config.END))
    config.logging.error('{}URL: {}{}'.format(config.RED, url, config.END))
    config.logging.error('{}HTTP Status Code: {}{}'.format(config.RED, res.status_code, config.END))
    config.logging.error('{red}Error Message: {txt}{end}'.format(red=config.RED, txt=res.text, end=config.END))
    return None

def typicalGetIterate(url, dictKey, environment=None, branch="main"):
    '''
    Re-usable function to GET objects that might have more than 100 items in it
    '''
    result = []
    skip = 0
    count = 1 # Just making sure we check at least once. Setting the real count value in while loop
    if environment:
        url = url + '&environment={}'.format(environment)
    logUrl(url)
    originalURL = url
    while skip <= count:
        url = iterateURL(originalURL, skip)
        logUrl(url)
        managementTokenHeader['branch'] = branch
        res = requests.get(url, headers=managementTokenHeader)
        if res.status_code in (200, 201):
            if 'count' in res.json(): # Did get a KeyError once... when there was nothing there.
                count = res.json()['count'] # Setting the real value of count here
            else:
                count = 0
            config.logging.debug('{}Response Now: {} {}'.format(config.YELLOW, res.json(), config.END))
            result = result + res.json()[dictKey]
            config.logging.debug('{}Result as of Now: {} {}'.format(config.YELLOW, result, config.END))
            skip += 100
        else:
            config.logging.error('{red}All {key} Export: Failed getting {key}{end}'.format(red=config.RED, key=dictKey, end=config.END))
            config.logging.error('{}URL: {}{}'.format(config.RED, url, config.END))
            config.logging.error('{}HTTP Status Code: {}{}'.format(config.RED, res.status_code, config.END))
            config.logging.error('{red}Error Message: {txt}{end}'.format(red=config.RED, txt=res.text, end=config.END))
            return None
    if result:
        return {dictKey: result, 'count': count}
    config.logging.info('No {} results'.format(dictKey))
    return None

def typicalUpdate(body, url, endpointName='', retry=False, msg='', branch="main"):
    '''
    Combining identical PUT methods into one
    '''
    logUrl(url)
    managementTokenHeader['branch'] = branch
    res = requests.put(url, headers=managementTokenHeader, json=body)
    if res.status_code in (200, 201):
        config.logging.info(str(endpointName) + ' ' + msg + ' updated')
        return res.json()
    elif (res.status_code == 429) and not retry:
        config.logging.warning('{}We are getting rate limited. Retrying in 2 seconds.{}'.format(config.YELLOW, config.END))
        sleep(2) # We'll retry once in a second if we're getting rate limited.
        return typicalUpdate(body, url, endpointName, True)
    config.logging.error('{}Failed updating {} - {}{}'.format(config.RED, endpointName, str(res.text), config.END))
    return logError(endpointName, '', url, res) # Empty string was name variable

def typicalCreate(body, url, endpointName='', retry=False, msg='created', token='mgmt', branch="main"):
    '''
    Combining identical POST methods into one

    - If token == mgmt -> It uses the Management Token
    - If token == auth -> It uses the Auth Token

    '''
    logUrl(url)
    if token == 'auth':
        headers = authTokenHeader
        if not headers:
            config.logging.critical('{}Credentials not defined - Exiting request{}'.format(config.RED, config.END))
            return None
    else:
        headers = managementTokenHeader
    headers['branch'] = branch
    res = requests.post(url, headers=headers, json=body)
    if res.status_code in (200, 201):
        config.logging.info(str(endpointName) + ' ' + msg)
        return res.json()
    elif (res.status_code == 429) and not retry:
        config.logging.warning('{}We are getting rate limited. Retrying in 2 seconds.{}'.format(config.YELLOW, config.END))
        sleep(2) # We'll retry once in a second if we're getting rate limited.
        return typicalCreate(body, url, endpointName, True, msg, token)
    config.logging.error('{}Failed {} {} - {}{}'.format(config.RED, msg, endpointName, str(res.text), config.END))
    return logError(endpointName, '', url, res) # Empty string was name variable

def typicalDelete(url, endpointName='', retry=False, branch="main"):
    '''
    Combining identical DELETE methods into one
    '''
    logUrl(url)
    managementTokenHeader['branch'] = branch
    res = requests.delete(url, headers=managementTokenHeader)
    if res.status_code in (200, 201):
        config.logging.info(str(endpointName) + ' deleted')
        return res.json()
    elif (res.status_code == 429) and not retry:
        config.logging.warning('{}We are getting rate limited. Retrying in 2 seconds.{}'.format(config.YELLOW, config.END))
        sleep(2) # We'll retry once in a second if we're getting rate limited.
        return typicalDelete(url, endpointName, True)
    config.logging.error('{}Failed delete {} - {}{}'.format(config.RED, endpointName, str(res.text), config.END))
    return logError(endpointName, '', url, res) # Empty string was name variabl

def getAllLanguages(branch="main"):
    '''
    Gets all languages
    sample url: https://api.contentstack.io/v3/locales?include_count={boolean_value}
    '''
    url = '{region}v3/locales?include_count=true'.format(region=region)
    return typicalGetIterate(url, 'locales', branch)

def getAllEnvironments(apiKey, token, region):
    '''
    Gets all environments
    sample url: https://api.contentstack.io/v3/environments?include_count={boolean_value}&asc={field_uid}&desc={field_uid}
    '''
    url = '{region}v3/environments?include_count=true'.format(region=region)
    return typicalGetIterate(url, 'environments', branch)

def getAllEntries(contentType, locale, environment=None, query=None, branch="main"):
    '''
    Gets all entries
    sample url: https://api.contentstack.io/v3/content_types/{content_type_uid}/entries?locale={language_code}&include_workflow={boolean_value}&include_publish_details={boolean_value}
    if environment:
        fetches only entries published in that environment
    if query:
        finds entries based on that query
    '''
    url = '{region}v3/content_types/{contentType}/entries?locale={locale}&include_workflow=true&include_publish_details=true&include_count=true'.format(region=region, contentType=contentType, locale=locale)
    if query:
        url = url + '&query={}'.format(query)
    return typicalGetIterate(url, 'entries', environment, branch)

def getSingleEntry(contentType, locale, uid, version=None, branch="main"):
    '''
    Gets a single entry
    sample url: https://api.contentstack.io/v3/content_types/{content_type_uid}/entries/{entry_uid}?version={version_number}&locale={language_code}&include_workflow={boolean_value}&include_publish_details={boolean_value}
    '''
    url = '{region}v3/content_types/{contentType}/entries/{uid}?locale={locale}&include_workflow=true&include_publish_details=true'.format(region=region, contentType=contentType, uid=uid, locale=locale)
    if version:
        url = url + '&version={}'.format(version)
    return typicalGetSimple(url, branch)

def getEntryLanguages(contentType, uid, branch="main"):
    '''
    Knowing where the entry has been localised
    sample url: https://api.contentstack.io/v3/content_types/{content_type_uid}/entries/{entry_uid}/locales
    '''
    url = '{region}v3/content_types/{contentType}/entries/{uid}/locales'.format(region=region, contentType=contentType, uid=uid)
    return typicalGetSimple(url, None, branch)

def getAllContentTypes(branch="main"):
    '''
    Gets all content types
    sample url: https://api.contentstack.io/v3/content_types?include_count={boolean_value}&include_global_field_schema={boolean_value}
    '''
    url = '{}v3/content_types?include_count=true&include_global_field_schema=true'.format(region)
    return typicalGetIterate(url, 'content_types', branch)


def getSingleContentType(contentType, version=None, branch="main"):
    '''
    Gets a single content type
    sample url: https://api.contentstack.io/v3/content_types/{content_type_uid}?version={content_type_version}
    '''
    url = '{region}v3/content_types/{contentType}'.format(region=region, contentType=contentType)
    if version:
        url = url + '?version={}'.format(version)
    return typicalGetSimple(url, branch)

def deleteEntry(contentType, locale, uid, deleteLocalized, branch="main"):
    '''
    Deletes an entry
    sample url: https://api.contentstack.io/v3/content_types/{content_type_uid}/entries/{entry_uid}?locale={locale_code}&delete_all_localized={boolean_value}
    '''
    url = '{region}v3/content_types/{contentType}/entries/{uid}?locale={locale}&delete_all_localized={deleteLocalized}'.format(region=region, contentType=contentType, uid=uid, locale=locale, deleteLocalized=str(deleteLocalized).lower())
    return typicalDelete(url, 'entry', branch)

def createEntry(contentType, locale, body, branch="main"):
    '''
    Creates an Entry
    sample url: https://api.contentstack.io/v3/content_types/{content_type_uid}/entries?locale={locale_code}
    '''
    url = '{region}v3/content_types/{contentType}/entries?locale={locale}'.format(region=region, contentType=contentType, locale=locale)
    return typicalCreate(body, url, 'Entry', branch)

def updateEntry(contentType, locale, body, branch="main"):
    '''
    Updates an entry
    sample url: https://api.contentstack.io/v3/content_types/{content_type_uid}/entries/{entry_uid}?locale={locale_code}
    '''
    uid = body['entry']['uid']
    url = '{region}v3/content_types/{contentType}/entries/{uid}?locale={locale}'.format(region=region, contentType=contentType, uid=uid, locale=locale)
    return typicalUpdate(body, url, 'entry', False, uid  + ' - ' + locale, branch)

def publishEntry(contentType, uid, environments, locales, locale, version=None, branch="main"):
    '''
    Publishes an entry
    sample url: https://api.contentstack.io/v3/content_types/{content_type_uid}/entries/{entry_uid}/publish
    '''
    url = '{region}v3/content_types/{contentType}/entries/{uid}/publish'.format(region=region, contentType=contentType, uid=uid)
    body = {
        'entry': {
            'environments': environments,
            'locales': locales
        },
        'locale': locale
    }
    if version:
        body['version'] = version
    return typicalCreate(body, url, 'entry', False, uid + ' - ' + locale + ' published', branch)
    
def createContentType(body, branch="main"):
    '''
    Creates a content type
    sample url: https://api.contentstack.io/v3/content_types
    '''
    url = '{}v3/content_types'.format(region)
    return typicalCreate(body, url, 'content_type', branch)

def updateContentType(body, contentType, branch="main"):
    '''
    Updates a content type
    sample url: https://api.contentstack.io/v3/content_types/{content_type_uid}
    '''
    url = '{}v3/content_types/{}'.format(region, contentType)
    return typicalUpdate(body, url, 'content_type', branch)

def setWorkflowStage(contentType, uid, locale, workflow, assignUsers=[], assignRoles=[], notify=False, branch="main"):
    '''
    Moves an entry to a certain workflow stage
    sample url: https://api.contentstack.io/v3/content_types/{{content_type_uid}}/entries/{{entry_uid}}/workflow?locale={locale_code}
    '''
    url = '{}v3/content_types/{}/entries/{}/workflow?locale={}'.format(region, contentType, uid, locale)
    body = {
	"workflow": {
		"workflow_stage": {
			"notify": notify,
			"uid": workflow,
			"assigned_to": assignUsers,
			"assigned_by_roles": assignRoles		
		    }
	    }
    }
    return typicalCreate(body, url, 'workflow', False, 'updated', 'auth', branch) # This is using the 'auth' -> AuthToken

