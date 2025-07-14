# tcg-ui.ps1 - UI Feature Generator for Pokemon TCG App
param([Parameter(ValueFromRemainingArguments)][string[]]$FeatureDescription)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$DevIssueScript = Join-Path $ScriptDir "dev-issue.ps1"

if ($FeatureDescription.Count -eq 0) {
    Write-Host "Usage: .\tcg-ui.ps1 'feature description'"
    Write-Host "Example: .\tcg-ui.ps1 'improve dashboard loading performance'"
    exit 1
}

$feature = $FeatureDescription -join " "
& $DevIssueScript -Template "ui" -Feature $feature
