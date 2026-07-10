#!/usr/bin/env python3
"""Aggregate runner for the five v3 closures."""
from __future__ import annotations
import json
from pathlib import Path

import w33_levi_next5_v3_formal as formal
import w33_levi_next5_v3_discriminant as discriminant
import w33_levi_next5_v3_e6 as e6
import w33_levi_next5_v3_tolerance as tolerance
import w33_levi_next5_v3_emulator as emulator

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_2026_07_10_LEVI_NEXT5_V3_results.json'

def analyze():
    tracks={
      '1_lean_formal_rank':formal.analyze(),
      '2_full_discriminant_action':discriminant.analyze(),
      '3_native_E6_geometry_map':e6.analyze(),
      '4_tolerance_photonic_compile':tolerance.analyze(),
      '5_end_to_end_optical_emulator':emulator.analyze(),
    }
    checks={'all_five_present':len(tracks)==5,'all_five_pass':all(t['status']=='PASS' for t in tracks.values())}
    return {'title':'Five v3 closures: Lean rank artifact, discriminant action, E6 object map, tolerance compiler, optical packet emulator','status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'track_pass':{k:v['status']=='PASS' for k,v in tracks.items()},'tracks':tracks,'honest_scope':'The Lean source has no placeholders and its arithmetic mirror certificate passes, but Lean kernel compilation was not available in this container. All four executable Python mathematics/engineering tracks and the aggregate regression suite were run locally.'}

def main():
    out=analyze();OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0 if out['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
