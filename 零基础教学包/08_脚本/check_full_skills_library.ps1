$ErrorActionPreference = "Stop"

$thisPackage = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$fullRootItem = Get-ChildItem -LiteralPath $thisPackage -Directory |
    Where-Object { $_.Name -like "10_*Skills*" } |
    Select-Object -First 1

if (-not $fullRootItem) {
    throw "Cannot find local full skills library under: $thisPackage"
}
$fullRoot = $fullRootItem.FullName

$categoryDirs = Get-ChildItem -LiteralPath $fullRoot -Directory |
    Where-Object { $_.Name -match "^\d{2}_" -and $_.Name -notlike "09_*" }

$rows = foreach ($cat in $categoryDirs) {
    Get-ChildItem -LiteralPath $cat.FullName -Directory -ErrorAction SilentlyContinue | ForEach-Object {
        [PSCustomObject]@{
            Category = $cat.Name
            Name = $_.Name
            HasSkillMd = Test-Path -LiteralPath (Join-Path $_.FullName "SKILL.md")
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

Write-Host "All full-library skill folders contain SKILL.md. Total=$($rows.Count)"
