# -*- coding: utf-8 -*-
from genweb6.gpaq.api import AUTHORITY_URL
from genweb6.gpaq.api import SCOPE_BASE
from genweb6.gpaq.utils import genwebGpaqConfig

import msal


def get_access_token():
  response = None
  gpaq_config = genwebGpaqConfig()

  try:
    authority = AUTHORITY_URL.replace('organizations', gpaq_config.tenant_id)

    clientapp = msal.ConfidentialClientApplication(
      gpaq_config.client_id,
      client_credential=gpaq_config.client_secret,
      authority=authority)

    response = clientapp.acquire_token_for_client(scopes=SCOPE_BASE)

    try:
      return response['access_token']
    except KeyError:
      raise Exception(response['error_description'])

  except Exception as ex:
    raise Exception('Error retrieving Access token\n' + str(ex))
