import streamlit as st
from langchain_core.messages import AIMessage

class DisplayResultsStreamlit:
    def __init__(self, usecase, graph, user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        if self.usecase != "Basic Chatbot":
            return

        with st.chat_message("user"):
            st.write(self.user_message)

        final_message = None
        for state in self.graph.stream(
            {"messages": [("user", self.user_message)]},
            stream_mode="values",
        ):
            messages = state.get("messages", [])
            if messages:
                final_message = messages[-1]

        with st.chat_message("assistant"):
            if isinstance(final_message, AIMessage):
                st.write(final_message.content)
            else:
                st.error("The graph completed without producing an assistant response.")