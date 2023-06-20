import streamlit as st
import streamlit.components.v1 as components
import requests
from bs4 import BeautifulSoup
import re
import json
from scraper import foleon_scraper
from openai_funtions import open_ai_summary
import webbrowser
from PIL import Image

im = Image.open("image.png")
im2=Image.open("Untitled.png")
st.set_page_config(
        page_title="Charts reader for Gleeds report",
        page_icon=im,
        layout="wide",
    )
# User Inputs
st.image(im2)
st.title('Gleeds Foleon Interpreter')
url = st.text_input("Input Foleon Page URL")
if st.button("Run Analysis"):
    outputs = foleon_scraper(url)

    for title, sub_dict in outputs.items():
        st.title(f'Title: {title}')
        components.iframe(sub_dict["URL"], height=400)
        output = str(title) + str(sub_dict["Data"])
        st.markdown(f'Data extracted from the chart: ')
        st.markdown(sub_dict["Data"])
        if st.button(f'Click here to go to image source{title}'):
            webbrowser.open_new_tab(sub_dict["URL"])


from openai.error import OpenAIError
from .knowledge_gp.knowledge_gpt.components.sidebar import sidebar
from .knowledge_gp.knowledge_gpt.utils import (
    embed_docs,
    get_answer,
    get_sources,
    parse_docx,
    parse_pdf,
    parse_txt,
    search_docs,
    text_to_docs,
    wrap_text_in_html,
)


def clear_submit():
    st.session_state["submit"] = False


#st.set_page_config(page_title="KnowledgeGPT", page_icon="📖", layout="wide")
st.header("📖KnowledgeGPT")

sidebar()

uploaded_file = st.file_uploader(
    "Upload a pdf, docx, or txt file",
    type=["pdf", "docx", "txt"],
    help="Scanned documents are not supported yet!",
    on_change=clear_submit,
)

index = None
doc = None
if uploaded_file is not None:
    if uploaded_file.name.endswith(".pdf"):
        doc = parse_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".docx"):
        doc = parse_docx(uploaded_file)
    elif uploaded_file.name.endswith(".txt"):
        doc = parse_txt(uploaded_file)
    else:
        raise ValueError("File type not supported!")
    text = text_to_docs(doc)
    try:
        with st.spinner("Indexing document... This may take a while⏳"):
            index = embed_docs(text)
        st.session_state["api_key_configured"] = True
    except OpenAIError as e:
        st.error(e._message)

query = st.text_area("Ask a question about the document", on_change=clear_submit)
with st.expander("Advanced Options"):
    show_all_chunks = st.checkbox("Show all chunks retrieved from vector search")
    show_full_doc = st.checkbox("Show parsed contents of the document")

if show_full_doc and doc:
    with st.expander("Document"):
        # Hack to get around st.markdown rendering LaTeX
        st.markdown(f"<p>{wrap_text_in_html(doc)}</p>", unsafe_allow_html=True)

button = st.button("Submit")
if button or st.session_state.get("submit"):
    if not st.session_state.get("api_key_configured"):
        st.error("Please configure your OpenAI API key!")
    elif not index:
        st.error("Please upload a document!")
    elif not query:
        st.error("Please enter a question!")
    else:
        st.session_state["submit"] = True
        # Output Columns
        answer_col, sources_col = st.columns(2)
        sources = search_docs(index, query)

        try:
            answer = get_answer(sources, query)
            if not show_all_chunks:
                # Get the sources for the answer
                sources = get_sources(answer, sources)

            with answer_col:
                st.markdown("#### Answer")
                st.markdown(answer["output_text"].split("SOURCES: ")[0])

            with sources_col:
                st.markdown("#### Sources")
                for source in sources:
                    st.markdown(source.page_content)
                    st.markdown(source.metadata["source"])
                    st.markdown("---")

        except OpenAIError as e:
            st.error(e._message)
    #st.markdown(open_ai_summary([output]))
