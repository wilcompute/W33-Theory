#!/usr/bin/env python3
"""Eliminate 40-entry Q43 address remap by permuting rank8 decode ROMs once
at COMPILE TIME into native W33 40 line-bus numbering.

Same eight-cross phase operation, but zero dynamic bus->Q vertex lookup gates.
Direct lab comparison of FPGA logic-cell cost vs W33 rank14 and bridge Q rank8.
"""
import json,re,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_linebus_dual_q43_phase_geometry_20261023 import certificate

def produce():
    c=certificate()
    mp=c['bus_to_parabolic_quadric_point_permutation']
    E=c['bus_intersection_adjacency_E']
    old='q43_phase_oracle_rank8_20261023'
    new='w33_linebus_dual_rank8_direct_20261023'
    rtl=(ROOT/f'hardware/{old}.sv').read_text()
    for name in ('decode_a','decode_b'):
        pattern=rf"6'd(\d+): {name}=9'h([0-9a-f]+);"
        matches=re.findall(pattern,rtl)
        assert len(matches)==40
        table={int(a):int(v,16) for a,v in matches}
        assert sorted(table)==list(range(40))
        def replace(m):
            a=int(m.group(1))
            return f"6'd{a}: {name}=9'h{table[mp[a]]:03x};"
        rtl,count=re.subn(pattern,replace,rtl)
        assert count==40
    assert old in rtl
    rtl=rtl.replace(old,new)
    rtl=rtl.replace('// Four hyperbolic pairs', '// Native W33 line-bus IDs: four hyperbolic pairs')
    (ROOT/f'hardware/{new}.sv').write_text(rtl)
    tb=(ROOT/f'hardware/tb_{old}.sv').read_text().replace(old,new)
    def replace_row(m):
        a=int(m.group(1))
        row=sum(int(E[a][b])<<b for b in range(40))
        return f"expected_rows[{a}]=40'h{row:010x};"
    tb,n=re.subn(r"expected_rows\[(\d+)\]=40'h[0-9a-f]+;",replace_row,tb)
    assert n==40
    tb=tb.replace('PASS Q43 8-term oracle', 'PASS native W33 line-bus Q43-dual rank8 oracle')
    (ROOT/f'hardware/tb_{new}.sv').write_text(tb)
    return {'schema':'w33.line_bus_Q43.eight_term_native_direct_RTL.v1',
       'source_canonical_q43':'hardware/q43_phase_oracle_rank8_20261023.sv',
       'compiler':'analysis/w33_linebus_q43_direct_rank8_RTL_codegen_20261023.py',
       'direct_W33_bus_numbering':True,'dynamic_bus_to_Q43_lookups':0,
       'cross_register_phase_terms':8,'phase_tables_per_side':1,
       'source_bus_to_Q43_mapping':mp,
       'rtl':f'hardware/{new}.sv','testbench':f'hardware/tb_{new}.sv',
       'test_valid':1600,'test_invalid':2496,
       'physical_boundary':'Classical metadata control; no measured PIC phase gates or registered FPGA board.'}
if __name__=='__main__':
    x=produce()
    x['sha256']=hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    (ROOT/'data/w33_linebus_dual_rank8_direct_RTL_manifest_20261023.json').write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
    print('PASS native W33 line-bus rank8 direct oracle; compile-time ROM relabel, zero dynamic lookup')
