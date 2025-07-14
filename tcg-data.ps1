# tcg-data.ps1 - Data Pipeline Feature Generator for Pokemon TCG App
param([Parameter(ValueFromRemainingArguments)][string[]]$FeatureDescription)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$DevIssueScript = Join-Path $ScriptDir "dev-issue.ps1"

if ($FeatureDescription.Count -eq 0) {
    Write-Host "Usage: .\tcg-data.ps1 'feature description'"
    Write-Host "Example: .\tcg-data.ps1 'optimize Limitless API sync pipeline'"
    exit 1
}

$feature = $FeatureDescription -join " "
& $DevIssueScript -Template "data" -Feature $feature
