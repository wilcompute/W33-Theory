#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ONE=ROOT/'analysis/PASS4944_ONE_YOSYS_STAT.json';ALL=ROOT/'analysis/PASS4944_45_YOSYS_STAT.json'
OUT=ROOT/'data/PART_W33_PASS4944_PORT_SELECTOR_RTL.json'

def module_stat(path,needle):
    d=json.loads(path.read_text());mods=d['modules'];key=next(k for k in mods if needle in k);m=mods[key]
    return {'module_key':key,'num_cells':int(m.get('num_cells',0)),'num_wires':int(m.get('num_wires',0)),
            'num_wire_bits':int(m.get('num_wire_bits',0)),'cell_types':{k:int(v) for k,v in m.get('num_cells_by_type',{}).items()}}

def main()->int:
    one=module_stat(ONE,'w33_agl13_port_selector');all45=module_stat(ALL,'w33_port_selector45')
    assert one['num_cells']>0 and all45['num_cells']>0
    out=json.loads(OUT.read_text()) if OUT.exists() else {'pass':4944}
    out['synthesis']={
      'status':'COMPLETE',
      'yosys_single_selector':one,
      'yosys_45_parallel':all45,
      'cell_scaling_ratio':all45['num_cells']/one['num_cells'],
      'iverilog_log':'analysis/PASS4944_IVERILOG.log',
      'one_selector_stat':'analysis/PASS4944_ONE_YOSYS_STAT.json',
      'parallel45_stat':'analysis/PASS4944_45_YOSYS_STAT.json'}
    out['theorem']=('The Pass4872 AGL(1,3) port matching has a literal 45-way synthesizable RTL datapath. '
      'Algebraic exhaustive evaluation realizes all six local permutations with no local collisions, and the '
      'completed Icarus/Yosys evidence now supplies actual generic-cell counts for one selector and the complete '
      '45-way parallel fabric. The local independently addressable control state remains 135 bits versus the 117-bit '
      'global information optimum.')
    out['boundary']=('RTL/synthesis theorem for the local permutation fabric only. It does not prove optical insertion loss, '
      'device timing/placement, or that a globally packed 117-bit arbitrary table can be decoded at the same hardware cost.')
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
