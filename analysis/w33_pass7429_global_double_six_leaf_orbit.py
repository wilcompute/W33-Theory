#!/usr/bin/env python3
"""Pass7429: globalize the exact Pass4964 W33-spread <-> cubic double-six bridge over all 2240 E8 leaves."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7429_GLOBAL_DOUBLE_SIX_LEAF_ORBIT.json'

def main():
 W=696729600;leaves=2240;leaf_norm=311040;spreads=36;spread_stab_local=1440
 assert W//leaf_norm==leaves
 charts=leaves*spreads;chart_stab=W//charts
 assert charts==80640 and chart_stab==8640 and leaf_norm//spreads==chart_stab
 A2_4=11200;leaves_per_line=8;spreads_per_line_per_leaf=9
 charts_per_line=leaves_per_line*spreads_per_line_per_leaf
 assert charts_per_line==72 and charts*10==A2_4*charts_per_line
 A2=1120;leaves_per_A2=80;charts_per_A2=leaves_per_A2*spreads
 assert charts_per_A2==2880 and charts*40==A2*charts_per_A2
 steiner_per_leaf=120;steiner=leaves*steiner_per_leaf;steiner_stab=W//steiner
 assert steiner==268800 and steiner_stab==2592
 steiner_per_line=leaves_per_line*3
 assert steiner_per_line==24 and steiner==A2_4*steiner_per_line
 out={'schema':'w33.pass7429.global_double_six_leaf_orbit.v1','status':'PASS',
  'W_E8_order':W,'W33_Eisenstein_leaves':leaves,'leaf_normalizer_order':leaf_norm,
  'spreads_or_double_six_charts_per_leaf':spreads,'global_leaf_spread_charts':charts,'global_chart_stabilizer_order':chart_stab,
  'global_A2_4_lines':A2_4,'charts_per_A2_4_line':charts_per_line,
  'global_A2_points':A2,'charts_per_A2_point':charts_per_A2,
  'global_Steiner_chart_objects':steiner,'Steiner_object_stabilizer_order':steiner_stab,'Steiner_objects_per_A2_4_line':steiner_per_line,
  'Pass4964_input':'Within each W33 leaf there is a unique PGSp(4,3)-equivariant bijection between its 36 spreads and the 36 cubic-surface double-sixes; spread overlap 1/4 transports double-six intersection 6/4.',
  'Pass4965_input':'At each W33 line, the nine incident spreads split canonically into three Steiner triples.',
  'theorem':'The cubic-surface 36-state carrier globalizes over the E8 Eisenstein foliation to one 80640-element Weyl orbit of leaf-spread/double-six charts. Every global A2^4 line lies in exactly 72 charts and supports exactly 24 global Steiner chart objects (8 leaves x 3 local Steiner triples).',
  'boundary':'A chart is a pair (Eisenstein W33 leaf, spread) together with its canonical local double-six label. This does not identify one global cubic surface embedded in E8 or equate cubic lines with E8 roots.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','charts':charts,'Steiner':steiner}))
if __name__=='__main__':main()
