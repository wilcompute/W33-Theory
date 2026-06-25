#!/usr/bin/env python3
"""BT1759: E8 simple-reflection evidence for Coxeter hexagon bus limits."""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1759_e8_reflection_hexagon_fragmentation.json'
def roots():
    out=[]
    for i,j in itertools.combinations(range(8),2):
        for si in (2,-2):
            for sj in (2,-2):
                v=[0]*8; v[i]=si; v[j]=sj; out.append(tuple(v))
    for signs in itertools.product((1,-1), repeat=8):
        if signs.count(-1)%2==0: out.append(tuple(signs))
    return out
def main():
    R=roots(); RS=set(R); idx={r:i for i,r in enumerate(R)}
    def dot(v,a): return sum(x*y for x,y in zip(v,a))//4
    def basis(i,s=2):
        v=[0]*8; v[i]=s; return tuple(v)
    def sub(a,b): return tuple(x-y for x,y in zip(a,b))
    def add(a,b): return tuple(x+y for x,y in zip(a,b))
    A=[(1,-1,-1,-1,-1,-1,-1,1), add(basis(0),basis(1)), sub(basis(1),basis(0)), sub(basis(2),basis(1)), sub(basis(3),basis(2)), sub(basis(4),basis(3)), sub(basis(5),basis(4)), sub(basis(6),basis(5))]
    def refl(alpha):
        def s(v):
            c=dot(v,alpha); return tuple(v[i]-c*alpha[i] for i in range(8))
        return s
    S=[refl(a) for a in A]
    def cox(v):
        for s in S: v=s(v)
        return v
    perm=[idx[cox(r)] for r in R]
    def power(p,k):
        out=list(range(len(p)))
        for _ in range(k): out=[p[out[i]] for i in range(len(p))]
        return out
    c5=power(perm,5); seen=set(); hexes=[]
    for i in range(240):
        if i in seen: continue
        o=[]; j=i
        while j not in seen:
            seen.add(j); o.append(j); j=c5[j]
        hexes.append(o)
    hx={i:h for h,o in enumerate(hexes) for i in o}
    profiles=[]
    for si,s in enumerate(S):
        hist=Counter()
        for o in hexes:
            imgs=[idx[s(R[i])] for i in o]
            parts=Counter(hx[j] for j in imgs)
            hist[tuple(sorted(parts.values(),reverse=True))]+=1
        profiles.append({'simple_reflection':si,'fragmentation_histogram':{str(k):v for k,v in sorted(hist.items())}})
    checks={'roots_240':len(R)==240,'hexagons_40':len(hexes)==40,'all_reflections_same_13_27_profile':all(p['fragmentation_histogram']=={'(2, 2, 2)':27,'(6,)':13} for p in profiles)}
    payload={'theorem':'BT1759 E8 Reflection Hexagon Fragmentation','verified':all(checks.values()),'summary':'Simple E8 reflections do not preserve the C^5 Coxeter hexagon decomposition globally. For every Bourbaki simple reflection, 13 of the 40 C^5 hexagons map whole to hexagons, while 27 split into three 2-root fragments across Coxeter hexagons. This is actual Weyl evidence: the BT1756 Coxeter-cycle canonical form is not automatically full-Weyl natural.', 'profiles':profiles,'checks':checks,'boundary':'This tests the eight simple reflections. It shows full Weyl action fragments most Coxeter hexagons, so full Weyl-normalizer classification must use the stabilizer/normalizer of the Coxeter element rather than all W(E8).'}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'verified':payload['verified'],'profile':profiles[0]},indent=2))
    return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
