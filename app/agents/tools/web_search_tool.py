import os
import sys

from custom_exception import CustomException

from typing import List
from tavily import TavilyClient

from dotenv import load_dotenv

load_dotenv()

class WebSearchTool:
    def __init__(self):
        api_key = os.getenv("TAVILY_API_KEY")

        if not api_key:
            raise ValueError("API Key Not Found")
        
        self.client = TavilyClient(api_key=api_key)

    def run(self, query:str, k:int = 5) -> List[str]:
        try:
            response = self.client.search(
                query=query,
                search_depth="advanced",
                topic="general",
                time_range="month",
                max_results=k,
                include_answer=False,
                include_raw_content=False
            )

            results = response.get("results", [])

            return [
                item["content"][:800] for item in results if item.get("content")
            ]
        except Exception as e:
            raise CustomException(e, sys)

if __name__=="__main__":
    web_search_tool = WebSearchTool()
    query = "who is dialga and palkia?"
    print(web_search_tool.run(query=query, k=1))
