#!/usr/bin/env python3
"""Pass 1417: exact-cover orbit frontier for the 540 canonical frames.

The earlier search reported 6,579 covers as a time-capped lower bound and sampled
only stabilizers C4, C2xC2, and C4xC2.  This verifier produces deterministic
exact covers, computes their full PSp(4,3)-orbits, and certifies additional C2
and D8 stabilizer types.  It does not claim exhaustive enumeration.
"""
from __future__ import annotations

import argparse
import collections
import importlib.util
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "analysis" / "w33_pass1416_cokernel_signed_turn_intertwiner.py"
OUT = ROOT / "data" / "w33_pass1417_exact_cover_orbit_frontier.json"

EXPLICIT_REPRESENTATIVES = {
"C2":[0,15,18,25,33,41,43,51,55,59,95,97,114,119,134,135,168,172,177,185,198,205,210,218,222,256,262,278,283,285,297,305,307,321,330,345,350,368,371,380,385,391,397,401,410,414,432,464,468,488,492,494,499,501,511,512,516,529,530,533],
"C4":[0,9,23,24,37,47,55,61,85,95,99,103,111,119,122,123,132,165,174,181,206,208,216,233,237,248,252,257,281,287,297,307,314,321,328,350,356,368,369,382,390,395,403,408,413,424,430,446,449,461,466,483,487,499,503,511,521,528,531,538],
"C2xC2":[0,14,20,33,37,55,58,69,95,101,103,106,112,115,129,141,144,149,157,178,187,189,195,200,211,224,228,251,259,263,271,277,294,302,310,318,322,329,340,343,352,357,358,381,396,406,411,418,421,429,444,454,458,470,478,500,507,509,522,535],
"D8":[0,15,21,30,37,51,55,62,70,95,97,107,120,131,133,137,143,152,165,168,188,196,203,220,231,237,241,245,249,264,265,284,292,297,305,306,311,318,325,328,339,373,374,395,404,414,425,435,456,461,471,479,484,490,492,503,514,515,524,528],
"C4xC2":[0,15,21,30,37,47,55,61,80,95,99,103,115,119,122,130,132,161,170,174,181,206,209,213,227,229,241,246,248,252,259,282,287,306,311,321,326,330,350,352,357,367,386,395,411,418,441,449,454,458,459,476,479,490,502,509,511,521,530,538]
}


