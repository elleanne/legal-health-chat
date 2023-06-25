import json
locations = {'ca':'usa_ca', 'us':'usa_code', 'usa':'usa_code', 'usf':'usa_cfr'}
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

def preprocess_query(req_values):
    ''' create the query object'''
    ut_obj = UserQuery()
    ut_obj.query = req_values.get('Body', None)
    ut_obj.from_state = req_values.get('FromState', None).lower()
    ut_obj.from_country = req_values.get('FromCountry', None)


    return ut_obj

def get_query_str(ut_obj, get_state=False):
    if get_state and ut_obj.from_state in  ['ca', 'california']:
        return f'{ut_obj.query} in {ut_obj.from_state}, {ut_obj.from_country}'
    return str(ut_obj.query)

def get_legislation_code(ut_obj, get_state=False):
    if get_state and ut_obj.from_state in  ['ca', 'california']:
        return locations.get(ut_obj)
    return locations.get('usa')