import streamlit as st
import streamlit.components.v1 as components
import requests
from bs4 import BeautifulSoup
import re
import json
from scraper import foleon_scraper, download_link
from openai_funtions import open_ai_summary
import webbrowser
from PIL import Image
import warnings
warnings.simplefilter("ignore", UserWarning)
from openai.error import OpenAIError
from sidebar import sidebar
im = Image.open("Untitled.png")
im2=Image.open("favicon.png")
st.set_page_config(
        page_title='Gleeds Foleon Interpreter',
        page_icon=im2,
        layout="wide",
    )
# User Inputs
st.image(im)
st.title('Gleeds Foleon Interpreter')
def clear_submit():
    st.session_state["submit"] = False

# --- Initialising SessionState ---
if "load_state" not in st.session_state:
     st.session_state.load_state = False
#st.set_page_config(page_title="KnowledgeGPT", page_icon="📖", layout="wide")
#st.header("📖KnowledgeGPT")

apiKey=sidebar()



url = st.text_input("Input Foleon Page URL")
if st.button("Run Analysis") or st.session_state.load_state:
    st.session_state.load_state=True
    outputs = foleon_scraper(url)

    for title, sub_dict in outputs.items():
        dataAll=[]    
        st.title(f'Title: {title}')
        components.iframe(sub_dict["URL"], height=400)
        output = str(title) + str(sub_dict["Data"])
        st.markdown(f'Data extracted from the chart: ')
        st.markdown(sub_dict["Data"])
        summary=open_ai_summary([output],apiKey)
        st.markdown(f'ChatGpt summary: {summary}')
        dataAll.append(str(summary))
        url=sub_dict["URL"]
        st.markdown("Check out this [link](%s) for the chart source" % url)
        st.markdown("Summary of all charts")

    dataAll=''.join(dataAll)
    st.markdown(dataAll)
    st.markdown("""---""")
    st.download_button('Download text', dataAll, 'text')
    st.markdown("""---""")
    st.title("Upload the file you want to ask questions about by clicking the link below:")
    url2='https://knowledgegpt.streamlit.app/'
    st.markdown("Check out this [link](%s) for more" % url2)
