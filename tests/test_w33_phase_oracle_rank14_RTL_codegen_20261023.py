"""Classical RTL generator for the exact 14-cross-term W33 phase oracle."""
import json,sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_phase_oracle_rank14_RTL_codegen_20261023 import produce
def test_rank14_rtl_generates_both_files_and_1600_expectations():
    j=produce()
    assert j['symplectic_pairs']==7
    assert j['cross_cz_terms']==14
    assert j['valid_address_tests']==1600 and j['invalid_address_tests']==2496
    assert j['total_interface_io_bits']==34
def test_verilog_has_phase_cross_flags_and_onebody_adjustments():
    s=(ROOT/'hardware/w33_phase_oracle_rank14_20261023.sv').read_text()
    assert "cross_comb=da[13:0]&db[13:0]" in s
    assert "flip_comb=(^cross_comb)^da[14]^db[14]" in s
    assert "invalid_comb=(addr_a>=6'd40)||(addr_b>=6'd40)" in s
def test_testbench_covers_all_64x64_codeword_pairs():
    s=(ROOT/'hardware/tb_w33_phase_oracle_rank14_20261023.sv').read_text()
    assert "for(i=0;i<64;i=i+1)" in s
    assert "for(j=0;j<64;j=j+1)" in s
    assert 'ok!=1600 || bad!=2496' in s
def test_actual_up5k_mapped_resource_and_timing_boundary():
    p=ROOT/'data/w33_phase_oracle_rank14_ice40_20261023.json'
    if not p.exists():pytest.skip('UP5K mapped netlist not present in this checkout')
    m=json.loads(p.read_text())['modules']['w33_phase_oracle_rank14_20261023']
    typ=[x['type'] for x in m['cells'].values()]
    assert typ.count('SB_LUT4')==172
    assert typ.count('SB_DFFR')==19
    assert typ.count('SB_CARRY')==4
    assert sum(len(x['bits']) for x in m['ports'].values())==34
    log=ROOT/'data/w33_phase_oracle_rank14_UP5K_pnr_20261023.log'
    if log.exists():
        out=log.read_text()
        assert 'No Fmax available' in out
        assert 'No PCF file specified' in out
