from langgraph.graph import StateGraph, START, END
from src.langgraphAgenticAI.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraphAgenticAI.nodes.chatbot_with_tool_node import ChatbotWithToolNode
from src.langgraphAgenticAI.state.state import State
from src.langgraphAgenticAI.tools.search_tool import create_tool_node, get_tools
from langgraph.prebuilt import tools_condition, ToolNode

class GraphBuilder:
    def __init__(self, model):
        self.llm = model
        self.graph_builder = StateGraph(State)

    def basic_chatbot_build_graph(self):
        """
        Builds a basic chatbot graph using langgraph.
        This method initializes a chatbot node using "BasicChatbotNode" class
        and integrate it into the graph. The chatbot node is set as both the entry and exit point of graph.
        """
        self.basic_chatbot_node = BasicChatbotNode(self.llm)

        self.graph_builder.add_node("chatbot", self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START , "chatbot")
        self.graph_builder.add_edge( "chatbot" , END)

    def chatbot_with_tool_build_graph(self):
        """
        Builds an advance chatbot graph with tool integration,
        this method create a chatbot graph that includes both chatbot node and tool node.
        It defines tools initializes chatbot with capabilities, and sets up unconditional and direct edge between nodes.
        The chatbot node is set as the entry point.
        """
        # Defining the tool and tool node
        tools = get_tools()
        tool_node = create_tool_node(tools)
        # Define LLMs
        llm = self.llm

        # Define the chatbot node

        obj_chatbot_with_node = ChatbotWithToolNode(llm)
        chatbot_node = obj_chatbot_with_node.create_chatbot(tools)
    

        # Define nodes
        self.graph_builder.add_node("chatbot", chatbot_node)
        self.graph_builder.add_node("tools", tool_node)
        # Define conditional and edges
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_conditional_edges("chatbot", tools_condition)
        self.graph_builder.add_edge("tools", "chatbot")
        self.graph_builder.add_edge("chatbot", END)



    def setup_graph( self, usecase:str):
        """
        Setup the graph for the selected usecase
        """
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
        if usecase == "Chatbot With Web":
            self.chatbot_with_tool_build_graph()

        return self.graph_builder.compile()