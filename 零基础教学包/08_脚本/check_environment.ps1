$ErrorActionPreference = "Continue"

Write-Host "=== AI Agent zero-basic environment check ==="
Write-Host "Current directory: $(Get-Location)"
Write-Host "User profile: $env:USERPROFILE"

Write-Host ""
Write-Host "Python:"
try {
    python --version
} catch {
    Write-Host "python not found. Try: py --version"
}

Write-Host ""
Write-Host "PowerShell version:"
$PSVersionTable.PSVersion

Write-Host ""
Write-Host "Skill directories:"
$dirs = @(
    (Join-Path $env:USERPROFILE ".codex\skills"),
    (Join-Path $env:USERPROFILE ".claude\skills"),
    (Join-Path $env:USERPROFILE ".openclaw\skills")
)
foreach ($d in $dirs) {
    if (Test-Path -LiteralPath $d) {
        $count = (Get-ChildItem -LiteralPath $d -Directory -ErrorAction SilentlyContinue | Measure-Object).Count
        Write-Host "OK   $d ($count folders)"
    } else {
        Write-Host "MISS $d"
    }
}

Write-Host ""
Write-Host "Local full skills library:"
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$fullRootItem = Get-ChildItem -LiteralPath $root -Directory |
    Where-Object { $_.Name -like "10_*Skills*" } |
    Select-Object -First 1
if ($fullRootItem) {
    $fullRoot = $fullRootItem.FullName
    $skillCount = (Get-ChildItem -LiteralPath $fullRoot -Directory |
        Where-Object { $_.Name -match "^\d{2}_" -and $_.Name -notlike "09_*" } |
        ForEach-Object {
            Get-ChildItem -LiteralPath $_.FullName -Directory -ErrorAction SilentlyContinue |
                Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName "SKILL.md") }
        } | Measure-Object).Count
    Write-Host "OK   $fullRoot ($skillCount skills)"
} else {
    Write-Host "MISS local full skills library"
}

Write-Host ""
Write-Host "Done."
