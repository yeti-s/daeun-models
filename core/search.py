import os
import requests
from abc import ABC, abstractmethod
from urllib import parse

GOOGLE_SEARCH_API_KEY = os.environ['GOOGLE_SEARCH_API_KEY']
GOOGLE_SEARCH_ENGINE_ID = os.environ['GOOGLE_SEARCH_ENGINE_ID']
GOOGLE_SEARCH_URL = 'https://www.googleapis.com/customsearch/v1?{params}'

class SearchResult():
    def __init__(self, title:str, link:str, snippet:str):
        self.title = title
        self.link = link
        self.snippet = snippet
    
class SearchEngine(ABC):
    @abstractmethod
    def search(cls, query: str) -> list[SearchResult]:
        pass

class GoogleSearchEngine(SearchEngine):
    def search(self, query: str) -> list[SearchResult]:
        params = parse.urlencode({
            'key': GOOGLE_SEARCH_API_KEY,
            'cx': GOOGLE_SEARCH_ENGINE_ID,
            'q': query
        }, doseq=True)
        response = requests.get(GOOGLE_SEARCH_URL.format(params=params))
        
        if response.status_code != 200:
            raise Exception('Failed to fetch results from Google Search API')
        
        return [SearchResult(
            item['title'],
            item['link'],
            item['snippet']
        ) for item in response.json()['items']]
    
