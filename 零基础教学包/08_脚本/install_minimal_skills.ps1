param(
    [string]$Workspace,
    [string]$DestinationRoot,
    [switch]$IncludeScenarioExperiment,
    [switch]$IncludeFormatting,
    [switch]$IncludeEEG,
    [switch]$IncludeBCI,
    [switch]$IncludePsychometrics,
    [switch]$IncludeCausal,
    [switch]$IncludeProjectManagement,
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

$minimal = @(
    "markitdown",
    "pdf",
    "docx",
    "xlsx",
    "citation-management",
    "academic-research-openalex",
    "literature-review",
    "pdf-paper-summary",
    "empirical-analysis-skill-python",
    "research-data-auto-analysis-plotting",
    "text-analysis-basic",
    "topic-modeling",
    "sentiment-analysis",
    "scientific-writing",
    "peer-review",
    "scientific-critical-thinking",
    "skill-creator",
    "agent-browser",
    "mcp-builder"
)

if ($IncludeScenarioExperiment) {
    $minimal += @(
        "scenario-experiment-benchmark-mining",
        "scenario-experiment-design",
        "scenario-experiment-analysis",
        "scenario-experiment-reporting"
    )
}

if ($IncludeFormatting) {
    $minimal += @(
        "journal-title-page-metadata",
        "journal-abstract-keywords",
        "journal-reference-list-format",
        "journal-statistics-units-style",
        "journal-blind-review-anonymizer"
    )
}

if ($IncludeEEG) {
    $minimal += @(
        "eeg-experiment-planning",
        "eeg-preprocessing-pipeline",
        "erp-segmentation-analysis",
        "eeg-results-writing-figures"
    )
}

if ($IncludeBCI) {
    $minimal += @(
        "bci-data-structure",
        "eeg-feature-engineering-bci",
        "eeg-ml-classical-bci",
        "eeg-deep-learning-bci",
        "eeg-cross-subject-transfer-bci",
        "eeg-model-evaluation-leakage",
        "bci-results-reporting"
    )
}

if ($IncludePsychometrics) {
    $minimal += @(
        "scale-selection-adaptation",
        "scale-reliability-validity",
        "efa-cfa-measurement-model",
        "questionnaire-reporting-template"
    )
}

if ($IncludeCausal) {
    $minimal += @(
        "process-mediation-moderation",
        "causal-inference-design-audit",
        "did-psm-iv-rdd-dml-event-study",
        "statistical-results-tables"
    )
}

if ($IncludeProjectManagement) {
    $minimal += @(
        "project-initializer",
        "project-dashboard",
        "research-log",
        "data-lineage-tracker",
        "manuscript-version-manager",
        "submission-revision-tracker",
        "weekly-research-planner"
    )
}

$minimal = @($minimal | Sort-Object -Unique)

$common = @{}
if ($Workspace) { $common.Workspace = $Workspace }
if ($DestinationRoot) { $common.DestinationRoot = $DestinationRoot }
if ($DryRun) { $common.DryRun = $true }
if ($ForceCopy) { $common.ForceCopy = $true }

& $copyScript -SkillName $minimal @common
