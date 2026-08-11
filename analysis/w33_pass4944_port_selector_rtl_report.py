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
    out={'pass':4944,
      'logic':'45 parallel realizations of i -> (-1)^b i + r mod 3, r in F3 and b in F2',
      'encoding':{'live_port_bus_bits':90,'selector_rotation_bits':90,'selector_reflection_bits':45,
        'independent_binary_selector_state_bits':135,'native_mixed_radix':'45 trits + 45 bits',
        'information_theoretic_global_minimum_bits_from_Pass4872':117},
      'verification':{'iverilog':'exhaustive 18/18 valid input/state combinations for one selector plus a deterministic all-45-lane mixed vector',
        'yosys_single_selector':one,'yosys_45_parallel':all45,
        'cell_scaling_ratio':all45['num_cells']/one['num_cells']},
      'compiler_boundary':{'table_free_combinational_decode':True,
        'stores_117_bit_globally_packed_table':False,
        'reason':'This is the physically local 45-selector mixed-radix realization; a 117-bit arbitrary global-table codec would require a separate variable-length/global decoder.'},
      'theorem':'The Pass4872 AGL(1,3) port matching now has a literal synthesizable datapath. A one-selector block exhaustively realizes all six local permutations on all three valid ports, and 45 copies operate in parallel from the native 45-trit + 45-bit selector state. Yosys synthesis supplies an actual generic-cell cost for both one selector and the complete 45-way fabric rather than an information-only estimate.',
      'boundary':'RTL/synthesis theorem for the local permutation fabric only. It does not prove optical insertion loss, FPGA timing/placement, or that the information-theoretic 117-bit global encoding can be decoded at the same hardware cost.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
