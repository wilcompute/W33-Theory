"""FPGA physical-pin contract is fail-closed when no board data are supplied."""
import sys,json
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_timebin_UP5K_board_pin_contract_20261023 import (
pins_from_yosys_json, make_manifest,parse_pcf,approve)
NET=ROOT/'data/w33_single_photon_timebin_recursion_guard_ice40_20261023.json'
def test_actual_yosys_netlist_port_contract_rebuilds():
    p=make_manifest(NET)
    assert p['io_count']==25
    assert len(p['unassigned_ports'])==25
    assert p['status'].startswith('INCOMPLETE')
    assert p['real_board_product'] is None
def test_missing_board_signoff_is_an_error(tmp_path):
    p=make_manifest(NET)
    m=tmp_path/'board.json';m.write_text(json.dumps(p))
    pc=tmp_path/'pins.pcf';pc.write_text('')
    with pytest.raises(ValueError,match='APPROVED'):approve(NET,m,pc)
def test_synthetic_approval_only_validates_pcf_syntax_never_electricals(tmp_path):
    p=make_manifest(NET)
    p.update(status='APPROVED_BY_HARDWARE_OPERATOR',real_board_product='SYNTHETIC TEST ONLY',
        board_document_identifier='SYNTHETIC',board_document_sha256='a'*64,board_io_voltage='3.3V (synthetic)')
    m=tmp_path/'board.json';m.write_text(json.dumps(p))
    lines=[f'set_io {name} {i+1}' for i,name in enumerate(p['unassigned_ports'])]
    pc=tmp_path/'pins.pcf';pc.write_text('\n'.join(lines)+'\n')
    a=approve(NET,m,pc)
    assert a['ports']==25
    assert 'SYNTACTIC_ONLY' in a['level']
def test_repeated_pin_and_missing_pin_are_rejected(tmp_path):
    p=make_manifest(NET)
    lines=[f'set_io {name} {i+1}' for i,name in enumerate(p['unassigned_ports'])]
    q=tmp_path/'dup.pcf'
    q.write_text('\n'.join(lines+[f'set_io {p["unassigned_ports"][0]} 47']))
    with pytest.raises(ValueError,match='duplicate'):parse_pcf(q)
    q.write_text('\n'.join([lines[0],lines[1].split()[0]+' '+lines[1].split()[1]+' 1']))
    with pytest.raises(ValueError,match='pin reused'):parse_pcf(q)
    p.update(status='APPROVED_BY_HARDWARE_OPERATOR',real_board_product='SYNTHETIC',
        board_document_identifier='SYNTHETIC',board_document_sha256='b'*64,board_io_voltage='SYNTHETIC')
    m=tmp_path/'approved.json';m.write_text(json.dumps(p))
    q.write_text('\n'.join(lines[:-1]))
    with pytest.raises(ValueError,match='unpinned IO'):approve(NET,m,q)
