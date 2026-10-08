import streamlit as st
import os

from src.langgraphAgenticAI.ui.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}

    def load_streamlit_ui(self):
        st.set_page_config( page_title=" START "+ self.config.get_page_title(), layout= 'wide')
        st.header( " START "+ self.config.get_page_title())

        with st.sidebar:
            # Get options for config
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()

            self.user_controls["selected_llm"] = st.selectbox("Select LLM", llm_options)
            if self.user_controls["selected_llm"]=='Groq':
                # model selection
                model_options = self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"] = st.selectbox("Select Model", model_options)
                self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"] = st.text_input("API KEY", type="password")

                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning(" Please enter your correct groq api key to proceed, Dont have ? refer : https://console.groq.com/keys ")


            self.user_controls["selected_usecase"] = st.selectbox("Select Usecases" , usecase_options)

            if self.user_controls["selected_usecase"] == "Chatbot With Web":
                os.environ["TAVILY_API_KEY"] =  self.user_controls["TAVILY_API_KEY"]= st.session_state["TAVILY_API_KEY"]= st.text_input("TAVILY API KEY",type="password")
                if not self.user_controls["TAVILY_API_KEY"]:
                    st.warning(" Please enter your tavily api key to proceed. Dont have? refer tavily site")
        return self.user_controls