<#
.SYNOPSIS
    Indestructible Autonomous Pipeline Loop Supervisor for PowerShell.
.DESCRIPTION
    Continuous outer supervisor with multi-tiered fallback:
    1. Runs the continuous pipeline loop daemon (loop.py).
    2. Monitors python exit codes and catches unexpected crashes.
    3. Self-heals stale Git locks before restarting.
    4. Auto-restarts with exponential backoff upon unexpected termination.
    5. Dispatches heartbeat diagnostics to console and disk.
.PARAMETER Interval
    Polling interval in seconds between cycles (default: 60).
.PARAMETER Once
    Run a single iteration and exit immediately.
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

$ErrorActionPreference = "Continue"

Write-Host "===========================================================" -ForegroundColor Cyan
Write-Host "   Volmarr Knowledge Synthesis - Supervisor Watchdog Loop  " -ForegroundColor Cyan
Write-Host "   (Indestructible Multi-Tier Fallback Supervisor Active)   " -ForegroundColor Cyan
Write-Host "===========================================================" -ForegroundColor Cyan

function Clean-StaleLocks {
    $LockFiles = @(
        ".git\index.lock",
        ".git\HEAD.lock",
        ".git\refs\heads\main.lock",
        ".git\shallow.lock",
        ".git\config.lock",
        ".git\commit-graph.lock"
    )
    foreach ($lock in $LockFiles) {
        if (Test-Path $lock) {
            try {
                Remove-Item -Force $lock
                Write-Host "[Self-Healing] Removed stale Git lock: $lock" -ForegroundColor Yellow
            } catch {
                Write-Warning "Could not remove lock $lock : $_"
            }
        }
    }
}

$ArgsList = @("loop.py", "--interval", $Interval)
if ($Once) { $ArgsList += "--once" }
if ($NoPush) { $ArgsList += "--no-push" }
if ($Force) { $ArgsList += "--force" }

if ($Once) {
    Clean-StaleLocks
    uv run python @ArgsList
    exit $LASTEXITCODE
}

# Outer infinite supervisor watchdog loop
$ConsecutiveCrashes = 0
while ($true) {
    try {
        Clean-StaleLocks
        $Timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-dd HH:mm:ss UTC")
        Write-Host "[$Timestamp] Starting / Restarting autonomous loop engine..." -ForegroundColor Green
        
        uv run python @ArgsList

        $ExitCode = $LASTEXITCODE
        if ($ExitCode -eq 0) {
            Write-Host "Loop completed cleanly. Exiting supervisor." -ForegroundColor Green
            break
        } else {
            $ConsecutiveCrashes++
            $Backoff = [Math]::Min($ConsecutiveCrashes * 5, 60)
            Write-Host "[$Timestamp] Python process exited with code $ExitCode. Supervisor reviving engine in $Backoff seconds (Crash #$ConsecutiveCrashes)..." -ForegroundColor Red
            Clean-StaleLocks
            Start-Sleep -Seconds $Backoff
        }
    } catch {
        $ConsecutiveCrashes++
        $Backoff = [Math]::Min($ConsecutiveCrashes * 5, 60)
        Write-Host "Supervisor trapped exception: $_. Reviving in $Backoff seconds..." -ForegroundColor Red
        Clean-StaleLocks
        Start-Sleep -Seconds $Backoff
    }
}
