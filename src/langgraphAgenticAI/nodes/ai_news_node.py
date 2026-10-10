from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate
import os

from src.langgraphAgenticAI.state.state import State

class AINewsNode:
    def __init__(self, llm):
        """
        Initialize the AINewsNode with API keys for Tavily and Groq.
        """
        self.tavily = TavilyClient()
        self.llm = llm

    def fetch_news( self, state:State) -> dict:
        """
        Fetch AI news based on the specified frequency.
        Args:
            state(dict): The state dictionary containing the frequency.
        Returns:
            dict: State updates containing the normalized frequency and news data.
        """
        frequency = state.get("frequency", "").strip().lower()
        if not frequency:
            raise ValueError(
                "No news frequency found in state. "
                "Please pass the selected news frequency."
            )

        time_range_map = {'daily':'d', 'weekly':'w', 'monthly':'m', 'yearly':'y'}
        days_map = {'daily':1, 'weekly':7, 'monthly':30, 'yearly':365}

        if frequency not in time_range_map:
            raise ValueError(f"Invalid news frequency: {frequency}")

        response = self.tavily.search(
            query="Top artificial intelligence (AI) news in India and globally",
            topic="news",
            time_range=time_range_map[frequency],
            include_answer="advanced",
            max_results=20,
            days=days_map[frequency],
        )
        return {
            "frequency": frequency,
            "news_data": response.get("results", []),
        }

    def summarize_news(self, state:State)-> dict:
        """
        Summarize the fetched news using an LLM.
        Args:
            state(dict): The state dictionary containing 'news_data'.
        Returns:
            dict: State update containing the summary.
        """

        news_items = state.get("news_data", [])

        prompt_template = ChatPromptTemplate.from_messages([
            (
                "system", """Summarize AI news into markdown format. For each item include:
                - Date in 'YYYY-MM-DD' format in IST timezone
                - Concise sentence summary from latest news
                - Sort news by date (latest first)
                - Source URL as link
                Use format:
                #### [Date]
                - [summary](url)
                """
            ),
            ("user", "Article: \n{articles}")
        ])

        article_str = "\n\n".join([
            f"Content: {item.get('content', '')}\n"
            f"URL: {item.get('url', '')}\n"
            f"Date: {item.get('published_date', '')}"
            for item in news_items
        ])

        response = self.llm.invoke(prompt_template.format(articles=article_str))
        return {"summary": response.content}

    def save_results(self, state:State):
        frequency = state["frequency"]
        summary = state["summary"]
        filename = f"./AINews/{frequency}_summary.md"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# {frequency.capitalize()} AI News Summary\n\n")
            f.write(summary)
        return {"filename": filename}
