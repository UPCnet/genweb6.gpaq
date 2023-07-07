# -*- coding: utf-8 -*-
from genweb6.gpaq.models.embedconfig import EmbedConfig
from genweb6.gpaq.models.embedtoken import EmbedToken
from genweb6.gpaq.models.embedtokenrequestbody import EmbedTokenRequestBody
from genweb6.gpaq.models.reportconfig import ReportConfig

from genweb6.gpaq.api import token

import requests
import json


def get_embed_params_for_single_report(workspace_id, report_id):
  report_url = 'https://api.powerbi.com/v1.0/myorg/groups/' + workspace_id + '/reports/' + report_id
  api_response = requests.get(report_url, headers=get_request_header())

  if api_response.status_code != 200:
    return None

  api_response = json.loads(api_response.text)
  report = ReportConfig(api_response['id'], api_response['name'], api_response['embedUrl'])
  dataset_ids = [api_response['datasetId']]

  embed_token = get_embed_token_for_single_report_single_workspace(report_id, dataset_ids)
  embed_config = EmbedConfig(embed_token.tokenId, embed_token.token, embed_token.tokenExpiry, [report.__dict__])
  return json.dumps(embed_config.__dict__)


def get_embed_token_for_single_report_single_workspace(report_id, dataset_ids):
    request_body = EmbedTokenRequestBody()

    for dataset_id in dataset_ids:
        request_body.datasets.append({'id': dataset_id})

    request_body.reports.append({'id': report_id})

    embed_token_api = 'https://api.powerbi.com/v1.0/myorg/GenerateToken'
    api_response = requests.post(embed_token_api, data=json.dumps(request_body.__dict__), headers=get_request_header())

    if api_response.status_code != 200:
        return None

    api_response = json.loads(api_response.text)
    embed_token = EmbedToken(api_response['tokenId'], api_response['token'], api_response['expiration'])
    return embed_token


def get_request_header():
  return {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token.get_access_token()
  }