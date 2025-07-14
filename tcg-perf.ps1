# tcg-perf.ps1 - Performance Feature Generator for Pokemon TCG App
param([Parameter(ValueFromRemainingArguments)][string[]]$FeatureDescription)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$DevIssueScript = Join-Path $ScriptDir "dev-issue.ps1"

if ($FeatureDescription.Count -eq 0) {
    Write-Host "Usage: .\tcg-perf.ps1 'feature description'"
    Write-Host "Example: .\tcg-perf.ps1 'implement Redis caching for meta calculations'"
    exit 1
}

$feature = $FeatureDescription -join " "
& $DevIssueScript -Template "perf" -Feature $feature
