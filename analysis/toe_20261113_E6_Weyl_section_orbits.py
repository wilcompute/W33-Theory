#!/usr/bin/env python3
"""Enumerate the full Schlaefli graph automorphism group action on
coordinate-maximal E6(6) sections (72 sixers and 216 fivers).

A completed 51840-element automorphism enumeration certifies the
W(E6) Levi stabilizers 720 (=W(A5)=S6) and 240 (=W(A4) x W(A1)).
Always fail closed on a wall-time cap; partial enumeration isn't proof.
"""
import json,time,sys
from collections import Counter
from itertools import combinations
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_fermat_cubic_h27_sixers as F
OUT=ROOT/"data/toe_20261113_E6_Weyl_M_IIB_section_stabilizers.json"

def main(cap_s=115):
    G,_,_=F.original()
    allcliques=sorted(tuple(sorted(x)) for x in nx.find_cliques(nx.complement(G)))
    six=set(x for x in allcliques if len(x)==6)
    five=set(x for x in allcliques if len(x)==5)
    assert len(five)==216 and len(six)==72
    included={tuple(sorted(set(x)-{v})) for x in six for v in x}
    assert len(included)==432 and not set(included)&five
    sf=min(five);ss=min(six);se=min(included)
    maps=nx.algorithms.isomorphism.GraphMatcher(G,G).isomorphisms_iter()
    start=time.perf_counter()
    orbitf=set();orbits=set();orbite=set()
    stabilf=0;stabils=0;stabile=0;n=0;complete=True
    for m in maps:
        n+=1
        f=tuple(sorted(m[j] for j in sf));s=tuple(sorted(m[j] for j in ss))
        e=tuple(sorted(m[j] for j in se))
        assert f in five and s in six and e in included
        orbitf.add(f);orbits.add(s);orbite.add(e)
        stabilf+=f==sf;stabils+=s==ss;stabile+=e==se
        if n%1000==0:
            print("AUT",n,"ORBITS",len(orbitf),len(orbits),len(orbite),"ELAPSED",round(time.perf_counter()-start,1),flush=True)
            if time.perf_counter()-start>cap_s:
                complete=False
                break
    elapsed=round(time.perf_counter()-start,2)
    if complete:
        assert n==51840,n
        assert (len(orbitf),len(orbits),len(orbite))==(216,72,432)
        assert (stabilf,stabils,stabile)==(240,720,120)
    out={
      "schema":"toe.E6.Weyl.two.physical.section.orbits.v1",
      "status":"CERTIFIED_51840_FULL_W_E6_ACTION" if complete else "BOUNDED_AUTOMORPHISM_ENUMERATION_NO_FULL_CERTIFICATE",
      "complete":complete,
      "automorphisms_checked":n,
      "wall_s":elapsed,
      "wall_budget_s":cap_s,
      "maximal_fiver_orbit_seen":len(orbitf),
      "maximal_sixer_orbit_seen":len(orbits),
      "extendable_fiver_orbit_seen":len(orbite),
      "maximal_fiver_stabilizer_count_seen":stabilf,
      "maximal_sixer_stabilizer_count_seen":stabils,
      "extendable_fiver_stabilizer_count_seen":stabile,
      "expected_when_complete":{"W_E6_order":51840,"5_maximal_orbit":216,"5_maximal_stabilizer":240,
           "6_maximal_orbit":72,"6_maximal_stabilizer":720,
           "5_extendable_orbit":432,"5_extendable_stabilizer":120},
      "section_interpretation":"The order 240 and 720 are precisely the Weyl group orders of A4xA1 and A5 respectively, matching the Levi types of type IIB five-coordinate and M six-coordinate ExFT sections. Group stabilizer order alone does not prove the full connected parabolic identification.",
      "validity":"Only completed full enumeration permits the numeric group-order and stabilizer conclusion; incomplete is data for follow-up only."}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:out[k] for k in ("status","automorphisms_checked","maximal_fiver_orbit_seen","maximal_sixer_orbit_seen","extendable_fiver_orbit_seen","wall_s")},indent=2),flush=True)
    return out
if __name__=="__main__":main()
