import requests
import json


base_url = 'http://lawapi.xyz/ask/'

def get_json(data_dict):
    return json.dumps(data_dict)

def api_req(query_dict):
    ''' make the request to the lawapi to get the documents to pass to GPT'''
    res_docs = requests.get(base_url, json=query_dict)
    return res_docs