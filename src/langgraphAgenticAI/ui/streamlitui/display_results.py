import streamlit as st
from langchain_core.messages import AIMessage, ToolMessage

class DisplayResultsStreamlit:
    def __init__(self, usecase, graph, user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        if self.usecase == "Basic Chatbot":
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

        elif self.usecase == "Chatbot With Web":
            with st.chat_message("user"):
                st.write(self.user_message)

            initial_state = {"messages": [("user", self.user_message)]}
            res = self.graph.invoke(initial_state)
            has_assistant_response = False
            for message in res["messages"]:
                if isinstance(message, ToolMessage):
                    with st.chat_message("assistant"):
                        st.write("Tool Call Start")
                        st.write(message.content)
                        st.write("Tool Call End")
                elif isinstance(message, AIMessage) and message.content:
                    has_assistant_response = True
                    with st.chat_message("assistant"):
                        st.write(message.content)

            if not has_assistant_response:
                st.error("The graph completed without producing an assistant response.")