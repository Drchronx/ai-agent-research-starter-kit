$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$libraryRoot = Split-Path -Parent $scriptDir

$categoryDirs = Get-ChildItem -LiteralPath $libraryRoot -Directory |
    Where-Object { $_.Name -match "^\d{2}_" -and $_.Name -notlike "09_*" }

$rows = foreach ($cat in $categoryDirs) {
    Get-ChildItem -LiteralPath $cat.FullName -Directory -ErrorAction SilentlyContinue | ForEach-Object {
        [PSCustomObject]@{
            Category = $cat.Name
            Name = $_.Name
            HasSkillMd = Test-Path -LiteralPath (Join-Path $_.FullName "SKILL.md")
        }
    }
}

$rows | Group-Object Category | Select-Object Name, Count | Sort-Object Name | Format-Table -AutoSize

$missing = $rows | Where-Object { -not $_.HasSkillMd }
if ($missing) {
    Write-Host "Missing SKILL.md:"
    $missing | Format-Table -AutoSize
    exit 1
}

Write-Host "All local skill folders contain SKILL.md. Total=$($rows.Count)"

