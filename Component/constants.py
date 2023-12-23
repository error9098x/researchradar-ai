import os
import streamlit as st

SMTP_SERVER_ADDRESS = st.secrets['SMTP_SERVER_ADDRESS']
PORT = st.secrets['PORT']
SENDER_PASSWORD = st.secrets['SENDER_PASSWORD']
SENDER_ADDRESS = st.secrets['SENDER_ADDRESS']
GENAI_API_KEY = st.secrets['GOOGLE_API_KEY']
