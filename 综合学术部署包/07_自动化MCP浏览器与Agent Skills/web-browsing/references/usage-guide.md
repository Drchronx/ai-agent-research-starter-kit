# Web Browsing Usage Guide

## Quick Start

### Search the Web
```python
from scripts.search_web import search_web

results = search_web("latest python tutorial", num_results=3)
for r in results:
    print(f"{r['title']}: {r['snippet']}")
```

### Visit a Website
```python
from scripts.search_web import fetch_url

page = fetch_url("https://example.com")
print(page['title'])
print(page['content'][:500])
```

## Advanced Usage

### Extract Specific Data
For structured data extraction, combine with HTML parsing:

```python
from bs4 import BeautifulSoup

def extract_prices(url):
    page = fetch_url(url)
    soup = BeautifulSoup(page['content'], 'html.parser')
    
    prices = []
    for item in soup.find_all('div', class_='product-price'):
        prices.append(item.get_text(strip=True))
    
    return prices
```

### Search with Filters
You can refine searches by adding keywords:

```python
# Specific site search
search_web("site:wikipedia.org quantum computing")

# File type search  
search_web("pdf machine learning tutorial filetype:pdf")
```

## Error Handling

Always handle potential errors:

```python
try:
    results = search_web("some query")
    if any('error' in r for r in results):
        print("Search failed, try different keywords")
    else:
        display_results(results)
except Exception as e:
    print(f"Error: {e}")
```

## Rate Limiting

Be respectful of websites:
- Don't make more than 10 requests per minute
- Add delays between multiple fetches
- Respect robots.txt (handled automatically by most search engines)

## Tips for Better Results

1. **Use specific keywords** - "React hooks tutorial 2024" vs "react stuff"
2. **Try different search engines** - DuckDuckGo is default, but you can switch
3. **Check multiple results** - First result isn't always best
4. **Verify sources** - Cross-reference important information

---

For more examples, check the main SKILL.md file!
