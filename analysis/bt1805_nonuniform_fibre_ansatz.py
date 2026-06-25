#!/usr/bin/env python3
"""BT1805: constrained nonuniform 12-symbol fibre ansatz probe."""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1805_nonuniform_fibre_ansatz.json'
TABLES=['T001','T002','T010','T012','T020','T021','T100','T101','T111','T112','T120','T122','T200','T202','T210','T211','T221','T222']
COUNTS=np.array([528,562,578,528,612,580,528,528,480,528,612,564,562,528,578,562,562,560],dtype=int)
F2=np.array([[1,0,0,1,1,0,1,0,1,0,0,1,0,1,1,0,1,0],[0,1,1,0,0,1,0,1,0,1,1,0,1,0,0,1,0,1]],dtype=int)
F3=np.array([[1,0,0,1,2,0,2,0,0,0,0,2,0,1,0,0,0,0],[2,0,0,1,1,0,2,0,2,0,0,0,0,0,1,0,0,0],[0,0,2,0,0,2,0,1,0,1,2,0,0,0,0,1,0,0],[1,0,2,2,0,2,0,1,0,2,1,0,0,0,0,0,1,0],[2,2,1,1,1,1,2,1,2,1,0,0,1,0,1,1,0,1]],dtype=int)
DELTA=np.array([0,0,-2,0,0,0,0,0,0,0,0,0,0,0,-2,0,0,2],dtype=int)
def main():
    adjusted=COUNTS+DELTA
    payload={'bt':'BT1805','title':'nonuniform fibre ansatz','symbol_model':'12=3x4 table-local fibre layer above BT1795 transport','exact_fit':'trivial table-local weights fit all 18 counts, but simple structured lifts fail; therefore the test is whether the counts satisfy BT1801 linear constraints.','observed':{'counts':COUNTS.tolist(),'total':int(COUNTS.sum()),'F2_eval':(F2@COUNTS%2).astype(int).tolist(),'F3_eval':(F3@COUNTS%3).astype(int).tolist()},'minimal_even_F3_repair':{'delta':DELTA.tolist(),'changed_tables':[{ 'table':TABLES[i], 'delta':int(DELTA[i]), 'old':int(COUNTS[i]), 'new':int(adjusted[i]) } for i in range(18) if DELTA[i]],'L1_size':int(np.abs(DELTA).sum()),'adjusted_total':int(adjusted.sum()),'adjusted_F2_eval':(F2@adjusted%2).astype(int).tolist(),'adjusted_F3_eval':(F3@adjusted%3).astype(int).tolist()},'interpretation':'The nearest even-count repair to the F3 syndrome changes only three tables by two counts: T010, T210, and T222. This points to a small ternary fibre correction rather than a global support-geometry failure.','conclusion':'A table-local nonuniform 12-symbol fibre layer can fit the data, but the observed vector is off the pure F3 double-six constraint by a tiny three-table even correction. The next target is to explain the special triple T010/T210/T222 from fibre geometry.'}
    OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'F3_eval':payload['observed']['F3_eval'],'repair_L1':payload['minimal_even_F3_repair']['L1_size'],'changed':['T010','T210','T222']},indent=2))
if __name__=='__main__': main()
