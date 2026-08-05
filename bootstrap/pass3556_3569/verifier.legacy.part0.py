#!/usr/bin/env python3
"""Passes 3542-3555 exact radius/amplitude/code/fault/C5 closure.

The verifier rebuilds the 45-octet filled port complex from W(3,3), verifies a
new 263-term cohomology circuit and a complete two-column direction census,
constructs the exact 2+5 five-channel spectral factorization and an improved
rational witness, computes the complete duality atlas for the four frontier
binary codes, proves the minimum five-bit compound Clebsch fault locator, and
classifies restrictions of the Perkel and W33 rank-20 modules to subgroup types
inside their explicit common A5.

The covering-radius endpoint, unrestricted amplitude optimum, chromatic number,
and canonical objectwise C5 intertwiner remain open.
"""
from __future__ import annotations
import collections, hashlib, itertools, json, math
from fractions import Fraction
from pathlib import Path
import numpy as np
import sympy as sp
try:
    from numba import njit
except Exception:  # pragma: no cover - CI installs numba
    def njit(f): return f

try:
    from analysis.bt3542_3555_core import geometry, quotient_generators, rref
except ImportError:
    from bt3542_3555_core import geometry, quotient_generators, rref

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_BT3542_BT3555_RADIUS_AMPLITUDE_CODE_FAULT_C5_results.json'

# Frozen exact relation found by deterministic basis exchange. The verifier
# reconstructs the generator matrix and checks this full relation directly.
RADIUS_SUPPORT=[2,3,5,8,12,13,15,18,20,21,23,24,27,32,33,35,36,40,41,42,43,46,51,54,55,62,71,74,75,81,82,84,85,87,90,94,95,97,98,99,101,102,105,107,112,114,118,119,120,123,125,126,129,132,137,139,140,146,147,155,157,160,161,164,168,169,172,173,174,178,179,180,182,183,187,188,191,192,194,203,204,207,212,213,215,221,227,228,230,231,232,234,236,243,244,248,250,251,254,255,257,263,265,266,271,274,277,278,280,283,288,290,292,294,298,300,306,307,312,314,315,319,323,324,330,331,335,337,338,342,349,353,355,356,358,359,361,368,370,372,377,379,381,382,385,386,390,392,394,395,396,397,400,402,404,405,409,411,418,420,421,425,426,433,436,437,442,445,446,452,455,456,460,464,469,470,476,479,480,481,491,495,499,502,504,509,512,513,514,516,530,532,536,543,544,548,550,555,556,560,562,563,564,567,569,571,573,578,580,586,589,590,592,593,595,598,603,605,606,610,614,615,620,621,626,628,630,633,637,639,644,646,650,653,654,655,657,659,660,661,664,665,667,668,670,674,676,677,679,681,682,684,688,691,693,694,698,702,705,707,709,713,714]
RADIUS_COEFFS=[2,1,2,2,2,2,2,1,2,1,2,2,2,2,1,2,2,1,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,2,1,2,1,1,2,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1,1,2,1,2,1,1,2,1,1,2,1,1,1,1,1,1,2,2,2,1,2,2,2,1,2,2,2,2,1,2,2,1,2,2,1,2,2,2,1,2,2,2,1,2,2,2,2,2,2,2,1,2,2,2,2,1,1,1,1,2,1,1,1,1,2,1,2,1,1,1,1,1,1,1,1,1,2,1,1,2,1,2,2,2,2,1,2,2,2,2,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,2,1,2,2,1,2,2,2,2,2,2,1,2,1,2,2,2,1,2,2,2,1,1,1,1,2,2,2,2,2,2,2,2,2,2,1,1,2,1,1,1,2,1,2,1,1,1,2,1,1,1,1,2,2,2,2,2,2,1,2,1,2,2,1]
RADIUS_HASH='d22f3661c1b2ab8e96936a693b887d2539c83fa9bd683b8465cbf900ce025fb8'

CODES={
'13_5_5':[3,5,6,7,8,16,24,9,12,18,20,25,26],
'16_5_8':[1,2,4,7,9,12,18,20,25,26,10,17,28,15,23,31],
'24_5_11':[1,2,4,3,5,6,8,16,24,9,12,18,20,25,26,10,17,28,13,22,27,15,23,31],
'28_5_14':[1,2,4,7,8,16,24,9,12,18,20,25,26,10,17,28,11,14,19,21,29,30,13,22,27,15,23,31],
}
FAULT_LABELS=[0,0,0,0,30,25,0,7,0,27,13,22,14,18,29,1]


