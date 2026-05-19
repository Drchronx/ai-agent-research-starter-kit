---
name: ai4scholar-mcp-openclaw-setup
description: "Set up AI4Scholar access through MCP or the OpenClaw plugin. Trigger for AI4Scholar deployment, ai4scholar.net API key configuration, mcp.ai4scholar.net/sse, OpenClaw plugin install, Scholar plugin setup, gateway restart, Windows plugin install troubleshooting, or verifying AI4Scholar availability."
---

# AI4Scholar MCP And OpenClaw Setup

Use this skill to deploy AI4Scholar as a scholarly tool provider for an Agent. It covers the two access modes from the source guide: lightweight MCP and full OpenClaw plugin.

Source guide: `https://lifu-coze.feishu.cn/wiki/WOaewK33Ei2g1nkt44kcRXiBnze`

## Security Rules

- Never print or store the real API key in shared notes, manuals, or chat output.
- Use `${AI4SCHOLAR_API_KEY}` as a placeholder.
- Prefer environment variables or a local private config file.
- Do not commit `openclaw.json` if it contains a real key.

## Choose The Mode

| Mode | Use when | Includes |
|---|---|---|
| MCP | User wants fast setup and core AI4Scholar tools | search, PDF/full-text, citation support, scientific drawing depending on server exposure |
| OpenClaw plugin | User wants full AI4Scholar experience | 36 tools, Scholar Mode, slash commands, project/library workflow |

## MCP Setup

Add this to the client's MCP server configuration:

```json
{
  "mcpServers": {
    "ai4scholar": {
      "url": "https://mcp.ai4scholar.net/sse",
      "headers": {
        "Authorization": "Bearer ${AI4SCHOLAR_API_KEY}"
      }
    }
  }
}
```

Then restart the gateway or AI client.

## OpenClaw Plugin Setup

Requirements:

- OpenClaw installed.
- Node.js 18 or newer.
- AI4Scholar account and API key from `https://ai4scholar.net`.

Install:

```bash
openclaw plugins install ai4scholar
```

Configure `openclaw.json`:

```json
"ai4scholar": {
  "enabled": true,
  "config": {
    "apiKey": "${AI4SCHOLAR_API_KEY}"
  }
}
```

Restart:

```bash
openclaw gateway stop
openclaw gateway start
```

Verify:

```bash
openclaw plugins list
```

The startup log should indicate that the API key is configured. Do not paste the log if it prints secrets.

## Windows Plugin Install Failure

If OpenClaw plugin install fails with a Windows spawn error, use one of these routes:

1. Prefer MCP mode to avoid plugin installation.
2. Confirm `npm --version` works and npm is in `PATH`.
3. Manual plugin install:

```bash
npm pack ai4scholar
mkdir %USERPROFILE%\.openclaw\extensions\ai4scholar
tar -xzf ai4scholar-0.6.3.tgz -C %USERPROFILE%\.openclaw\extensions\ai4scholar --strip-components=1
openclaw gateway stop
openclaw gateway start
```

Check the actual package version after `npm pack`; do not assume `0.6.3` if a newer tarball is downloaded.

## Verification Prompt

```text
Check whether AI4Scholar is available.
Do not display the API key.
Verify whether MCP or the OpenClaw plugin is configured, then run a small low-cost paper-search test.
```

## Troubleshooting

| Problem | Check |
|---|---|
| API key invalid | Recreate key on `ai4scholar.net` and update local config |
| Search result empty | Broaden query, try another source, check network |
| Plugin not found | Use npm package route; do not search only in a plugin marketplace |
| DOI download fails | Check institutional access; use open-access tools first |
| PDF extraction poor | Use local `pdf` or `markitdown` fallback |
