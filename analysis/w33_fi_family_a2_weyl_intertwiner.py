#!/usr/bin/env python3
"""Explicit Weyl intertwiner from the physical FI A2 to the canonical CE2/family A2.

Both objects are reconstructed inside the SAME doubled-coordinate E8 root
system.  The physical FI element is the recorded organizer-E8 Cartan vector
from w33_physical_fi_e6_a2_z3_grading.py.  The canonical family A2 is the
mark-3 CE2 A2 of Pass7081-7096.

A breadth-first search over the finite orbit of A2 subsystems under the eight
simple E8 reflections finds an explicit 23-reflection Weyl word.  Stronger
than mapping the six A2 roots, that word intertwines all 240 root grades:
physical FI grades 0,1,2 map exactly to canonical CE2 grades 0,1,2.
"""
from __future__ import annotations
import importlib.util, json, sys
from collections import Counter, deque
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_fi_family_a2_weyl_intertwiner.json"
EXPECTED_WORD=(2,1,4,6,0,1,2,3,7,1,0,2,1,3,4,5,6,0,7,1,2,3,4)

def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path); assert spec and spec.loader
    m=importlib.util.module_from_spec(spec); sys.modules[name]=m; spec.loader.exec_module(m); return m

def components(roots,dot):
    roots=list(roots); rem=set(range(len(roots))); out=[]
    while rem:
        i=rem.pop(); C=[i]; st=[i]
        while st:
            u=st.pop()
            ns=[v for v in list(rem) if dot(roots[u],roots[v])!=0]
            for v in ns: rem.remove(v); C.append(v); st.append(v)
        out.append([roots[i] for i in C])
    return out

def main(write=True):
    old=load(ROOT/"analysis/w33_pass7081_7096_e8_z3_z4_z12_common_refinement.py","old_z3a2")
    fi=load(ROOT/"analysis/w33_physical_fi_e6_a2_z3_grading.py","physical_fi_a2")
    R=old.e8_roots_doubled(); h=(1,3,9,27,81,243,729,2187)
    simp=old.simple_roots(R,h); assert len(simp)==8
    cm=old.coeff_map(R,simp)
    canon_neutral=[r for r in R if cm[r][4]%3==0]
    canon_a2=next(c for c in components(canon_neutral,old.dot) if len(c)==6)

    t=fi.lin(fi.A4,fi.COEFF)
    def pgrade(r):
        z=sum(t[i]*F(r[i],2) for i in range(8))%1
        return int(3*z)%3
    phys_neutral=[r for r in R if pgrade(r)==0]
    phys_a2=next(c for c in components(phys_neutral,old.dot) if len(c)==6)
    assert set(phys_a2)!=set(canon_a2)

    def refl(x,a):
        q=old.dot(x,a); assert q%4==0; k=q//4
        return tuple(x[i]-k*a[i] for i in range(8))
    start=frozenset(phys_a2); target=frozenset(canon_a2)
    q=deque([start]); prev={start:(None,None)}
    while q:
        S=q.popleft()
        if S==target: break
        for gi,a in enumerate(simp):
            N=frozenset(refl(x,a) for x in S)
            if N not in prev: prev[N]=(S,gi); q.append(N)
    assert target in prev
    word=[]; cur=target
    while prev[cur][0] is not None:
        p,gi=prev[cur]; word.append(gi); cur=p
    word=tuple(reversed(word))
    assert word==EXPECTED_WORD

    def act(x):
        for gi in word: x=refl(x,simp[gi])
        return x
    assert frozenset(act(x) for x in start)==target

    pair=Counter()
    for r in R:
        pair[(pgrade(r),cm[act(r)][4]%3)]+=1
    assert pair==Counter({(0,0):78,(1,1):81,(2,2):81})

    out={
      "schema":"w33.fi_family_a2_weyl_intertwiner.v1",
      "status":"PASS_EXPLICIT_FI_TO_CE2_FAMILY_A2_WEYL_INTERTWINER",
      "headline":"A concrete E8 Weyl word of 23 simple reflections maps the six-root A2 selected by the physical FI Cartan element to the repository's canonical CE2/family A2. The same word intertwines all 240 root grades exactly: 78 neutral roots and the two 81-root sectors map grade-for-grade without inversion.",
      "simple_roots_doubled":[list(r) for r in simp],
      "weyl_word_zero_based":list(word),
      "weyl_word_one_based":[i+1 for i in word],
      "word_length":len(word),
      "physical_A2_roots_doubled":[list(r) for r in sorted(start)],
      "canonical_family_A2_roots_doubled":[list(r) for r in sorted(target)],
      "grade_intertwining":{"0->0":78,"1->1":81,"2->2":81},
      "A2_orbit_states_seen":len(prev),
      "interpretation":"The physical FI-selected external SU(3) and the canonical CE2/family SU(3) are not merely abstract A2 systems: they are explicitly Weyl-conjugate in the shared E8 root gauge.",
      "boundary":"This is an E8 root/Cartan intertwiner. It does not identify the separate affine nine-site Lie su(3) of Pass5686/5696 with the family factor; that remains a different intertwiner problem.",
      "checks":{"six_roots_to_six_roots":True,"word_frozen":True,"all_240_grades_intertwined":True}}
    if write: OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({k:out[k] for k in ("status","word_length","weyl_word_zero_based","grade_intertwining")},indent=2))
    return out
if __name__=="__main__": main(True)
