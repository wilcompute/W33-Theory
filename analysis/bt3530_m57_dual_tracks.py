#!/usr/bin/env python3
"""Two exact source-level M57 search tracks.

Track U is the unrestricted double-fibration model from Pass 3506.
Track I adds fixed-point-free involution constraints to every row-pair
permutation and separates non-involutory triangle holonomy lazily.

No n=56 SAT/UNSAT result is claimed.
"""
from __future__ import annotations
import argparse
import importlib.util
import json
import math
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"analysis/bt3506_m57_permutation_csp.py"

def load_base():
    spec=importlib.util.spec_from_file_location("bt3506_m57_base",BASE)
    if spec is None or spec.loader is None:
        raise RuntimeError(BASE)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def spectral_gate(n:int)->dict[str,Any]:
    d=n+1
    disc=4*d-3
    t=math.isqrt(disc)
    out={"fibre_size":n,"degree":d,"vertices":d*d+1,"discriminant":disc}
    if d==2:
        out.update(status="ADMISSIBLE",multiplicities=[2,2])
        return out
    if t*t!=disc:
        out["status"]="REJECT_NONSQUARE_DISCRIMINANT"
        return out
    num=d*(d-2)
    if num%t:
        out["status"]="REJECT_NONINTEGRAL_MULTIPLICITY"
        return out
    f2=d*d+num//t
    g2=d*d-num//t
    if f2%2 or g2%2:
        out["status"]="REJECT_NONINTEGRAL_MULTIPLICITY"
        return out
    out.update(status="ADMISSIBLE",restricted=[(-1+t)//2,(-1-t)//2],
               multiplicities=[f2//2,g2//2])
    return out

def involutive_statistics(n:int)->dict[str,int]:
    pairs=n*(n-1)//2
    return {
        "unordered_row_pairs":pairs,
        "element_involution_constraints":pairs*n,
        "factorization_pencils":n,
        "perfect_matchings_per_pencil":n-1,
        "edges_per_matching":n//2 if n%2==0 else 0,
        "edges_partitioned_per_pencil":n*(n-1)//2,
        "triangle_holonomies":n*(n-1)*(n-2)//6,
    }

def build_involutive_model(n:int=56):
    base=load_base()
    model,p=base.build_cp_sat_model(n)
    # For each unordered row pair, the forward permutation is an involution.
    # The base domain already excludes fixed points.
    for i in range(n):
        for j in range(i+1,n):
            forward=[p[i,j,a] for a in range(n)]
            for a in range(n):
                model.AddElement(p[i,j,a],forward,a)
    return model,p

def holonomy(candidate,i,j,k,a):
    b=candidate[i,j][a]
    c=candidate[j,k][b]
    return candidate[k,i][c]

def noninvolutory_holonomy_violations(candidate,n:int,limit:int|None=None):
    violations=[]
    for i in range(n):
        for j in range(i+1,n):
            for k in range(j+1,n):
                for a in range(n):
                    h=holonomy(candidate,i,j,k,a)
                    hh=holonomy(candidate,i,j,k,h)
                    if h==a or hh!=a:
                        violations.append((i,j,k,a,h,hh))
                        if limit is not None and len(violations)>=limit:
                            return violations
    return violations

def staged_frontier():
    stages=[1,2,4,6]+list(range(8,57,2))
    rows=[spectral_gate(n) for n in stages]
    assert [r["fibre_size"] for r in rows if r["status"]=="ADMISSIBLE"]==[1,2,6,56]
    return rows

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--n",type=int,default=56)
    parser.add_argument("--track",choices=["stats","unrestricted","involutive"],default="stats")
    args=parser.parse_args()
    base=load_base()
    result={
        "spectral_stages":staged_frontier(),
        "base_statistics":base.model_statistics(args.n),
        "involutive_statistics":involutive_statistics(args.n),
        "boundary":"Models are emitted; n=56 is not solved.",
    }
    if args.track=="involutive":
        model,_=build_involutive_model(args.n)
        result["model_proto_constraints"]=len(model.Proto().constraints)
    elif args.track=="unrestricted":
        model,_=base.build_cp_sat_model(args.n)
        result["model_proto_constraints"]=len(model.Proto().constraints)
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=="__main__":
    main()
