import os
import openai
import requests
import json

from preprocess.query import get_legislation_code, get_query_str

api_key = os.getenv("OPENAI_API_KEY", "")
if api_key != "":
    openai.api_key = api_key
else:
    print("Warning: OPENAI_API_KEY is not set")
       
# number of most relevant legal documents
n_best = 10

def query_chat_gpt(msg):
    return openai.ChatCompletion.create(
      model="gpt-4-0613",
      messages=msg,
      temperature=0,
      max_tokens=1000
    )

def get_response(sent, n):
    # get docs to pass to GPT 
    if check_is_legal_question(get_query_str(sent)):
        docs = getRelevantDocs(reformat_user_query(get_query_str(sent)), get_legislation_code(sent),n)
        # query GPT
        sent_str = f'{get_query_str(sent, get_state=True)}. Keep it short and simple.'
        return generate_legal_answer(sent_str, docs)
    return 'You must ask a valid legal question.'

def check_is_legal_question(text):
    msg=[
          {"role": "system", "content": '''Test whether this query is serious or just a joke. If it is serious, answer 'yes'. 
           Otherwise, answer 'no'. Always answer yes or no, do not answer anything else'''}, 
          {"role": "user", "content": text}
    ]
    
    # send query to GPT
    response = query_chat_gpt(msg)
    res_bool = response.choices[0]['message']['content']

    if 'yes' in res_bool.lower():
        return True

    return False

def getRelevantDocs(sentence, legislation_code, n):
    # find n most relevant legal documents that are relevant to `sentence`  
    # returns those documents in a list from a secondary API

    base_url = 'http://lawapi.xyz/query'
    query_json = json.dumps({
        'n': n,
        'query': sentence,
        "legislation" : legislation_code
    })
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.post(base_url, data=query_json, headers=headers)
    if response.status_code > 299:
        print('http error')
    
    unicode_string = response.content.decode('utf-8')
    json_data = json.loads(unicode_string)
    
    return [r['t'] for r in json_data]

def reformat_user_query(sentence):
    msg=[
          {"role": "system", "content": '''User ask legal question. Determine what information should be check in the law to
            be check in the law to answer it. output it in the form of a series of questions'''},
          {"role": "user", "content": sentence}
    ]
    # send query to GPT
    response = query_chat_gpt(msg)

    # return answer
    return response.choices[0]['message']['content']

def generate_legal_answer(inquiry, documents):
    # documents: a list of documents
    
    # set up full query
    input_str = "Legal question: \n" + inquiry + "\n\n"
    doc_str =''
    ind = 1
    for d in documents:
        doc_str += "\n\n\n" + str(ind) + ":\n"
        doc_str += d + "\n\n"
        
        ind += 1
        
    msg=[
          {"role": "system", "content": '''You are a lawyer. The user will ask a legal question and provide several relevant legal documents for your reference.
           Based on the user's question, you should search for relevant information in the legal documents that help answer it, and provide an answer that is 
           supported by the information in the legal documents. The answer needs to be within 150 words. Do not mention that you used supporting documents, 
           but, if possible, mention the section of the law that you used to build your answer. '''+ doc_str},
          {"role": "user", "content": input_str}
    ]
    
    # send query to GPT
    response = query_chat_gpt(msg)

    # return answer
    return response.choices[0]['message']['content']