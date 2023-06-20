import streamlit as st

from knowledge_gpt.components.faq import faq


def set_openai_api_key(api_key: str):
    st.session_state["OPENAI_API_KEY"] = api_key


def sidebar():
    with st.sidebar:
        st.markdown(
            "## How to use\n"
            "1. Insert the link of one of the Gleeds Foleon reports\n"
            "2. Press submit so the app can read you charts.\n"
            "3. Find also a ChatGpt 3.5 summarization of the chart with insights.\n"
            "4. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below🔑\n"  # noqa: E501
            "5. Upload a pdf, docx, or txt file📄 at the end of the report\n"
            "6. Ask a question about the document💬\n"
            "7. Read and enjoy your results\n"
          
        )
        api_key_input = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="Paste your OpenAI API key here (sk-...)",
            help="You can get your API key from https://platform.openai.com/account/api-keys.",  # noqa: E501
            value=st.session_state.get("OPENAI_API_KEY", ""),
        )

        if api_key_input:
            set_openai_api_key(api_key_input)

        st.markdown("---")
        st.markdown("# About")
        st.markdown(
            "This tool lets you read the Charts from the Foleon reports "
            "and convert them into text with summary. "
            " Another tool called KnowledgeGPT has been added in order to get more insights from you documents "
            "📖KnowledgeGPT allows you to ask questions about your "
            "documents and get accurate answers with instant citations. "
        )
        st.markdown(
            "This tool is a work in progress. "
            "You can contribute to the project on [GitHub]"  # noqa: E501
            "with your feedback and suggestions💡"
        )
        st.markdown("Made by [Joseph Haynes, Erblin Marku and Sheldon Atkinson]")
        st.markdown("KnowledgeGPT is made by [mmz_001](https://twitter.com/mm_sasmitha)")
        st.markdown("---")

        faq()
