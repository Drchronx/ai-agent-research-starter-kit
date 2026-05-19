param(
    [string[]]$SkillName,
    [string]$Category,
    [string]$Workspace,
    [string]$DestinationRoot,
    [switch]$List,
    [switch]$DryRun,
    [switch]$ForceCopy
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$libraryRoot = Split-Path -Parent $scriptDir

function Get-LocalSkills {
    $categoryDirs = Get-ChildItem -LiteralPath $libraryRoot -Directory |
        Where-Object { $_.Name -match "^\d{2}_" -and $_.Name -notlike "09_*" }

    foreach ($cat in $categoryDirs) {
        Get-ChildItem -LiteralPath $cat.FullName -Directory -ErrorAction SilentlyContinue |
            Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName "SKILL.md") } |
            ForEach-Object {
                [PSCustomObject]@{
                    Category = $cat.Name
                    Name = $_.Name
                    Source = $_.FullName
                }
            }
    }
}

$allSkills = @(Get-LocalSkills)

if ($List) {
    $allSkills | Sort-Object Category, Name | Select-Object Category, Name | Format-Table -AutoSize
    Write-Host "Total=$($allSkills.Count)"
    exit 0
}

if (-not $SkillName -and -not $Category) {
    throw "Provide -SkillName, -Category, or -List."
}

if (-not $DestinationRoot) {
    if (-not $Workspace) {
        throw "Provide -Workspace or -DestinationRoot."
    }
    $DestinationRoot = Join-Path $Workspace "skills"
}

$selected = @()
if ($SkillName) {
    foreach ($name in $SkillName) {
        $matches = @($allSkills | Where-Object { $_.Name -eq $name })
        if (-not $matches) {
            Write-Host "WARN missing skill: $name"
        }
        $selected += $matches
    }
}

if ($Category) {
    $catMatches = @($allSkills | Where-Object { $_.Category -eq $Category -or $_.Category -like "*$Category*" })
    if (-not $catMatches) {
        Write-Host "WARN missing category: $Category"
    }
    $selected += $catMatches
}

$selected = @($selected | Sort-Object Source -Unique)
if (-not $selected) {
    throw "No skills selected."
}

Write-Host "Local library   : $libraryRoot"
Write-Host "Destination root: $DestinationRoot"
Write-Host "Selected skills : $($selected.Count)"

if ($DryRun) {
    $selected | Select-Object Category, Name, Source | Format-Table -AutoSize
    Write-Host "DryRun enabled. No files copied."
    exit 0
}

New-Item -ItemType Directory -Force -Path $DestinationRoot | Out-Null
$destRootResolved = (Resolve-Path -LiteralPath $DestinationRoot).Path

$copied = 0
$skipped = 0
foreach ($skill in $selected) {
    $dest = Join-Path $DestinationRoot $skill.Name
    if (Test-Path -LiteralPath $dest) {
        if (-not $ForceCopy) {
            Write-Host "SKIP existing: $($skill.Name)"
            $skipped += 1
            continue
        }
        $resolvedDest = (Resolve-Path -LiteralPath $dest).Path
        if (-not ($resolvedDest.StartsWith($destRootResolved, [System.StringComparison]::OrdinalIgnoreCase))) {
            throw "Refusing to remove outside destination root: $resolvedDest"
        }
        Remove-Item -LiteralPath $resolvedDest -Recurse -Force
    }

    Copy-Item -LiteralPath $skill.Source -Destination $dest -Recurse -Force
    Write-Host "COPIED: $($skill.Name)"
    $copied += 1
}

Write-Host "Done. Copied=$copied Skipped=$skipped"

