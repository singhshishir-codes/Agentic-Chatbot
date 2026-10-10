import streamlit as st
from src.langgraphAgenticAI.graph.graph_builder import GraphBuilder
from src.langgraphAgenticAI.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraphAgenticAI.LLMs.grok_llm import GroqLLM
from src.langgraphAgenticAI.ui.streamlitui.display_results import DisplayResultsStreamlit


def load_langgraph_agenticai_app():
    """
    Load and run the langgraph Agentic AI application with streamlit UI.
    This function initializes the UI, handles user input, configure LLM models,
    sets up the graph based on selected use case, and display the output while 
    implementing exception handeling and robustness.
    """

    ui  = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    if not user_input:
        st.error('Error : Failed to load user input from the UI')
        return 

    if st.session_state.IsFetchButtonClicked:
        user_message = st.session_state.timeframe
    else:
        user_message = st.chat_input("Enter your message:")

    if user_message:
        try:
            obj_llm_config = GroqLLM(user_controls_input= user_input)
            model = obj_llm_config.get_llm_model()

            if not model:
                st.error("Error: LLM model is not initialized")
                return 
            usecase = user_input.get("selected_usecase")

            if not usecase:
                st.error("Error: No usecase selected")
                return

            graph_builder = GraphBuilder(model)
            graph = graph_builder.setup_graph(usecase)
            DisplayResultsStreamlit(usecase, graph, user_message).display_result_on_ui()

        except Exception as e:
            st.error(f"Error while generating a response: {e}")
            return