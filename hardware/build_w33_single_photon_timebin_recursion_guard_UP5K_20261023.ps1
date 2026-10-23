# Reproduce the single-photon recursive metadata guard on iCE40UP5K reference target.
# Toolchain paths point to isolated YoWASP installations on the connected Windows machine.
# I/O is automatically assigned; no real PCB pin constraints or optical hardware.
param(
 [string]$YosysExe='C:\Temp\w33_yowasp_synth\bin\yowasp-yosys.exe',
 [string]$NextpnrExe='C:\Temp\w33_yowasp_pnr\bin\yowasp-nextpnr-ice40.exe'
)
$root=Split-Path $PSScriptRoot -Parent
Push-Location $root
try {
 $env:PYTHONPATH=(Split-Path (Split-Path $YosysExe -Parent) -Parent)
 $yosysCmd='read_verilog -sv hardware/w33_single_photon_timebin_recursion_guard.sv; synth_ice40 -top w33_single_photon_timebin_recursion_guard -json data/w33_single_photon_timebin_recursion_guard_ice40_20261023.json; stat'
 & $YosysExe -Q -T -l data/w33_single_photon_timebin_recursion_guard_synth_20261023.log -p $yosysCmd
 if($LASTEXITCODE -ne 0){throw 'Yosys synthesis failed'}
 $env:PYTHONPATH=(Split-Path (Split-Path $NextpnrExe -Parent) -Parent)
 & $NextpnrExe --up5k --package sg48 --freq 24 --seed 20261023 --pcf-allow-unconstrained --json data/w33_single_photon_timebin_recursion_guard_ice40_20261023.json --asc data/w33_single_photon_timebin_recursion_guard_UP5K_unpinned_20261023.asc --log data/w33_single_photon_timebin_recursion_guard_UP5K_pnr_20261023.log
 if($LASTEXITCODE -ne 0){throw 'nextpnr failed'}
 Write-Host 'PASS reference UP5K route, NOT pin-constrained board deployment'
} finally {Pop-Location}
