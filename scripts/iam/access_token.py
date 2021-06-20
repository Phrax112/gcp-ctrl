
"""
Login script to grab the access token for a service account for a project.

"""

import requests

METADATA_URL = 'http://metadata.google.internal/computeMetadata/v1/'
METADATA_HEADERS = {'Metadata-Flavor': 'Google'}
SERVICE_ACCOUNT = 'default'

def get_access_token():
    url = '{}instance/service-accounts/{}/token'.format(METADATA_URL, SERVICE_ACCOUNT)
    # Request an access token from the metadata server.
    r = requests.get(url, headers=METADATA_HEADERS)
    r.raise_for_status()
    # Extract the access token from the response.
    access_token = r.json()['access_token']
    return access_token
