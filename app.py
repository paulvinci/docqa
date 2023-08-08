# Bring in deps
import streamlit as st 
import time
import os
from langchain.document_loaders import TextLoader, Docx2txtLoader
from langchain.vectorstores import Chroma, FAISS
from langchain.chains import LLMChain
from langchain.llms import LlamaCpp
from langchain.embeddings import LlamaCppEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import PromptTemplate


# Customize the layout
st.set_page_config(page_title="DOCAI", page_icon="🤖", layout="wide")     
st.markdown(f"""
            <style>
            .stApp {{background-image: url("https://images.unsplash.com/photo-1682685797366-715d29e33f9d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDF8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=870&q=80"); 
                     background-attachment: fixed;
                     background-size: cover}}
         </style>
         """, unsafe_allow_html=True)

# Initialize model, vector stores
# Import LLM
path = './models/llama-2-7b-chat.ggmlv3.q2_K.bin'
llm = LlamaCpp(model_path=path, num_output=500, verbose=True, n_ctx=3000)
embeddings = LlamaCppEmbeddings(model_path=path)

# Load Vector Stores
path_vectorstores='./vectorstores/faiss/'
db = FAISS.load_local(path_vectorstores, embeddings)

# Craft a prompt template that works best for your LLM
prompt_template = """
[INST] <<SYS>>
Use the following pieces of information to answer the user's question.
Please ensure that your responses are socially unbiased and positive in nature.
If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
<</SYS>>
Context: {context}
Question: {question}
Only return the helpful answer below and nothing else.
Helpful answer: [/INST]"""

# Context will be the similar doc and question will be the query
prompt = PromptTemplate.from_template(prompt_template)

# Use LLM to generate answer from the context
query_llm = LLMChain(llm=llm,prompt=prompt)

# Query through LLM    
question = st.text_input("Ask something from the file")    
if question:
    tic = time.perf_counter()
    similar_doc = db.similarity_search(question,k=4)
    context = ''.join([t.page_content for t in similar_doc])
    response = query_llm.run({'context':context,'question':question})
    toc = time.perf_counter()
    exec_time = time.strftime("%M:%S", time.gmtime(toc - tic))
    st.write(response)
    st.write(f'Execution time: {exec_time} minutes')