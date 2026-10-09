"""Exhaust all 9880 unordered W33 point triples under PSp(4,3).
For each orbit: stabilizer, 81-cycle H-invariant dimensions and its
possible rank-three quotient. Detect symmetry-invariant triple energies
cannot choose a unique triple without degenerate symmetry breaking.
"""
from itertools import combinations
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import bt1688_exact_h1_character_irreducibility as B

def count_orbits(size,maps):
    unseen=set(range(size));counts=[]
    while unseen:
        x=min(unseen);orb={p[x] for p in maps}
        assert orb<=unseen
        unseen-=orb;counts.append(len(orb))
    return len(counts),sorted(counts)

def invariant_cycle_rank(group, lines):
    lineid={l:i for i,l in enumerate(lines)}
    edgeid={(p,i):4*i+j for i,l in enumerate(lines) for j,p in enumerate(l)}
    assert len(edgeid)==160
    edge=[(p,i) for i,l in enumerate(lines) for p in l]
    maps80=[];maps160=[]
    for g in group:
        lp=[lineid[tuple(sorted(g[p] for p in l))] for l in lines]
        maps80.append(list(g)+[40+x for x in lp])
        maps160.append([edgeid[(g[p],lp[i])] for p,i in edge])
    a,vo=count_orbits(80,maps80)
    b,eo=count_orbits(160,maps160)
    return b-a+1,dict(vertex_orbits=a,edge_orbits=b,vertex_sizes=vo,edge_sizes=eo)

def certificate():
    pts=B.make_points();lines=B.w33_lines(pts)
    G=B.projective_group(pts);assert len(G)==25920
    triples=set(combinations(range(40),3))
    results=[]
    while triples:
        r=min(triples)
        orbit={tuple(sorted(g[x] for x in r)) for g in G}
        assert orbit<=triples
        triples-=orbit
        stabilizer=[g for g in G if all(g[x]==x for x in r)]
        set_stabilizer=[g for g in G if set(g[x] for x in r)==set(r)]
        rank,stats=invariant_cycle_rank(stabilizer,lines)
        srank,sstats=invariant_cycle_rank(set_stabilizer,lines)
        ncomm=sum(B.symplectic_form(pts[x],pts[y])==0 for x,y in combinations(r,2))
        on_line=any(set(r)<=set(l) for l in lines)
        assert len(set_stabilizer)*len(orbit)==25920
        results.append(dict(representative=list(r),orbit_size=len(orbit),
            pointwise_stabilizer_order=len(stabilizer),
            setwise_stabilizer_order=len(set_stabilizer),
            commuting_pairs=ncomm,contained_in_line=on_line,
            pointwise_H1_invariant_rank=rank,setwise_H1_invariant_rank=srank,
            pointwise_orbit_stats=stats,setwise_orbit_stats=sstats))
        print('ORBIT',r,'size',len(orbit),'rank',rank,'setrank',srank,flush=True)
    assert sum(x['orbit_size'] for x in results)==9880
    energy_hist={str(E):sum(t['orbit_size'] for t in results
                 if 3-t['commuting_pairs']==E) for E in range(4)}
    assert energy_hist=={'0':160,'1':2160,'2':4320,'3':3240}
    return dict(status='PASS',G_order=25920,triples=9880,
        toy_selector='E(T)=3-(number of pairwise-commuting point pairs)',
        selector_energy_histogram=energy_hist,
        selector_minima=160,selector_first_energy_gap=1,
        total_orbits=len(results),orbit_types=sorted(results,key=lambda x:x['orbit_size']),
        theorem='Any energy invariant under full PSp(4,3), defined only on unordered triples, is constant on each orbit. It cannot have an isolated selected minimum: every minimum orbit has its stated degeneracy.',
        boundary='A spontaneous broken-symmetry order parameter may choose one triple; no energy functional, domain-wall tension or dynamical selection has been derived.')
if __name__=='__main__':
    x=certificate()
    (ROOT/'data/w33_20261009_all_triple_orbit_breaking.json').write_text(json.dumps(x,indent=2)+'\n')
    print('PASS',x['total_orbits'],'types')
