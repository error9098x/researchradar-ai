from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
import requests
from langchain.chains.question_answering import load_qa_chain
from urllib.parse import urlparse
from tempfile import NamedTemporaryFile
from PyPDF2 import PdfReader
from Component.constants import GENAI_API_KEY
import google.generativeai as genai

genai.configure(api_key=GENAI_API_KEY)

def get_conversational_chain(temp):
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model=ChatGoogleGenerativeAI(model="gemini-pro",temperature=temp)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff",prompt=prompt) 
    return chain

def get_text_chunks(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_pdf_content_and_parse(website_url):
    parsed_url = urlparse(website_url)
    if parsed_url.path.endswith(".pdf"):  # Check if the url is a pdf
        response = requests.get(website_url)
        with NamedTemporaryFile(suffix=".pdf") as pdf_file:
            pdf_file.write(response.content)
            pdf_file.seek(0)
            reader = PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""  # Fallback to empty string if None
            #st.warning(text)
    text_chunks = get_text_chunks(text)  # Assuming `get_text_chunks` is a function that you've defined
    get_vector_store(text_chunks)

def user_input(user_question,temp):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    
    new_db = FAISS.load_local("faiss_index", embeddings)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain(temp)

    
    response = chain(
        {"input_documents":docs, "question": user_question}
        , return_only_outputs=True)

    print(response)
    st.write("Reply: ", response["output_text"])