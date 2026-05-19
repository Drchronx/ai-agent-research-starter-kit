param(
    [switch]$Install
)

$ErrorActionPreference = "Stop"
$packageRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)

$reqs = Get-ChildItem -LiteralPath $packageRoot -Recurse -Filter requirements.txt |
    Where-Object { $_.FullName -match '\\scripts\\requirements\.txt$|\\requirements\.txt$' } |
    Select-Object @{Name="SkillFolder"; Expression={ Split-Path -Parent (Split-Path -Parent $_.FullName) }},
                  @{Name="Requirements"; Expression={ $_.FullName }}

if (-not $reqs) {
    Write-Host "No requirements.txt found."
    exit 0
}

$reqs | Format-Table -AutoSize

if (-not $Install) {
    Write-Host "Listed only. To install all detected requirements, run with -Install."
    exit 0
}

foreach ($r in $reqs) {
    Write-Host "Installing requirements: $($r.Requirements)"
    python -m pip install -r $r.Requirements
}

Write-Host "Dependency installation finished. Review any pip warnings above."
