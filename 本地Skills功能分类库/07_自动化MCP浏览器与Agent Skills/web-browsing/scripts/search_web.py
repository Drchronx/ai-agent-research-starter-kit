#!/usr/bin/env python3
"""
Web search utility for the web-browsing skill.
Searches the web and returns relevant results.
"""

import requests
from bs4 import BeautifulSoup
import urllib.parse


def search_web(query: str, num_results: int = 5) -> list[dict]:
    """
    Perform a web search and return results.
    
    Args:
        query: Search query string
        num_results: Number of results to return (default: 5)
    
    Returns:
        List of dictionaries with title, url, and snippet
    """
    # Using DuckDuckGo HTML API (no API key required)
    search_url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        
        # Extract search results
        for result in soup.find_all('a', class_='result__a')[:num_results]:
            title = result.get_text()
            url = result.get('href', '')
            
            # Get snippet from adjacent div
            snippet_div = result.find_parent().find_next_sibling('div', class_='result__snippet')
            snippet = snippet_div.get_text() if snippet_div else ''
            
            results.append({
                'title': title,
                'url': url,
                'snippet': snippet
            })
        
        return results
    
    except Exception as e:
        return [{'error': f'Search failed: {str(e)}'}]


def fetch_url(url: str) -> dict:
    """
    Fetch and parse a webpage.
    
    Args:
        url: URL to fetch
    
    Returns:
        Dictionary with title, content, and metadata
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract title
        title_tag = soup.find('title')
        title = title_tag.get_text().strip() if title_tag else 'No title found'
        
        # Remove script and style elements
        for element in soup(['script', 'style', 'nav', 'footer']):
            element.decompose()
        
        # Get main content (prefer article, otherwise body)
        article = soup.find('article') or soup.find('main') or soup.find('body')
        content = article.get_text(separator='\n\n', strip=True) if article else ''
        
        return {
            'url': url,
            'title': title,
            'content': content[:5000],  # Limit to first 5000 chars
            'status': 'success'
        }
    
    except Exception as e:
        return {'error': f'Failed to fetch URL: {str(e)}', 'url': url}


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: search_web.py <search_query|url> [--fetch]")
        sys.exit(1)
    
    query = sys.argv[1]
    fetch_mode = '--fetch' in sys.argv
    
    if fetch_mode:
        result = fetch_url(query)
    else:
        result = search_web(query)
    
    import json
    print(json.dumps(result, ensure_ascii=False, indent=2))
