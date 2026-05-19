# AMiner MCP Beginner Guide

Source document supplied by the user:

```text
https://zhipu-ai.feishu.cn/wiki/VHAGwiboFivCztkqknSciiQjn4d
```

Fetched title: `AMiner MCP 服务使用指南`  
Fetched date: 2026-05-12  

## What AMiner Adds

AMiner is useful when a research task needs academic knowledge graph data rather than only paper search. Use it for scholar identity, affiliation, coauthor networks, institution analysis, patents, and expert discovery.

The source document describes AMiner MCP as an MCP service for standardized academic data queries. It reports coverage of papers, patents, and scholars through AMiner's academic knowledge graph.

## Endpoint

```text
https://mcp.aminer.cn/sse
```

Use an authorization token supplied by AMiner. Store it outside documents and prompts, preferably as an environment variable or private config value.

## Beginner Setup

1. Get an AMiner MCP token.
2. Add the AMiner MCP server to the client configuration.
3. Restart the AI client or gateway.
4. Ask the client to list available tools.
5. Run a known scholar lookup to verify the connection.

Example config pattern:

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

## Example Beginner Prompts

```text
请使用 AMiner MCP 查询清华大学某位学者的基本信息、研究方向、代表论文和合作网络。请区分 AMiner 返回的信息和你自己的推断。
```

```text
请用 AMiner MCP 帮我寻找“AI Agent 与科研创造力”方向的潜在专家，输出学者、机构、代表作、可能相关性和需要核验的信息。
```

```text
请用 AMiner MCP 查询某个研究主题的论文、专利和主要机构分布，再用 OpenAlex 或 AI4Scholar 交叉核验关键论文。
```

## Common Failure Handling

| Problem | Action |
|---|---|
| Connection timeout | Check endpoint, network, client timeout, and retry later |
| Auth failure | Check token validity and expiration |
| Tool list unavailable | Confirm MCP server config and restart gateway/client |
| Name ambiguity | Add institution, department, coauthors, and field |
| Result not verifiable | Cross-check with DOI, ORCID, institutional homepage, OpenAlex, AI4Scholar, or CNKI |

## Research Output Standard

Every AMiner-based output should include:

- Query target and disambiguation conditions.
- AMiner evidence.
- Cross-check source.
- Verified items.
- Unverified items.
- Limitations.

Do not use AMiner metrics alone to claim academic quality. Interpret scholar and institution data in relation to the user's actual research question.

