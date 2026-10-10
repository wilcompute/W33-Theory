#!/usr/bin/env python3
"""Pass 2957: parse same-harness Yosys/nextpnr reports and make the role decision."""
from __future__ import annotations
import argparse,json,re
from pathlib import Path

def cells(text):
    patterns=[r'Number of cells:\s+(\d+)',r'ICESTORM_LC:\s+(\d+)']
    for pattern in patterns:
        hits=re.findall(pattern,text)
        if hits:return int(hits[-1])
    raise AssertionError('logic-cell count absent')
def fmax(text):
    patterns=[r'Max frequency for clock[^:]*:\s*([0-9.]+)\s*MHz',r'([0-9.]+)\s*MHz']
    for pattern in patterns:
        hits=re.findall(pattern,text)
        if hits:return float(hits[-1])
    raise AssertionError('maximum frequency absent')
def main():
    p=argparse.ArgumentParser();p.add_argument('--rank-yosys',required=True);p.add_argument('--base-yosys',required=True)
    p.add_argument('--rank-pnr',required=True);p.add_argument('--base-pnr',required=True);p.add_argument('--output',required=True)
    a=p.parse_args()
    rank={'logic_cells':cells(Path(a.rank_yosys).read_text()),'fmax_mhz':fmax(Path(a.rank_pnr).read_text())}
    base={'logic_cells':cells(Path(a.base_yosys).read_text()),'fmax_mhz':fmax(Path(a.base_pnr).read_text())}
    if rank['logic_cells']<base['logic_cells'] and rank['fmax_mhz']>=base['fmax_mhz']:
        role='replace_execution_core'
    elif rank['logic_cells']<base['logic_cells']:
        role='compressed_context_memory_only_pending_timing_budget'
    elif rank['logic_cells']>=base['logic_cells'] and rank['fmax_mhz']<base['fmax_mhz']:
        role='reject_execution_encoding_retain_storage_theorem'
    else:
        role='context_memory_candidate_not_execution_replacement'
    out={'schema':'w33.pass2957.rank7_hardware_verdict.v1','status':'OBSERVED_SAME_HARNESS_PNR',
      'rank7':rank,'arithmetic_baseline':base,
      'delta':{'logic_cells':rank['logic_cells']-base['logic_cells'],'fmax_mhz':rank['fmax_mhz']-base['fmax_mhz']},
      'role_decision':role,
      'boundary':'One selected iCE40 device, package, harness and toolchain; not a device-independent hardware theorem.'}
    Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
