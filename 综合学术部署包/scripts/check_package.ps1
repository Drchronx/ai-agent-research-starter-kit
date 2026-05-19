$ErrorActionPreference = "Stop"

$packageRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)

$categoryDirs = Get-ChildItem -LiteralPath $packageRoot -Directory |
    Where-Object { $_.Name -match '^\d{2}_' -and $_.Name -notmatch '手册|模板' }

$rows = foreach ($cat in $categoryDirs) {
    Get-ChildItem -LiteralPath $cat.FullName -Directory | ForEach-Object {
        $skillPath = Join-Path $_.FullName "SKILL.md"
        [PSCustomObject]@{
            Category = $cat.Name
            Name = $_.Name
            HasSkillMd = Test-Path -LiteralPath $skillPath
            Requirements = Test-Path -LiteralPath (Join-Path $_.FullName "scripts\requirements.txt")
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

Write-Host "All packaged skill folders contain SKILL.md."
