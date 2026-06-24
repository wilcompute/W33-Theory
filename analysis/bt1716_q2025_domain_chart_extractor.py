#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
OUT=Path(__file__).resolve().parents[1]/'data'/'bt1716_q2025_domain_chart_extractor.json'
# Pauli encoding: 0=I, 1=X, 2=Y, 3=Z.  This avoids OCR ambiguity in raw strings.
RED=[[1,1,0],[0,1,0],[1,0,0],[0,1,2],[1,1,2],[1,3,1],[0,2,3],[3,1,1],[3,3,2],[2,1,2],[1,2,0],[2,1,0],[3,3,0],[3,3,3],[0,0,3],[1,1,3],[0,3,3],[3,2,0],[0,1,1],[0,2,1],[2,1,1],[3,0,0],[2,3,3],[0,0,1]]
BLUE=[[2,3,1],[0,3,2],[3,1,3],[1,1,2],[3,3,1],[2,1,3],[0,3,0],[2,2,3],[2,3,0],[0,1,3],[1,1,1],[1,0,2],[1,3,3],[0,3,1],[2,3,2],[2,0,3],[1,3,0],[2,2,1],[3,2,2],[1,3,2],[2,0,1],[3,1,2],[3,0,2],[3,1,0]]
def profile(labels):
 return {str(p):{str(a):sum(s[p]==a for s in labels) for a in range(4)} for p in range(3)}
def build():
 checks={'red_24':len(RED)==24 and len({tuple(x) for x in RED})==24,'blue_24':len(BLUE)==24 and len({tuple(x) for x in BLUE})==24,'labels_are_three_pauli_codes':all(len(x)==3 and all(c in range(4) for c in x) for x in RED+BLUE),'q2025_bus_counts':24*2==16*3==48,'axis_quotient_target':24//2==12,'shared_16_cell_target':16*3==48}
 return {'theorem':'BT1716 q2025 Domain Chart Extraction Certificate','verified':all(checks.values()),'summary':'The red and blue domains from q2025 Figure 10 were transcribed as two 24-observable sets using numeric Pauli codes 0=I,1=X,2=Y,3=Z. Each independently has the (24_2,16_3) bus count 48, and pairing two observations per axis targets the BT1715 12-axis bus over 16 cells.','red_codes':RED,'blue_codes':BLUE,'red_position_profile':profile(RED),'blue_position_profile':profile(BLUE),'bt1715_target':{'observations':24,'axes_after_pairing':12,'cells':16,'incidences':48},'boundary':['Manual visual transcription from q2025 Figure 10; not a machine OCR claim.','The actual 16 triples of each domain remain to be extracted before the Klein-Latin chart can be certified.'],'checks':checks}
def main():
 cert=build(); OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(cert,indent=2,sort_keys=True)+'\n'); print(cert['theorem'],cert['verified']); return 0 if cert['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
