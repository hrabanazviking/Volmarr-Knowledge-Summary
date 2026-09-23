<#
.SYNOPSIS
    Autonomous Knowledge Synthesis Pipeline Loop Runner for PowerShell.
.DESCRIPTION
    Runs the continuous pipeline loop: delta discovery, ingestion, DAG synthesis,
    16-suite evaluation test validation, and automatic Git push to origin/main.
.PARAMETER Interval
    Polling interval in seconds (default: 60).
.PARAMETER Once
    Run a single iteration and exit.
.PARAMETER NoPush
    Disable automatic Git push.
.PARAMETER Force
    Force complete re-synthesis on each iteration.
#>

[CmdletBinding()]
param (
    [int]$Interval = 60,
    [switch]$Once,
    [switch]$NoPush,
    [switch]$Force
)

Write-Host "===========================================================" -ForegroundColor Cyan
Write-Host "   Volmarr Knowledge Synthesis - Autonomous Loop Runner   " -ForegroundColor Cyan
Write-Host "===========================================================" -ForegroundColor Cyan

$ArgsList = @("loop.py", "--interval", $Interval)
if ($Once) { $ArgsList += "--once" }
if ($NoPush) { $ArgsList += "--no-push" }
if ($Force) { $ArgsList += "--force" }

uv run python @ArgsList
