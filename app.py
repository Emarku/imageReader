import streamlit as st
import streamlit.components.v1 as components
import requests
from bs4 import BeautifulSoup
import re
import json
from scraper import foleon_scraper
from openai_funtions import open_ai_summary

# User Inputs
st.title('Gleeds Foleon Interpreter')
url = st.text_input("Input Foleon Page URL")

if st.button("Run Analysis"):
    outputs = foleon_scraper(url)

    for title, sub_dict in outputs.items():
        output = str(title) + str(sub_dict["Data"])
        st.markdown(sub_dict["URL"])
        components.iframe(sub_dict["URL"], height=1000)
        st.markdown(open_ai_summary([output]))

