---
name: web-browsing
description: Browse and summarize websites, extract content from URLs, search the web for information. Use when user asks to visit a website, get webpage content, search online, or find current information that requires browsing the internet.
---

# Web Browsing Skill

This skill enables browsing websites, extracting content from URLs, and searching the web for information.

## When to Use

**Use this skill when:**
- User asks you to visit a website (e.g., "Check out example.com")
- User wants webpage content summarized
- User needs current information that requires internet search
- User provides a URL and wants it analyzed
- User asks to search for something online

## How It Works

### 1. Direct URL Access
When given a specific URL:
```markdown
User: "What's on https://example.com?"
→ Visit the page, extract main content, summarize key points
```

### 2. Web Search
When user asks to search:
```markdown
User: "Find information about climate change"
→ Perform web search, present top results with summaries
```

### 3. Content Extraction
For specific data extraction:
```markdown
User: "Get the latest news from techcrunch.com"
→ Navigate to site, extract relevant articles/headlines
```

## Tools Available

- **web_search**: Search the web for information
- **fetch_url**: Visit and retrieve webpage content
- **extract_content**: Parse HTML and extract structured data

## Best Practices

1. **Be specific** - Tell me what you want from the page (summary, specific data, latest news)
2. **Provide URLs** - If you have a specific page, share the URL directly
3. **Clarify intent** - Let me know if you need:
   - Quick summary
   - Detailed analysis
   - Specific data points
   - Latest updates

## Examples

```markdown
✅ "Visit https://news.ycombinator.com and summarize today's top stories"
✅ "Search for the latest React.js tutorial"
✅ "Check what's on Wikipedia's page about quantum computing"
✅ "Find pricing information from apple.com/iphone"
❌ Just say "browse the web" - be more specific!
```

## Limitations

- Cannot interact with JavaScript-heavy sites (may miss dynamic content)
- Some sites block automated access
- Video/audio content cannot be played, only described if available
- Login-required pages won't work without credentials

---

**Ready to browse!** Just give me a URL or tell me what to search for. 🌐
