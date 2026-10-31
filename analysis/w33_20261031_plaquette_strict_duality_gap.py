#!/usr/bin/env python3
"""Exact dual-plaquette thermal gap for W(3,3), with an independent geometry build.

Unlike a self-duality assertion, the polynomial identity is certified by exhaustive
GF(2) kernel enumeration.  No continuum or critical-point claim is made.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "data" / "w33_20261031_plaquette_strict_duality_gap.json"

def canonical(v):
    v = tuple(x % 3 for x in v)
    nz = next(x for x in v if x)
    return tuple((x * (1 if nz == 1 else 2)) % 3 for x in v)

def symp(a, b):
    return (a[0] * b[2] + a[1] * b[3] - a[2] * b[0] - a[3] * b[1]) % 3

def geometry():
    points = sorted({canonical(v) for v in itertools.product(range(3), repeat=4) if any(v)})
    idx = {p: i for i, p in enumerate(points)}
    lines = set()
    for i, a in enumerate(points):
        for b in points[i+1:]:
            if symp(a, b) != 0:
                continue
            line = frozenset(idx[canonical(tuple(a[k] + t*b[k] for k in range(4)))]
                             for t in range(3))
            line |= {idx[b]}
            if len(line) != 4:
                raise AssertionError("bad isotropic line")
            lines.add(tuple(sorted(line)))
    return points, sorted(lines)

def kernel_gf2(rows, n):
    rr=list(rows)
    pivots=[]
    for c in range(n):
        k=len(pivots)
        pos=next((i for i in range(k,len(rr)) if (rr[i]>>c)&1),None)
        if pos is None:
            continue
        rr[k],rr[pos]=rr[pos],rr[k]
        for i in range(len(rr)):
            if i!=k and (rr[i]>>c)&1:
                rr[i]^=rr[k]
        pivots.append(c)
    free=[c for c in range(n) if c not in pivots]
    basis=[]
    for f in free:
        x=1<<f
        for i in reversed(range(len(pivots))):
            if (rr[i]&x).bit_count()%2:
                x ^= 1<<pivots[i]
        basis.append(x)
    return basis, len(pivots)

def enumerate_weights(basis):
    # Gray walk: one XOR per word, plus direct parity check via caller.
    v=0
    last=0
    hist=Counter({0:1})
    for i in range(1,1<<len(basis)):
        gray=i^(i>>1)
        step=gray^last
        j=step.bit_length()-1
        v^=basis[j]
        hist[v.bit_count()]+=1
        last=gray
    return hist

def poly_mul(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        if not x: continue
        for j,y in enumerate(b):
            if y: c[i+j]+=x*y
    return c

def factor_coeffs():
    t8=[0]*8+[9]
    factor=[1,0,-1]
    p=[5,0,16,0,38,0,16,0,5]
    for _ in range(8):t8=poly_mul(t8,factor)
    return poly_mul(t8,p)

def main():
    ps,lines=geometry()
    assert len(ps)==len(lines)==40
    assert all(len(line)==4 for line in lines)
    # N: point-by-line. Kernel N = line even sets (route).
    N=[sum(1<<j for j,line in enumerate(lines) if i in line) for i in range(40)]
    NT=[sum(1<<i for i in line) for line in lines]
    assert all(row.bit_count()==4 for row in N+NT)
    route_basis,rank=kernel_gf2(N,40)
    address_basis,rank_T=kernel_gf2(NT,40)
    route=enumerate_weights(route_basis)
    address=enumerate_weights(address_basis)
    difference=[address.get(k,0)-route.get(k,0) for k in range(41)]
    expected=factor_coeffs()
    expected+= [0]*(41-len(expected))
    checks={
       "40_points_lines":len(ps)==len(lines)==40,
       "point_line_regular_4":all(r.bit_count()==4 for r in N+NT),
       "rank_25_both":rank==rank_T==25,
       "dimension_15_both":len(route_basis)==len(address_basis)==15,
       "full_enumeration_32768_both":sum(route.values())==sum(address.values())==32768,
       "route_40_15_10_and_216":min(k for k in route if k>0)==10 and route[10]==216,
       "address_40_15_8_and_45":min(k for k in address if k>0)==8 and address[8]==45,
       "strict_difference_factorization":difference==expected,
       "complement_symmetry":all(route[k]==route[40-k] and address[k]==address[40-k] for k in range(41))
    }
    # Derivatives at t=1 up to order seven vanish; eighth is nonzero.
    falling=lambda n,j: __import__("math").factorial(n)//__import__("math").factorial(n-j) if n>=j else 0
    deriv=[sum(difference[k]*falling(k,j) for k in range(41)) for j in range(9)]
    checks["order8_contact_at_t1"]=all(d==0 for d in deriv[:8]) and deriv[8]!=0
    assert all(checks.values()),checks
    payload={
     "schema":"w33.20261031.plaquette_strict_duality_gap.v1",
     "status":"PASS",
     "source_geometry":"W(3,3), reconstructed directly from projective F3^4 and alternating form",
     "incidence_orientation":"N=40 points x 40 lines; route=ker_F2(N) on lines, address=ker_F2(N^T) on points",
     "rank_F2":rank,"dimension_F2":len(route_basis),
     "route_weight_enumerator":dict(sorted(route.items())),
     "address_weight_enumerator":dict(sorted(address.items())),
     "weight_enumerator_gap_coefficients_low_to_high":difference,
     "strict_factorization":"W_address(t)-W_route(t)=9*t^8*(1-t^2)^8*(5*t^8+16*t^6+38*t^4+16*t^2+5)",
     "eighth_derivative_at_t1":deriv[8],
     "conclusion":"W_address(t)>W_route(t) for 0<t<1; same first 8 Taylor coefficients at t=1.",
     "physical_scope":"finite Ising plaquette partition functions share 2^40*cosh(K)^40 normalization, t=tanh(K); no thermodynamic critical point established.",
     "prior_art":"Pass 159/167 address code; Pass 173 route code; Pass 12500 nonseldual plaquette check.",
     "checks":checks
    }
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,default=DEFAULT)
    args=parser.parse_args()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(json.dumps({"status":"PASS","checks":len(checks),"rank":rank,
           "min_route":10,"min_address":8,"derivative8":deriv[8],
           "output":str(args.output)},sort_keys=True))

if __name__=="__main__":
    main()
