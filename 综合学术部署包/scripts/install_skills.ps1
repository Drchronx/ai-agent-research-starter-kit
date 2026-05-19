param(
    [ValidateSet("codex", "claude", "openclaw")]
    [string]$Target = "codex",
    [switch]$DryRun,
    [switch]$ForceCopy
)

$ErrorActionPreference = "Stop"

$packageRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)

switch ($Target) {
    "codex" { $targetRoot = Join-Path $env:USERPROFILE ".codex\skills" }
    "claude" { $targetRoot = Join-Path $env:USERPROFILE ".claude\skills" }
    "openclaw" { $targetRoot = Join-Path $env:USERPROFILE ".openclaw\skills" }
}

$categoryDirs = Get-ChildItem -LiteralPath $packageRoot -Directory |
    Where-Object { $_.Name -match '^\d{2}_' -and $_.Name -notmatch '手册|模板' }

$skills = foreach ($cat in $categoryDirs) {
    Get-ChildItem -LiteralPath $cat.FullName -Directory |
        Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName "SKILL.md") } |
        ForEach-Object {
            [PSCustomObject]@{
                Category = $cat.Name
                Name = $_.Name
                Source = $_.FullName
                Destination = Join-Path $targetRoot $_.Name
            }
        }
}

Write-Host "Package root: $packageRoot"
Write-Host "Target root : $targetRoot"
Write-Host "Skills found: $($skills.Count)"

if ($DryRun) {
    $skills | Select-Object Category, Name, Destination | Format-Table -AutoSize
    Write-Host "DryRun enabled. No files copied."
    exit 0
}

New-Item -ItemType Directory -Force -Path $targetRoot | Out-Null

$copied = 0
$skipped = 0

foreach ($skill in $skills) {
    if ((Test-Path -LiteralPath $skill.Destination) -and -not $ForceCopy) {
        Write-Host "SKIP existing: $($skill.Name)"
        $skipped += 1
        continue
    }

    Copy-Item -LiteralPath $skill.Source -Destination $skill.Destination -Recurse -Force
    Write-Host "COPIED: $($skill.Name)"
    $copied += 1
}

Write-Host "Done. Copied=$copied Skipped=$skipped Target=$targetRoot"
