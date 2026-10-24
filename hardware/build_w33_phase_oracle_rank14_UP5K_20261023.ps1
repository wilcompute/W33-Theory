# Reference build of 14-term W33 phase-oracle control logic; NO actual optical device.
# Auto-assigned SG48 pins: this is NOT a board-constrained implementation.
param(
 [string]$YosysExe='C:\Temp\w33_yowasp_synth\bin\yowasp-yosys.exe',
 [string]$NextpnrExe='C:\Temp\w33_yowasp_pnr\bin\yowasp-nextpnr-ice40.exe',
 [string]$IcarusExe='C:\iverilog\bin\iverilog.exe',
 [string]$VvpExe='C:\iverilog\bin\vvp.exe'
)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
Push-Location $root
try {
 py analysis/w33_phase_oracle_rank14_RTL_codegen_20261023.py
 if($LASTEXITCODE -ne 0){throw 'RTL generation failed'}
 & $IcarusExe -g2012 -s tb_w33_phase_oracle_rank14_20261023 -o "$env:TEMP\w33_phase_oracle_rank14.vvp" hardware/w33_phase_oracle_rank14_20261023.sv hardware/tb_w33_phase_oracle_rank14_20261023.sv
 if($LASTEXITCODE -ne 0){throw 'Icarus compilation failed'}
 & $VvpExe "$env:TEMP\w33_phase_oracle_rank14.vvp"
 if($LASTEXITCODE -ne 0){throw 'Icarus scoreboard failed'}
 $env:PYTHONPATH=Split-Path (Split-Path $YosysExe -Parent) -Parent
 $cmd='read_verilog -sv hardware/w33_phase_oracle_rank14_20261023.sv; synth_ice40 -top w33_phase_oracle_rank14_20261023 -json data/w33_phase_oracle_rank14_ice40_20261023.json; stat'
 & $YosysExe -Q -T -l data/w33_phase_oracle_rank14_ice40_synth_20261023.log -p $cmd
 if($LASTEXITCODE -ne 0){throw 'Yosys synthesis failed'}
 $env:PYTHONPATH=Split-Path (Split-Path $NextpnrExe -Parent) -Parent
 & $NextpnrExe --up5k --package sg48 --freq 24 --seed 20261023 --pcf-allow-unconstrained --json data/w33_phase_oracle_rank14_ice40_20261023.json --asc data/w33_phase_oracle_rank14_UP5K_unpinned_20261023.asc --log data/w33_phase_oracle_rank14_UP5K_pnr_20261023.log
 if($LASTEXITCODE -ne 0){throw 'nextpnr route failed'}
 Write-Host 'PASS classical control RTL all 4096 address pairs; UNPINNED nextpnr only, no real Fmax or board'
} finally {Pop-Location}
