#!/usr/bin/env python3
"""Pass 409: minimal-support compact-E8 two-control witness."""
from __future__ import annotations
import importlib.util, json
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20260923_compact_e8_sparse8.json"

def load(path,name):
    s=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

dw=load(ROOT/"analysis/w33_diagonal_weld_e8_lie_generation.py","dw")
ri=load(ROOT/"analysis/w33_e8_split_real_form_involution.py","ri")
compiler,bridge,table=dw.load_inputs()
amps=dw.backgrounds(bridge); vecs=dw.source_generators(compiler,amps)
sc=json.loads((ROOT/"artifacts/e8_structure_constants_w33_discrete.json").read_text())
roots=[tuple(map(int,r)) for r in sc["basis"]["roots"]]
rmap={r:8+i for i,r in enumerate(roots)}
neg={8+i:rmap[tuple(-x for x in r)] for i,r in enumerate(roots)}

phase={}
for a in range(8,248):
    k=ri.killing(sc,a,neg[a]); assert k in (-60,60)
    phase[a]=-1 if k>0 else 1

def compact_partner(v):
    y=[0]*248
    for a,x in enumerate(v):
        if not x: continue
        if a<8: y[a]-=x
        else: y[neg[a]]+=phase[a]*x
    return y

support=[16,19,23,31,153,190,216,228]
other_witnesses=[
    [204,44,176,45,31,26,187,216],
    [12,132,136,147,189,194,204,219],
    [15,19,31,38,48,132,200,205],
    [14,23,159,165,168,190,219,234],
]
base=vecs[(1,"plus")]
x=[0]*248
for i in support: x[i]=base[i]
y=compact_partner(x)

def root_det(S):
    return int(sp.Matrix([roots[i-8] for i in S]).det())

determinants={",".join(map(str,S)):root_det(S)
              for S in [support]+other_witnesses}
assert all(abs(v)==1 for v in determinants.values())

modular={}
for p in (103,109):
    b,_=dw.closure((x,y),table,dw.ModularBasis(p),p)
    modular[str(p)]={
        "dimension":len(b.rows),
        "grading":dw.grade_counts(sorted(b.rows),compiler),
        "depth":max(b.depths),
    }
    assert len(b.rows)==248

exact,events=dw.closure((x,y),table,dw.RationalBasis())
assert len(exact.rows)==248
assert dw.grade_counts(sorted(exact.rows),compiler)=={"g0":86,"g1":81,"g2":81}
g1=compiler["coordinate_maps"]["grade1_source_indices"]
g2=compiler["coordinate_maps"]["grade2_source_indices"]
positions=[g1.index(i) for i in support]

out={
    "schema":"w33.20260923.compact_e8_sparse8.v1",
    "status":"PASS_MINIMAL_EIGHT_ROOT_COMPACT_E8_CONTROL",
    "architecture":"x plus exact compact-conjugate partner sigma_c(x)",
    "support":support,
    "grade1_positions":positions,
    "grade2_partner_indices":[g2[j] for j in positions],
    "amplitudes":[x[i] for i in support],
    "roots":[list(roots[i-8]) for i in support],
    "compact_partner_phase_signs":[phase[i] for i in support],
    "selected_root_determinant":root_det(support),
    "independent_unimodular_witness_determinants":determinants,
    "modular_replays":modular,
    "exact_Q":{"dimension":len(exact.rows),
               "grading":dw.grade_counts(sorted(exact.rows),compiler),
               "depth":max(exact.depths),"events":events},
    "lower_bound":{
        "minimum_support":8,
        "reason":"With k selected roots and their negatives, every generated root lies in their root-lattice span, so generated Cartan rank is at most k; rank(E8)=8."
    },
    "upper_bound":"The displayed 8-root unimodular witness closes exactly to all 248 dimensions over Q.",
    "boundary":"Minimality is for this root-supported compact-conjugate two-control architecture; it is not a lower bound on arbitrary dense laboratory Hamiltonian parameterizations."
}
OUT.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"status":out["status"],"support":support,
                  "det":out["selected_root_determinant"],
                  "exact_dim":out["exact_Q"]["dimension"]},indent=2))
