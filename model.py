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

def get_response(sent, n):
    docs = getRelevantDocs(sent,n)
    sent = f'{sent}. Explain with an eigth grade reading comprehension. Keep is short and simple.'

    return generate_legal_answer(sent, docs)

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


def find_math_sentences(text):
    # returns a list a sentences having numbers and math concepts

    msg=[
        {"role": "system", "content": "Given the text, identify sentences that contain numbers, math expressions, or math concepts. Store those sentences in a Python list and return the list."},
        {"role": "user", "content": ""},
        {"role": "assistant", "content": "Given the text, identify sentences that contain numbers, math expressions, or math concepts. Store those sentences in a Python list and return the list."},
        {"role": "user", "content": text}
    ]

    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=msg,
      temperature=0
    )


    return response.choices[0]['message']['content']






def get_math_questions(text):
    msg=[
        {"role": "system", "content": "Given the text, identify sentences that contain numbers, math expressions, or math concepts. Store those sentences in a Python list and return the list."},
        {"role": "user", "content": ""},
        {"role": "assistant", "content": "Given the text, identify sentences that contain numbers, math expressions, or math concepts. Store those sentences in a Python list and return the list."},
        {"role": "user", "content": text}
    ]

def get_highlight_location(text):
    example_text = 'Congress shall be in session on the sixth day of January succeeding every meeting of the electors. The Senate and House of Representatives shall meet in the Hall of the House of Representatives at the hour of 1 o’clock in the afternoon on that day, and the President of the Senate shall be their presiding officer. Two tellers shall be previously appointed on the part of the Senate and two on the part of the House of Representatives, to whom shall be handed, as they are opened by the President of the Senate, all the certificates and papers purporting to be certificates of the electoral votes, which certificates and papers shall be opened, presented, and acted upon in the alphabetical order of the States, beginning with the letter A; and said tellers, having then read the same in the presence and hearing of the two Houses, shall make a list of the votes as they shall appear from the said certificates; and the votes having been ascertained and counted according to the rules in this subchapter provided, the result of the same shall be delivered to the President of the Senate, who shall thereupon announce the state of the vote, which announcement shall be deemed a sufficient declaration of the persons, if any, elected President and Vice President of the United States, and, together with a list of the votes, be entered on the Journals of the two Houses. Upon such reading of any such certificate or paper, the President of the Senate shall call for objections, if any. Every objection shall be made in writing, and shall state clearly and concisely, and without argument, the ground thereof, and shall be signed by at least one Senator and one Member of the House of Representatives before the same shall be received. When all objections so made to any vote or paper from a State shall have been received and read, the Senate shall thereupon withdraw, and such objections shall be submitted to the Senate for its decision; and the Speaker of the House of Representatives shall, in like manner, submit such objections to the House of Representatives for its decision; and no electoral vote or votes from any State which shall have been regularly given by electors whose appointment has been lawfully certified to according to section 6 of this title from which but one return has been received shall be rejected, but the two Houses concurrently may reject the vote or votes when they agree that such vote or votes have not been so regularly given by electors whose appointment has been so certified. If more than one return or paper purporting to be a return from a State shall have been received by the President of the Senate, those votes, and those only, shall be counted which shall have been regularly given by the electors who are shown by the determination mentioned in section 5 of this title to have been appointed, if the determination in said section provided for shall have been made, or by such successors or substitutes, in case of a vacancy in the board of electors so ascertained, as have been appointed to fill such vacancy in the mode provided by the laws of the State; but in case there shall arise the question which of two or more of such State authorities determining what electors have been appointed, as mentioned in section 5 of this title , is the lawful tribunal of such State, the votes regularly given of those electors, and those only, of such State shall be counted whose title as electors the two Houses, acting separately, shall concurrently decide is supported by the decision of such State so authorized by its law; and in such case of more than one return or paper purporting to be a return from a State, if there shall have been no such determination of the question in the State aforesaid, then those votes, and those only, shall be counted which the two Houses shall concurrently decide were cast by lawful electors appointed in accordance with the laws of the State, unless the two Houses, acting separately, shall concurrently decide such votes not to be the lawful votes of the legally appointed electors of such State. But if the two Houses shall disagree in respect of the counting of such votes, then, and in that case, the votes of the electors whose appointment shall have been certified by the executive of the State, under the seal thereof, shall be counted. When the two Houses have voted, they shall immediately again meet, and the presiding officer shall then announce the decision of the questions submitted. No votes or papers from any other State shall be acted upon until the objections previously made to the votes or papers from any State shall have been finally disposed of.'
    msg=[
        {"role": "system", "content": "Given the input text, find the sentence that has the most legal implications. Return a tuple containing two numbers separated by a comma. The first number is the starting index of that number, and the second number is the ending index of that number."},
        {"role": "user", "content": example_text},
        {"role": "assistant", "content": "151,256"},
        {"role": "user", "content": text}
    ]

    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=msg,
      temperature=0.5
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
inquiry = "I am a pregnant 25-year-old woman. I have to take a surgery. What is the information I need to know regarding health insurance?"
doc_list = getRelevantDocs(inquiry, n_best)
print(generate_legal_answer(inquiry, doc_list))


