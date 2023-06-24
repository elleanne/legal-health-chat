import json

class UserQuery:
    query = ""
    num_docs = 10
    user_id = 0
    user_age = 13
    gender = 'f'
    state = ''
    from_city = ''
    from_country = ''
    # query_array = []

def get_user_q_dict(query_obj):
    return vars(query_obj)

def keyword_search(text):
    return []

def preprocess_query(req_values):
    ''' create the query object'''
    ut_obj = UserQuery()
    ut_obj.query = req_values.get('Body', None)
    # from_number = req_values.get('From', None)
    ut_obj.from_state = req_values.get('FromState', None)
    ut_obj.from_country = req_values.get('FromCountry', None)

    return f'{ut_obj.query} in {ut_obj.from_state}, {ut_obj.from_country}'