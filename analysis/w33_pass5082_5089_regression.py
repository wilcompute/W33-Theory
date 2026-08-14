#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
J=json.loads((R/'data/PART_W33_PASS5082_5089_RESULTS.json').read_text())
assert J['status']=='PASS_WITH_ALL_Q_DISTANCE_AND_Q4_HEAVY_SHELL_OPEN'
assert J['5082']['fourier_max']=={'q2':'29/45','q3':'9/10','q4':'409/425'}
assert J['5083']['active_chart_minimum']==108 and J['5083']['equality_witness_weight']==81
assert J['5084']['generator_dependency_code']==[425,169,5] and J['5084']['A5']==170
assert J['5085']['V11']=='point theta' and J['5085']['V12_standard']=='line theta'
assert J['5086']['double_errors']==1311390 and J['5086']['double_failures']==0
assert J['5086']['one_sweep_triples']+J['5086']['two_sweep_local_cut_triples']==21600
assert J['5087']['generated_dimension']==30 and J['5087']['discriminant']==68
assert J['5088']['K4_cliques']==114480 and J['5088']['selected_tetrahedral_K4s']==1080 and J['5088']['exact_match']
assert J['5089']['torsion_free'] and J['5089']['q2_signed_theta_rank']==74
# Cross-packet reconciliation: 5090 forces q4 exotic minima into heavy charts.
P=R/'analysis/PASS5090_5097_EXECUTED_OUTCOMES.md'
if P.exists():
    s=P.read_text();assert 'heavy-chart' in s or 'heavier' in s
print('PASS 5082-5089')
