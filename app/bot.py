from streamlit_chat import message
import streamlit as st
import openai
import os
import json
st.balloons()

# Set up OpenAI API key
openai.api_type = "azure"
openai.api_base = "https://aks-production.openai.azure.com/"
# openai.api_base=  "https://biotest123.openai.azure.com/"
openai.api_version = "2023-03-15-preview"
openai.api_key = os.getenv("KEY_AZURE_AI")
data = {"questions": 0, "answers": 0}



def write_results(data):
    
    _data = json_loader(loc="results.json")
    _data["questions"] += data["questions"]
    _data["answers"] += data["answers"]

    json.dump(_data, open("results.json", "w"))
    

def json_loader(loc='agenda.json'):
    json_file = open(loc)
    return json.load(json_file)


def generate_gpt_chat(prompt,model='gpt3',max_tokens=4000):
    bot_context = f"you are geektime event agent ,event date is 12.6.23 in pavilion 10 expo tel aviv,this is event json agenda:{json_loader()}. \
                   you are friendly and concise. \
                   you only provide factual answers to queries, and do not provide answers that are not related to geekime event ."
                   
    response = openai.ChatCompletion.create(
        # engine=model,
        engine="gpt3",
        messages=[{"role":"system","content":bot_context},
                  {"role":"user","content":prompt}
                  ],
        temperature=1,
        max_tokens=max_tokens,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    return str(response['choices'][0]['message']['content'])

st.title("Geektime Event Chatbot")
st.markdown("This is a chatbot that can answer questions about the event agenda")


data["questions"] += 1
write_results(data)
data["answers"] += 1
write_results(data)

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
user_input=st.text_input("You:",key='input')
if user_input:
    data["questions"] += 1
    write_results(data)
    
    output=generate_gpt_chat(prompt=user_input)
    data["answers"] += 1
    write_results(data)
    #store the output
    st.session_state['past'].append(user_input)
    st.session_state['generated'].append(output)
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user') 
        


