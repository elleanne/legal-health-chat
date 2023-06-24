import requests
import json


base_url = 'http://lawapi.xyz/ask/2/'

def get_json(data_dict):
    return json.dumps(data_dict)

def api_req(query_dict):
    
    res_docs = requests.get(base_url, json=query_dict)
    
    return