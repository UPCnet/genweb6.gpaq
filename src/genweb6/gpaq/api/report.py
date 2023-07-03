# -*- coding: utf-8 -*-
from genweb6.gpaq.api import token

import requests
import json


def get_embed_params_for_single_report(workspace_id, report_id):
  report_url = 'https://api.powerbi.com/v1.0/myorg/groups/' + workspace_id + '/reports/' + report_id
  api_response = requests.get(report_url, headers={
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token.get_access_token()
  })

  if api_response.status_code != 200:
    return None

  api_response = json.loads(api_response.text)
  return api_response['embedUrl']