import json

class UserQuery:
    query = ""
    # query_array = []
    num_docs = 10

def get_user_q_dict(query_obj):
    return dict(query_obj)

def keyword_search(text):
    return []

def preprocess_query(text):
    ut_obj = UserQuery()
    ut_obj.query = text
    # ut_obj.query_array = keyword_search(text)
    ## set num docs ??
    
    return get_user_q_dict(ut_obj)