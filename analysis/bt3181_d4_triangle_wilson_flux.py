#!/usr/bin/env python3
"""Pass 3181: D4 triangle Wilson-flux census."""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/PART_BT3181_D4_TRIANGLE_WILSON_FLUX_results.json'
E=[(i,j) for i in range(4) for j in range(2)];ONE=(0,0);N=[x for x in E if x!=ONE]
def mul(a,b):
    i,j=a;k,l=b;return ((i+(k if j==0 else -k))%4,(j+l)%2)
def inv(a):return next(b for b in E if mul(a,b)==ONE and mul(b,a)==ONE)
def conj(g,a):return mul(mul(g,a),inv(g))
def comm(a,b):return mul(mul(mul(a,b),inv(a)),inv(b))
def k(a,b):return int(comm(a,b)!=ONE)
def flux(t):a,b,c=t;return k(a,b)^k(b,c)^k(c,a)
def main():
    triples=list(itertools.product(N,repeat=3));c=Counter(flux(t) for t in triples);seen=set();orbits=Counter()
    for t in triples:
        if t in seen:continue
        o={tuple(conj(g,x) for x in t) for g in E};seen|=o;orbits[(len(o),flux(t))]+=1
    assert c=={0:223,1:120} and sum(orbits.values())==106
    out={'schema':'w33.pass3181.d4_triangle_wilson_flux.v1','definition':'Phi(a,b,c)=kappa(a,b) xor kappa(b,c) xor kappa(c,a)','ordered_nonidentity_triples':343,'flux_zero':223,'flux_one':120,'simultaneous_conjugation_orbits':106,'orbit_census':[{'orbit_size':s,'flux':f,'orbits':n} for (s,f),n in sorted(orbits.items())],'across_23_measured_triangles':{'assignments':7889,'flat_flux':5129,'curved_flux':2760},'theorem':'Phi is invariant under simultaneous conjugation because each D4 commutator lies in the central derived subgroup {1,r^2}.','boundary':'Exact finite non-Abelian holonomy syndrome; not spacetime curvature or measured optical phase.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