def semantic_hash(data):
    body=dict(data);body.pop('semantic_sha256',None)
    return hashlib.sha256(json.dumps(body,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def radius_certificate(geo,G):
    rel=np.zeros(720,dtype=np.int8);rel[RADIUS_SUPPORT]=RADIUS_COEFFS
    assert int(np.count_nonzero(rel))==263 and hashlib.sha256(bytes(rel)).hexdigest()==RADIUS_HASH
    assert not np.any((G@rel)%3)
    # Make the 263-relation fundamental by taking 262 support columns first,
    # then extending them deterministically to a basis.
    extra=2;supp=[x for x in RADIUS_SUPPORT if x!=extra]
    assert len(rref(G[:,supp])[1])==262
    order=supp+[i for i in range(720) if i not in set(supp)]
    _,piv=rref(G[:,order]);bb=[order[i] for i in piv[:436]]
    assert len(bb)==436 and extra not in bb and all(x in bb for x in supp)
    aug=np.concatenate([G[:,bb],G],axis=1);red,piv=rref(aug);assert piv[:436]==list(range(436))
    TT=red[:,436:];non=np.array([i for i in range(720) if i not in set(bb)],dtype=int)
    state_to_dir=np.array([-1,0,0,1,2,3,1,3,2],dtype=np.int8)
    max_union=max_dirs=max_direction=0;four=0;cap_hist=collections.Counter();candidate_434=0;bestrow=None;pairs=0
    for ii,a in enumerate(non):
        ca=TT[:,a].astype(np.int16);bs=non[ii+1:]
        if not len(bs):continue
        codes=3*ca[:,None]+TT[:,bs]
        for jj,b in enumerate(bs):
            bc=np.bincount(codes[:,jj],minlength=9)
            counts=[int(bc[np.where(state_to_dir==d)[0]].sum()) for d in range(4)]
            zero=int(bc[0]);union=436-zero;nz=sum(c>0 for c in counts);cap=sum((c+241)//242 for c in counts if c)
            pairs+=1;cap_hist[cap]+=1;candidate_434+=int(cap>=4)
            max_union=max(max_union,union);max_dirs=max(max_dirs,nz);max_direction=max(max_direction,max(counts));four+=int(nz==4)
            row=(union,-cap,counts,zero,int(a),int(b))
            if bestrow is None or row>bestrow:bestrow=row
    assert pairs==40186 and max_union==319 and max_dirs==3 and four==0 and max_direction==264
    assert dict(cap_hist)=={2:34119,3:5277,4:790}
    # Exact rank-three pilot on the 64 heaviest nonbasis columns in this basis.
    weights=np.count_nonzero(TT[:,non],axis=0)+1;pick=np.argsort(-weights,kind='stable')[:64];selected=non[pick]
    pmap=np.full(27,-1,dtype=np.int8);reps={}
    for aa,zz,cc in itertools.product(range(3),repeat=3):
        if aa==zz==cc==0:continue
        v=(aa,zz,cc);f=next(x for x in v if x);inv=1 if f==1 else 2;rep=tuple(inv*x%3 for x in v)
        if rep not in reps:reps[rep]=len(reps)
        pmap[9*aa+3*zz+cc]=reps[rep]
    assert len(reps)==13
    triple_count=0;triple_max_union=triple_max_dirs=triple_max_pop=0;triple_cap=collections.Counter();triple_best=None
    for ia in range(62):
        a=int(selected[ia]);ca=TT[:,a].astype(np.int16)
        for ib in range(ia+1,63):
            b=int(selected[ib]);base3=9*ca+3*TT[:,b]
            for ic in range(ib+1,64):
                c=int(selected[ic]);bc=np.bincount(base3+TT[:,c],minlength=27)
                counts=[int(bc[np.where(pmap==d)[0]].sum()) for d in range(13)]
                zero=int(bc[0]);union=436-zero;nd=sum(x>0 for x in counts);mx=max(counts);cap=sum((x+241)//242 for x in counts if x)
                triple_count+=1;triple_cap[cap]+=1;triple_max_union=max(triple_max_union,union);triple_max_dirs=max(triple_max_dirs,nd);triple_max_pop=max(triple_max_pop,mx)
                row=(union,nd,-cap,counts,zero,a,b,c)
                if triple_best is None or row>triple_best:triple_best=row
    assert triple_count==41664 and triple_max_union==360 and triple_max_dirs==6 and triple_max_pop==253
    assert dict(triple_cap)=={3:544,4:3383,5:10325,6:27407,7:5}
    return {'flat_dimension':480,'coboundary_rank':44,'cohomology_dimension':436,'generator_columns':720,
      'new_circuit_weight':263,'relation_sha256':RADIUS_HASH,'fundamental_extra_column':extra,
      'pair_census':pairs,'maximum_union_support':max_union,'maximum_occupied_PG1_directions':max_dirs,
      'four_direction_pairs':four,'maximum_direction_population':max_direction,
      'adversarial_cancellation_cap_histogram':{str(k):v for k,v in sorted(cap_hist.items())},
