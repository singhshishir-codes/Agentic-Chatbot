from typing_extensions import NotRequired, TypedDict
from langgraph.graph.message import add_messages
from typing import Annotated

class State(TypedDict):
    """
    Represents the structure of state used in graph
    """
    messages: Annotated[list, add_messages]
    frequency: NotRequired[str]
    news_data: NotRequired[list[dict]]
    summary: NotRequired[str]
    filename: NotRequired[str]