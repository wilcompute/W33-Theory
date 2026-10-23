# iCE40UP5K reference implementation of the Walsh-qutrit frame metadata controller.
# No board-specific pinout, calibrated optical actuator or detector wiring.
param(
 [string]$YosysExe='C:\Temp\w33_yowasp_synth\bin\yowasp-yosys.exe',
 [string]$NextpnrExe='C:\Temp\w33_yowasp_pnr\bin\yowasp-nextpnr-ice40.exe',
 [double]$ClockMHz=24
)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
if(-not(Test-Path $YosysExe)){throw "Missing Yosys: $YosysExe"}
if(-not(Test-Path $NextpnrExe)){throw "Missing nextpnr: $NextpnrExe"}
$env:PYTHONPATH=(Split-Path (Split-Path $YosysExe -Parent) -Parent)+';'+(Split-Path (Split-Path $NextpnrExe -Parent) -Parent)
Push-Location $root
try {
 $cmd='read_verilog -sv hardware/w33_walsh_qutrit_frame.sv; synth_ice40 -top w33_walsh_qutrit_frame -json data/w33_walsh_qutrit_frame_ice40_20261023.json; stat'
 & $YosysExe -Q -T -l data/w33_walsh_qutrit_ice40_synth_20261023.log -p $cmd
 if($LASTEXITCODE -ne 0){throw "Yosys returned $LASTEXITCODE"}
 $args=@('--up5k','--package','sg48','--freq',"$ClockMHz",'--seed','20261023','--pcf-allow-unconstrained','--json','data/w33_walsh_qutrit_frame_ice40_20261023.json','--asc','data/w33_walsh_qutrit_frame_UP5K_unpinned_20261023.asc','--log','data/w33_walsh_qutrit_frame_UP5K_pnr_20261023.log')
 & $NextpnrExe @args
 if($LASTEXITCODE -ne 0){throw "nextpnr returned $LASTEXITCODE"}
 Write-Host 'PASS UP5K UNPINNED place and route; not a board bitstream'
} finally { Pop-Location }
