# Matched W33 point/Q43 dual-line-bus FPGA reference builds; NO optical hardware.
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
 $env:OPENBLAS_NUM_THREADS='1'
 py analysis/w33_q43_cospectral_mode_entanglement_phase_complexity_20261023.py
 if($LASTEXITCODE -ne 0){throw 'cospectral certificate failed'}
 py analysis/w33_linebus_dual_q43_phase_geometry_20261023.py
 if($LASTEXITCODE -ne 0){throw 'dual-line geometry failed'}
 py analysis/w33_q43_eight_term_oracle_rtl_20261023.py
 if($LASTEXITCODE -ne 0){throw 'Q43 generation failed'}
 py analysis/w33_linebus_q43_address_bridge_codegen_20261023.py
 if($LASTEXITCODE -ne 0){throw 'bridge generation failed'}
 py analysis/w33_linebus_q43_direct_rank8_RTL_codegen_20261023.py
 if($LASTEXITCODE -ne 0){throw 'direct native generation failed'}
 $cfgs=@(
  @('q43_phase_oracle_rank8_20261023','q43_phase_oracle_rank8'),
  @('w33_linebus_dual_q43_phase_bridge_20261023','w33_linebus_q43_bridge'),
  @('w33_linebus_dual_rank8_direct_20261023','w33_linebus_dual_rank8_direct')
 )
 foreach($cfg in $cfgs) {
  $name=$cfg[0];$stem=$cfg[1]
  $rtl="hardware/$name.sv";$tb="hardware/tb_$name.sv"
  $extra=@()
  if($name -eq 'w33_linebus_dual_q43_phase_bridge_20261023') {
   $extra=@('hardware/q43_phase_oracle_rank8_20261023.sv')
  }
  & $IcarusExe -g2012 -s "tb_$name" -o "$env:TEMP/$name.vvp" $rtl $tb @extra
  if($LASTEXITCODE -ne 0){throw "Icarus build failed $name"}
  & $VvpExe "$env:TEMP/$name.vvp"
  if($LASTEXITCODE -ne 0){throw "Icarus tests failed $name"}
  $outputJson="data/"+$stem+"_ice40_20261023.json"
  $outputAsc="data/"+$stem+"_UP5K_unpinned_20261023.asc"
  $log="data/"+$stem+"_UP5K_pnr_20261023.log"
  $env:PYTHONPATH=Split-Path (Split-Path $YosysExe -Parent) -Parent
  $ys="read_verilog -sv $rtl $($extra -join ' '); synth_ice40 -top $name -json $outputJson; stat"
  & $YosysExe -Q -T -p $ys
  if($LASTEXITCODE -ne 0){throw "Yosys failed $name"}
  $env:PYTHONPATH=Split-Path (Split-Path $NextpnrExe -Parent) -Parent
  & $NextpnrExe --up5k --package sg48 --freq 24 --seed 20261023 --pcf-allow-unconstrained --json $outputJson --asc $outputAsc --log $log
  if($LASTEXITCODE -ne 0){throw "nextpnr failed $name"}
 }
 Write-Host 'PASS classical 40-line-bus Q43 oracle reference; UNPINNED, NO physical photon hardware'
} finally {Pop-Location}
