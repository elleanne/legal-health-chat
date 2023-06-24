import os
import openai
import requests
import json

api_key = os.getenv("OPENAI_API_KEY", "")
if api_key != "":
    openai.api_key = api_key
else:
    print("Warning: OPENAI_API_KEY is not set")
       
# number of most relevant legal documents
n_best = 10



def getRelevantDocs(sentence, n):
    # find n most relevant legal documents that are relevant to `sentence`  
    # returns those documents in a list

    base_url = 'http://lawapi.xyz/query'
    query_json = json.dumps({
        'n': n,
        'query': sentence
    })
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.post(base_url, data=query_json, headers=headers)
    if response.status_code != 200:
        print('http error')
    
    unicode_string = response.content.decode('utf-8')
    json_data = json.loads(unicode_string)
    
    return [r['t'] for r in json_data]
    


def generate_legal_answer(inquiry, documents):
    # documents: a list of documents
    
    input_str = "Legal question: \n" + inquiry + "\n\n"
    
    ind = 1
    for d in documents:
        input_str += "Supporting document " + str(ind) + ":\n"
        input_str += d + "\n\n"
        
        ind += 1
        
    
    msg=[
          {"role": "system", "content": "You are a lawyer. The user will ask a legal question and provide several relevant legal documents for your reference. Based on the user's question, you should search for relevant information in the legal documents that help answer it, and provide an answer that is supported by the information in the legal documents. The answer needs to be within 150 words."},
          {"role": "user", "content": input_str}
    ]
    
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=msg,
      temperature=0
    )


    return response.choices[0]['message']['content']


########################
# example
########################
inquiry = "I am a pregnant 25-year-old woman. I am in jail because of theft. What are my rights?"
doc_list = getRelevantDocs(inquiry, n_best)
print(generate_legal_answer(inquiry, doc_list))
'''
As a pregnant woman in jail, you have certain rights. Under § 4051 of Chapter 303 of Title 18, a covered institution may not place a pregnant prisoner or a prisoner in post-partum recovery in a segregated housing unit unless the prisoner presents an immediate risk to herself or others. The placement should be limited and temporary. This means that you have the right not to be placed in restricted housing unless you are a risk to yourself or others. Additionally, under § 4322 of Chapter 317, restraints cannot be used on a prisoner during the period of pregnancy, labor, and post-partum recovery. This restriction begins after your pregnancy has been confirmed by healthcare professionals and lasts until post-partum recovery. Furthermore, under § 3596 of Chapter 228, a death sentence cannot be carried out upon a woman while she is pregnant. Finally, under § 1841 of Chapter 90A, nothing in this section shall be construed to permit the prosecution of any woman concerning her unborn child. Therefore, you have the right to proper medical attention during this period of your life, which extends to healthcare provided in a community confinement facility where you have access to necessary medical care, mental health care, and medicine in partnership with local health service providers, as per § 3621(i) of Chapter 229.
'''