def load_base():
    spec = importlib.util.spec_from_file_location("pass1416", BASE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def perm_order(p):
    import math
    seen = [False]*len(p)
    ans = 1
    for i in range(len(p)):
        if not seen[i]:
            j=i; n=0
            while not seen[j]:
                seen[j]=True; n+=1; j=p[j]
            ans=math.lcm(ans,n)
    return ans


def classify_group(elems, compose):
    n=len(elems)
    orders=sorted(perm_order(g) for g in elems)
    abelian=all(compose(a,b)==compose(b,a) for a in elems for b in elems)
    if n==2: name="C2"
    elif n==4: name="C4" if 4 in orders else "C2xC2"
    elif n==8 and abelian: name="C4xC2" if 4 in orders else "C2^3"
    elif n==8: name="D8" if orders.count(2)==5 else "Q8"
    else: name=f"order{n}"
    return name,orders,abelian


def certificate():
    b=load_base()
    points,edges,lines,frames,G,M,A,N,d,K=b.build_geometry()
    lidx={L:i for i,L in enumerate(lines)}
    fidx={f:i for i,f in enumerate(frames)}
    pidx={p:i for i,p in enumerate(points)}

    def line_perm(g):
        return tuple(lidx[frozenset(g[i] for i in L)] for L in lines)
    line_actions=[line_perm(g) for g in G]

    def frame_perm(lp):
        return tuple(fidx[tuple(sorted((lp[a],lp[c])))] for a,c in frames)

    def cover_valid(cov):
        return len(cov)==60 and len(set(cov))==60 and np.all(M[list(cov)].sum(axis=0)==1)

    def stabilizer(cov):
        C=set(cov); out=[]
        for g,lp in zip(G,line_actions):
            ok=True
            for r in cov:
                a,c=frames[r]
                rr=fidx[tuple(sorted((lp[a],lp[c])))]
                if rr not in C:
                    ok=False; break
            if ok: out.append(g)
        return out

    explicit={}
    checks={}
    for expected,cov0 in EXPLICIT_REPRESENTATIVES.items():
        cov=tuple(cov0)
        checks[f"{expected}_representative_is_exact_cover"]=cover_valid(cov)
        S=stabilizer(cov)
        name,orders,abelian=classify_group(S,b.compose)
        checks[f"{expected}_stabilizer_type"]=name==expected
        C=set(cov); orbits=[]
        while C:
            r=next(iter(C)); orb=set()
            for g in S:
                lp=line_perm(g); a,c=frames[r]
                orb.add(fidx[tuple(sorted((lp[a],lp[c])))])
            orbits.append(len(orb)); C-=orb
        explicit[expected]={
            "cover":list(cov),"stabilizer_order":len(S),"element_orders":orders,
            "abelian":abelian,"group_type":name,"G_orbit_size":25920//len(S),
            "normalized_covers_through_frame0":(25920//len(S))*60//540,
            "orbits_on_cover_frames":sorted(orbits),"fixed_selected_frames":orbits.count(1)
        }

    row_masks=[]; col_rows=[[] for _ in range(240)]
    for r,row in enumerate(M):
        mask=0
        for c in np.flatnonzero(row):
            c=int(c); mask|=1<<c; col_rows[c].append(r)
        row_masks.append(mask)
    col_bits=[]
    for rows in col_rows:
        z=0
        for r in rows: z|=1<<r
        col_bits.append(z)
    conflicts=[]
    for r,row in enumerate(M):
        z=0
        for c in np.flatnonzero(row): z|=col_bits[int(c)]
        conflicts.append(z)
    ALLC=(1<<240)-1; ALLR=(1<<540)-1
    solutions=[]
    def search(covered,active,chosen):
        if len(solutions)>=16: return True
        if covered==ALLC:
            solutions.append(tuple(sorted(chosen))); return False
        rem=ALLC^covered; best=None; bestn=10**9
        x=rem
        while x:
            bit=x&-x; c=bit.bit_length()-1; x-=bit
            cand=col_bits[c]&active; n=cand.bit_count()
            if n==0:return False
            if n<bestn:
                best,bestn=cand,n
                if n==1:break
        x=best
        while x:
            bit=x&-x; r=bit.bit_length()-1; x-=bit
            if search(covered|row_masks[r],active&~conflicts[r],chosen+[r]): return True
        return False
    search(row_masks[0],ALLR&~conflicts[0],[0])
    checks["first_16_deterministic_covers_found"]=len(solutions)==16
    checks["first_16_are_exact_covers"]=all(cover_valid(c) for c in solutions)

    def transvection(v):
        vv=np.array(v,dtype=np.int64); out=[]
        for x in points:
            y=(np.array(x,dtype=np.int64)+b.om(x,v)*vv)%3
            out.append(pidx[b.norm(tuple(y))])
        return tuple(out)
    gen_vecs=[(1,1,0,2),(1,2,1,1),(1,2,2,0),(0,1,0,1)]
    point_gens=[transvection(v) for v in gen_vecs]
    frame_gens=[]
    for g in point_gens:
        fp=frame_perm(line_perm(g)); frame_gens.append(fp); frame_gens.append(b.invperm(fp))
    def transform(cov,g): return tuple(sorted(g[r] for r in cov))
    def orbit(cov):
        seen={cov}; todo=collections.deque([cov])
        while todo:
            x=todo.popleft()
            for g in frame_gens:
                y=transform(x,g)
                if y not in seen: seen.add(y); todo.append(y)
        return seen
    prior=set(); first16=[]; all_distinct=True
    for cov in solutions:
        if cov in prior:
            all_distinct=False; break
        orb=orbit(cov)
        prior |= {x for x in orb if 0 in x}
        S=stabilizer(cov); name,orders,_=classify_group(S,b.compose)
        first16.append({"cover":list(cov),"stabilizer":name,"stabilizer_order":len(S),"orbit_size":len(orb)})
    checks["first_16_lie_in_distinct_G_orbits"]=all_distinct and len(first16)==16
    checks["first_16_stabilizers_are_C2"]=all(x["stabilizer"]=="C2" for x in first16)

    five_type_bound=sum(x["G_orbit_size"] for x in explicit.values())
    combined_bound=sum(x["orbit_size"] for x in first16) + sum(explicit[t]["G_orbit_size"] for t in ("C4","C2xC2","D8","C4xC2"))
    checks["five_stabilizer_types_certified"]=set(explicit)=={"C2","C4","C2xC2","D8","C4xC2"}
    checks["combined_lower_bound_226800"]=combined_bound==226800
    checks={k:bool(v) for k,v in checks.items()}

    return {
      "schema":"w33.pass1417.exact_cover_orbit_frontier.v1",
      "status":"PASS" if all(checks.values()) else "FAIL",
      "theorem":(
        "The canonical 540-frame/240-edge exact-cover problem has at least five PSp(4,3)-orbit types, "
        "with stabilizers C2, C4, C2xC2, D8, and C4xC2. In particular the earlier sampled list was "
        "not exhaustive: C2 and D8 occur. A C2-stabilized cover fixes 12 of its selected frames, so "
        "cover stabilizers are not universally diagonal."
      ),
      "explicit_orbit_types":explicit,
      "deterministic_first16":first16,
      "lower_bounds":{
        "from_five_stabilizer_types":five_type_bound,
        "from_16_distinct_C2_orbits_plus_four_other_types":combined_bound,
        "previous_time_capped_bound":6579
      },
      "checks":checks,
      "boundary":(
        "This is a certified orbit frontier, not a complete enumeration. The exact total number of covers "
        "and the number of orbits within each stabilizer type remain open."
      )
    }


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--output",type=Path,default=OUT); ap.add_argument("--check",action="store_true"); a=ap.parse_args()
    p=certificate(); text=json.dumps(p,sort_keys=True,separators=(",",":"))+"\n"
    if a.check:
        if not a.output.exists() or a.output.read_text()!=text: raise SystemExit("Pass 1417 certificate drift")
    else:
        a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(text)
    print(json.dumps({"status":p["status"],"checks":sum(p["checks"].values()),"total":len(p["checks"]),"lower_bound":p["lower_bounds"]["from_16_distinct_C2_orbits_plus_four_other_types"]}))
    return 0 if p["status"]=="PASS" else 1
if __name__=="__main__": raise SystemExit(main())
