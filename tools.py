from langchain.tools import tool
from bs4 import BeautifulSoup
from tavily import TavilyClient
import requests
from dotenv import load_dotenv
from rich import print
import os

load_dotenv()

tavily = TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))

@tool 
def web_search(query: str) -> str:
    '''Search the web for recent and reliable information on a topic . Returns Titles , URLs and snippets.'''
    results = tavily.search(
        query=query,
        max_results=5
    )

    output = []
    for r in results['results']:
        output.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n"
        )

    return '\n-------------------------------\n'.join(output)

@tool
def scrape_url(url: str) -> str:
    """Scrape a webpage and return its title and text."""

    try:
        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=20
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        title = soup.title.get_text(strip=True) if soup.title else "No title"
        text = soup.get_text(separator=" ", strip=True)

        return f"Title: {title}\n\nContent:\n{text[:5000]}"

    except requests.Timeout:
        return "Error: Website took too long to respond."

    except requests.RequestException as e:
        return f"Could not scrape URL: {e}"


