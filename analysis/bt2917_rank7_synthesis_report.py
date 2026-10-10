#!/usr/bin/env python3
"""Parse observed Yosys/nextpnr evidence for Pass 2917."""
from __future__ import annotations
import argparse,json,re
from pathlib import Path

def cells(text):
    hits=re.findall(r'Number of cells:\s+(\d+)',text)
    if not hits:raise AssertionError('Yosys cell count not found')
    return int(hits[-1])
def fmax(text):
    hits=re.findall(r'Max frequency for clock[^:]*:\s*([0-9.]+)\s*MHz',text)
    if not hits:raise AssertionError('nextpnr max frequency not found')
    return float(hits[-1])
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--rank-yosys',required=True);ap.add_argument('--base-yosys',required=True)
    ap.add_argument('--rank-pnr',required=True);ap.add_argument('--base-pnr',required=True);ap.add_argument('--output',required=True)
    a=ap.parse_args();rank={'logic_cells':cells(Path(a.rank_yosys).read_text()),'fmax_mhz':fmax(Path(a.rank_pnr).read_text())}
    base={'logic_cells':cells(Path(a.base_yosys).read_text()),'fmax_mhz':fmax(Path(a.base_pnr).read_text())}
    out={'schema':'w33.pass2917.rank7_synthesis_comparison.v1','status':'OBSERVED_REMOTE_PNR',
         'rank7':rank,'baseline_four_trit':base,
         'delta':{'logic_cells':rank['logic_cells']-base['logic_cells'],'fmax_mhz':rank['fmax_mhz']-base['fmax_mhz']},
         'interpretation':('rank-coded engine wins area' if rank['logic_cells']<base['logic_cells'] else 'rank-coded engine does not win area'),
         'boundary':'One iCE40UP5K SG48 harness and toolchain; not a device-independent hardware law.'}
    Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
