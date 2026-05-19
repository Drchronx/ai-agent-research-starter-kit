---
name: aminer-mcp-research
description: "Use AMiner MCP for academic knowledge graph tasks: scholar search, author profile lookup, institution or team analysis, paper and patent discovery, academic influence checks, and research trend mapping. Trigger when the user mentions AMiner, AMiner MCP, mcp.aminer.cn, scholar portrait, academic graph, institution comparison, expert discovery, patent search, or wants to combine AMiner with literature review and citation verification."
---

# AMiner MCP Research

Use this skill when the task needs AMiner's academic knowledge graph through MCP.

Primary source document: `https://zhipu-ai.feishu.cn/wiki/VHAGwiboFivCztkqknSciiQjn4d`  
AMiner MCP endpoint: `https://mcp.aminer.cn/sse`  
AMiner open docs: `https://www.aminer.cn/open/docs`

## Core Rule

Never invent AMiner results. If the MCP server is not configured, the auth token is missing, or the tool call fails, report the blocker and provide the manual AMiner query plan.

Do not print AMiner auth tokens in chat, logs, documents, or scripts. Refer to them as `AMINER_MCP_TOKEN` or "your AMiner token".

## When To Use

- Find a scholar by name and affiliation.
- Build a scholar profile: affiliation, fields, papers, patents, influence indicators, coauthors.
- Compare institutions, labs, or research teams.
- Identify experts for a research topic.
- Explore paper, patent, author, and institution relationships.
- Map academic trends and knowledge graph relationships.
- Cross-check literature search results from OpenAlex, Semantic Scholar, CNKI, or AI4Scholar.

## Setup Checklist

1. Confirm the user has an AMiner MCP token.
2. Configure the MCP server in the target client:

```json
{
  "aminer": {
    "url": "https://mcp.aminer.cn/sse",
    "headers": {
      "Authorization": "Bearer ${AMINER_MCP_TOKEN}"
    }
  }
}
```

3. Restart the MCP gateway or AI client.
4. Ask the client to list available AMiner tools.
5. Run one low-risk query, such as a known scholar lookup.

## Python MCP Pattern

Use this pattern only when the user asks for direct Python integration:

```python
from mcp import ClientSession
from mcp.client.sse import sse_client

url = "https://mcp.aminer.cn/sse"
headers = {"Authorization": f"Bearer {AMINER_MCP_TOKEN}"}

async with sse_client(url=url, headers=headers) as (read_stream, write_stream):
    async with ClientSession(read_stream, write_stream) as session:
        await session.initialize()
        tools = await session.list_tools()
```

After `list_tools()`, use the actual returned tool schema. Do not guess required parameters.

## Research Workflow

### 1. Clarify entity

Ask for or infer:

- Scholar Chinese and English name.
- Institution or department.
- Research field.
- Time range.
- Whether patent data matters.

For common Chinese names, never treat the first match as correct. Disambiguate by institution, field, coauthors, and representative works.

### 2. Query AMiner

Use AMiner MCP tools for:

- Person search.
- Scholar details.
- Paper list.
- Patent list.
- Institution or organization information.
- Field or trend information when available.

### 3. Cross-validate

For literature-quality outputs, cross-check AMiner results with at least one of:

- `academic-research-openalex`
- `ai4scholar-research`
- `citation-management`
- `cnki-research-assistant`
- DOI, ORCID, official personal homepage, or institutional homepage.

### 4. Output

Use this structure:

```text
Query target:
AMiner evidence:
Cross-check evidence:
Likely identity:
Representative papers:
Patents or applied outputs:
Coauthor/institution network:
Research trend interpretation:
Unverified items:
Next search actions:
```

## Quality Rules

- Separate "AMiner returned" from "I infer".
- Mark uncertain matches as "needs manual verification".
- Do not use h-index, citation count, or paper count alone as a quality judgment.
- For management, psychology, neuroscience, or HCI topics, connect scholar data to research questions, methods, and theory rather than just listing papers.
- For Chinese names, include original Chinese name, romanized name, institution, and field whenever available.

## Reference

For detailed beginner instructions, read `references/aminer-mcp-guide.md`.

