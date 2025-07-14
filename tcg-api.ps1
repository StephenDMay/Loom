# tcg-api.ps1 - API Feature Generator for Pokemon TCG App
param([Parameter(ValueFromRemainingArguments)][string[]]$FeatureDescription)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$DevIssueScript = Join-Path $ScriptDir "dev-issue.ps1"

if ($FeatureDescription.Count -eq 0) {
    Write-Host "Usage: .\tcg-api.ps1 'feature description'"
    Write-Host "Example: .\tcg-api.ps1 'implement tournament bracket API endpoints'"
    exit 1
}

$feature = $FeatureDescription -join " "
& $DevIssueScript -Template "api" -Feature $feature
