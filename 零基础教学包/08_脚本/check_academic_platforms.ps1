$ErrorActionPreference = "Continue"

Write-Host "=== Academic platform environment check ==="
Write-Host "AMiner MCP endpoint    : https://mcp.aminer.cn/sse"
Write-Host "AI4Scholar MCP endpoint: https://mcp.ai4scholar.net/sse"

Write-Host ""
Write-Host "Environment variables:"
if ($env:AMINER_MCP_TOKEN) {
    Write-Host "OK   AMINER_MCP_TOKEN is set"
} else {
    Write-Host "MISS AMINER_MCP_TOKEN"
}

if ($env:AI4SCHOLAR_API_KEY) {
    Write-Host "OK   AI4SCHOLAR_API_KEY is set"
} else {
    Write-Host "MISS AI4SCHOLAR_API_KEY"
}

Write-Host ""
Write-Host "Node/npm/OpenClaw:"
try { node --version } catch { Write-Host "MISS node" }
try { npm --version } catch { Write-Host "MISS npm" }
try { openclaw --version } catch { Write-Host "MISS openclaw" }

Write-Host ""
Write-Host "Expected local skill folders:"
$packageRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$materialsRoot = Split-Path -Parent $packageRoot
$localLibraryItem = Get-ChildItem -LiteralPath $materialsRoot -Directory |
    Where-Object { $_.Name -like "*Skills*" } |
    Select-Object -First 1
if ($localLibraryItem) {
    $localLibrary = $localLibraryItem.FullName
} else {
    $fullLibraryItem = Get-ChildItem -LiteralPath $packageRoot -Directory |
        Where-Object { $_.Name -like "10_*Skills*" } |
        Select-Object -First 1
    $localLibrary = $fullLibraryItem.FullName
}
$expected = @(
    "aminer-mcp-research",
    "ai4scholar-research",
    "ai4scholar-paper-search",
    "ai4scholar-paper-detail-batch",
    "ai4scholar-citation-network",
    "ai4scholar-author-intelligence",
    "ai4scholar-paper-recommendation",
    "ai4scholar-pdf-fulltext-reading",
    "ai4scholar-auto-citation-bibtex",
    "ai4scholar-mcp-openclaw-setup",
    "ai4scholar-scholar-mode-projects",
    "ai4scholar-sci-draw"
)
foreach ($name in $expected) {
    $match = Get-ChildItem -LiteralPath $localLibrary -Directory -Recurse -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -eq $name -and (Test-Path -LiteralPath (Join-Path $_.FullName "SKILL.md")) } |
        Select-Object -First 1
    if ($match) {
        Write-Host "OK   $name -> $($match.FullName)"
    } else {
        Write-Host "MISS $name in local library"
    }
}

Write-Host ""
Write-Host "Done. Missing env vars do not mean failure; they mean the platform is not configured yet."
Write-Host "Skills are expected in the local categorized library, not installed into Codex root by default."
