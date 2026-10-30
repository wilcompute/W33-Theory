# Carry the state that is NOT in git to another computer (2026-10-30).
#
#   pwsh -File scripts/machine_transfer.ps1 export [-Out C:\path\toe_state.zip]   # on the old machine
#   pwsh -File scripts/machine_transfer.ps1 import  -In  C:\path\toe_state.zip    # on the new machine, after cloning
#
# What it carries (everything else is in the repository):
#   claude_memory/   ~/.claude/projects/<this repo>/memory   -- the agent's long-term project memory (MEMORY.md + facts)
#   codex_config/    ~/.codex/config.toml and AGENTS.md from WSL (NOT the 2+ GB session history: Codex sessions are local-only
#                    and are not needed to resume work; archive them first with `codex archive`)
#   wsl_orb/         ~/orb/*.py, *.sh and the strict/verbose build recipes from WSL (the orbifolder binaries are rebuilt)
#   tools.txt        where tectonic, PARI, Lean were found, so the new machine can match them
# The zip never goes into the repository: it may hold machine paths and private notes.
param([Parameter(Mandatory)][ValidateSet("export", "import")][string]$Mode, [string]$Out, [string]$In)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
# Claude stores per-project memory under a folder named after the MAIN checkout's path (not a worktree's), every character other
# than a letter or digit replaced by '-'
$Main = Split-Path -Parent (git -C $Root rev-parse --path-format=absolute --git-common-dir)
$Slug = ($Main -replace '[^A-Za-z0-9]', '-')
$MemDir = Join-Path $HOME ".claude\projects\$Slug\memory"

if ($Mode -eq "export") {
    if (-not $Out) { $Out = Join-Path $HOME "toe_state_$(Get-Date -Format yyyyMMdd).zip" }
    $Stage = Join-Path ([IO.Path]::GetTempPath()) "toe_state_$(Get-Random)"
    New-Item -ItemType Directory -Force $Stage | Out-Null
    if (Test-Path $MemDir) { Copy-Item -Recurse $MemDir (Join-Path $Stage "claude_memory") }
    if (Get-Command wsl -ErrorAction SilentlyContinue) {
        $w = (wsl -e wslpath -a ($Stage -replace '\\', '/')).Trim()
        wsl -e bash -lc "mkdir -p '$w/codex_config' '$w/wsl_orb'; cp ~/.codex/config.toml ~/.codex/AGENTS.md '$w/codex_config/' 2>/dev/null; cd ~/orb 2>/dev/null && find . -maxdepth 2 \( -name '*.py' -o -name '*.sh' -o -name 'Makefile' -o -name '*.patch' \) -size -2M -exec cp --parents {} '$w/wsl_orb/' \; ; true"
    }
    "python=$((Get-Command py -ErrorAction SilentlyContinue).Source)`n" + (py -3 scripts/doctor.py | Out-String) | Set-Content (Join-Path $Stage "tools.txt")
    Compress-Archive -Force -Path (Join-Path $Stage "*") -DestinationPath $Out
    Remove-Item -Recurse -Force $Stage
    Write-Host "exported -> $Out  (copy it to the new machine; do not commit it)"
}
else {
    if (-not $In -or -not (Test-Path $In)) { throw "pass -In <zip from export>" }
    $Stage = Join-Path ([IO.Path]::GetTempPath()) "toe_state_$(Get-Random)"
    Expand-Archive -Force $In $Stage
    if (Test-Path (Join-Path $Stage "claude_memory")) {
        New-Item -ItemType Directory -Force $MemDir | Out-Null
        Copy-Item -Recurse -Force (Join-Path $Stage "claude_memory\*") $MemDir
        Write-Host "claude memory -> $MemDir"
    }
    if (Get-Command wsl -ErrorAction SilentlyContinue) {
        $w = (wsl -e wslpath -a ($Stage -replace '\\', '/')).Trim()
        wsl -e bash -lc "mkdir -p ~/.codex ~/orb; cp -n '$w'/codex_config/* ~/.codex/ 2>/dev/null; cp -rn '$w'/wsl_orb/. ~/orb/ 2>/dev/null; true"
        Write-Host "codex config -> WSL ~/.codex (existing files kept); orbifolder recipes -> WSL ~/orb"
    }
    Write-Host "old machine's tool locations:"; Get-Content (Join-Path $Stage "tools.txt") | Select-Object -First 30
    Remove-Item -Recurse -Force $Stage
}
