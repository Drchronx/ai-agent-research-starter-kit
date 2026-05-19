param(
    [string]$Workspace,
    [string]$DestinationRoot,
    [switch]$DryRun,
    [switch]$ForceCopy
)

$ErrorActionPreference = "Stop"

$packageRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$parentRoot = Split-Path -Parent $packageRoot
$libraryRootItem = Get-ChildItem -LiteralPath $parentRoot -Directory |
    Where-Object { $_.Name -like "*Skills*" -and (Test-Path -LiteralPath (Join-Path $_.FullName "skills_manifest.csv")) } |
    Select-Object -First 1

if (-not $libraryRootItem) {
    throw "Cannot find local skills library next to this package."
}

$libraryRoot = $libraryRootItem.FullName
$toolsDir = Get-ChildItem -LiteralPath $libraryRoot -Directory |
    Where-Object { $_.Name -like "00_*" } |
    Select-Object -First 1

if (-not $toolsDir) {
    throw "Cannot find tools directory in local skills library."
}

$copyScript = Join-Path $toolsDir.FullName "copy_skill_to_workspace.ps1"

if (-not (Test-Path -LiteralPath $copyScript)) {
    throw "Cannot find local copy script: $copyScript"
}

if (-not $Workspace -and -not $DestinationRoot) {
    throw "This compatibility script no longer installs to Codex root. Provide -Workspace or -DestinationRoot."
}

$common = @{}
if ($Workspace) { $common.Workspace = $Workspace }
if ($DestinationRoot) { $common.DestinationRoot = $DestinationRoot }
if ($DryRun) { $common.DryRun = $true }
if ($ForceCopy) { $common.ForceCopy = $true }

& $copyScript -Category "Skills" @common
