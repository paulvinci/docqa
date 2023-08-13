# Bring in deps
from http.client import responses
import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from streamlit_text_rating.st_text_rater import st_text_rater
from streamlit_star_rating import st_star_rating
import time
import os
import requests
from langchain.document_loaders import TextLoader, Docx2txtLoader
from langchain.vectorstores import FAISS
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import PromptTemplate
import pandas as pd
import gspread 
from oauth2client.service_account import ServiceAccountCredentials
import pygsheets
import json
import toml


# Customize the layout
st.set_page_config(page_title="RuLLM", page_icon="👑", layout="wide") 
st.markdown(f"""
            <style>
            .stApp {{background-image: url("https://images.unsplash.com/photo-1691466065738-1abe6adbbdd5?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1887&q=80"); 
                     background-attachment: fixed;
                     background-size: cover}}
         </style>
         """, unsafe_allow_html=True)

def stream_example(response_text):
    for word in response_text.split():
        yield word + " "
        time.sleep(0.1)

@st.cache_data
def llm_inference(url):
    tic = time.perf_counter()
    response = requests.get(url)
    toc = time.perf_counter()
    exec_time = time.strftime("%M:%S", time.gmtime(toc - tic))
    return response, exec_time

# Query through LLM    
ngrok_url = "https://58f8-2001-861-3f45-8770-cd70-35a3-852-5b94.ngrok-free.app"
question = st.text_input("Ask something from the files provided as context")    
if question:
    url = f'{ngrok_url}/search?query={question}'
    response, exec_time = llm_inference(url)
    st.info(response.text)
    st.write(f'Execution time: {exec_time} minutes')
 
# Google Sheets
## Loading
spreadsheet_key = "1lvIK4MoqqRLeIFe4XstOF8GKxpuuB9mFeauMho6jgjw"
scope = "https://spreadsheets.google.com/feeds"
credentials_json = json.loads(json.dumps(toml.loads(open('./rullama_rd_data.toml').read())))
credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_json, scope)
worksheet = gspread.authorize(credentials).open_by_key(spreadsheet_key).worksheet("Feuille 1")
data = worksheet.get_all_values()
headers = data.pop(0)
df = pd.DataFrame(data, columns=headers)
## Updating
gc = pygsheets.authorize(service_file='./rullama_rd_data.json')
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1lvIK4MoqqRLeIFe4XstOF8GKxpuuB9mFeauMho6jgjw/edit#gid=0')
wks = sh[0]

if question:
    if response:
        evaluation = st_star_rating(label="Please rate the relevance of the answer", maxValue=5, defaultValue=3, key="rating")
        st.write(evaluation)
        if evaluation:
            temp = pd.DataFrame({'question':[question],'response':[response.text],'evaluation':[evaluation]})
            new_df = pd.concat([df,temp])[['question','response','evaluation']]
            wks.set_dataframe(new_df, 'A1')
        else:
            pass
    