#!/usr/bin/env python3
"""Pass5285: exact four-type refinement of the q=5 Hoffman-13 shortening frontier.

Pass5264 decomposes the [312,52] Hoffman-shortened footprint code into 13 cell
codes and proves every word below 40 must involve at least three cells. This pass
uses the complete q=5 weight-8 dual shell to refine the 312 non-cover coordinates
relative to the fixed Hoffman coclique.

For every non-cover P block x, count how many of the 13 cover blocks are in the
three Pass5232 relations R1/R2/R3 to x. Exactly four signatures occur:
  (6,5,2)^144, (6,6,1)^96, (6,3,4)^48, (6,1,6)^24.
Thus all 312 coordinates see exactly six R1 cover neighbors, while the R2/R3
balance splits into four exact types.

The 24,375 weight-8 dual checks meet the cover in 0,1,2 coordinates with counts
16815,7320,240. Restricting these three check families to the 312 complement
coordinates gives type-dependent replication and maximum pair codegrees. None of
these restricted moment systems by itself reaches the candidate shortened bound
40; the exact shortened minimum remains one of 28,32,36,40.

This is an exact finite refinement and a search-surface theorem, not a d=40 claim.
"""
from __future__ import annotations
import itertools, json
from collections import Counter, deque, defaultdict
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
from analysis.w33_pass5214_q5_connectedL_point_footprint_gluing import p_component_assignment

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5285_HOFFMAN13_FOURTYPE_REFINEMENT.json'
COVER=(6,30,73,111,128,140,157,189,193,226,254,277,320)
SEED=(119,124,183,188,209,302,317,318)

def main():
    G=build_W(5); acid,nc=p_component_assignment(G); assert nc==325
    blocks=[set() for _ in range(325)]
    for a,A in enumerate(G['apartments']): blocks[acid[a]].update(A)
    assert {len(B) for B in blocks}=={12}
    cov=set(COVER); comp=[x for x in range(325) if x not in cov]; assert len(comp)==312

    pts=G['pts']; pidx={p:i for i,p in enumerate(pts)}
    blockkey={tuple(sorted(B)):i for i,B in enumerate(blocks)}
    def norm(v):
        for x in v:
            if x:
                s=pow(x,-1,5); return tuple(s*y%5 for y in v)
        raise ValueError
    def sp(u,v): return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%5
    def perm(v):
        pp=[]
        for x in pts:
            a=sp(x,v); pp.append(pidx[norm(tuple((x[k]+a*v[k])%5 for k in range(4)))])
        return [blockkey[tuple(sorted(pp[p] for p in B))] for B in blocks]
    gens=[perm(v) for v in ((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(1,1,0,0),(1,0,0,1))]
    shell={tuple(sorted(SEED))}; Q=deque(shell)
    while Q:
        s=Q.popleft()
        for g in gens:
            t=tuple(sorted(g[x] for x in s))
            if t not in shell: shell.add(t); Q.append(t)
    assert len(shell)==24375

    pair=Counter()
    for D in shell:
        for a,b in itertools.combinations(D,2): pair[tuple(sorted((a,b)))]+=1
    assert set(pair.values())<={5,25}

    sig={}
    dist=Counter()
    for x in comp:
        c=Counter(pair[tuple(sorted((x,y)))] for y in COVER)
        s=(c[25],c[5],c[0])
        assert sum(s)==13
        sig[x]=s; dist[s]+=1
    want={(6,5,2):144,(6,6,1):96,(6,3,4):48,(6,1,6):24}
    assert dist==Counter(want)

    cover_intersections=Counter(len(set(D)&cov) for D in shell)
    assert cover_intersections==Counter({0:16815,1:7320,2:240})

    family_stats={}
    expected_rep={
      0:{(6,5,2):429,(6,6,1):426,(6,3,4):441,(6,1,6):445},
      1:{(6,5,2):167,(6,6,1):168,(6,3,4):153,(6,1,6):155},
      2:{(6,5,2):4,(6,6,1):6,(6,3,4):6,(6,1,6):0},
    }
    expected_lam={0:23,1:17,2:4}
    for h in (0,1,2):
        fam=[tuple(x for x in D if x not in cov) for D in shell if len(set(D)&cov)==h]
        rep=Counter()
        pc=Counter()
        for D in fam:
            for x in D: rep[x]+=1
            for a,b in itertools.combinations(D,2): pc[tuple(sorted((a,b)))]+=1
        bytype={}
        for s in want:
            vals={rep[x] for x in comp if sig[x]==s}
            assert len(vals)==1
            bytype[s]=next(iter(vals))
        assert bytype==expected_rep[h]
        maxpair=max(pc.values()) if pc else 0
        assert maxpair==expected_lam[h]
        family_stats[str(h)]={
          'checks':len(fam),
          'restricted_check_weight':8-h,
          'replication_by_signature':{str(k):v for k,v in bytype.items()},
          'maximum_pair_codegree':maxpair,
        }

    out={
      'pass':5285,
      'status':'THEOREM_HOFFMAN13_COMPLEMENT_FOURTYPE_REFINEMENT_WITH_DISTANCE_WALL',
      'shortened_code':'[312,52,d]_2, d in {28,32,36,40}',
      'cover_size':13,
      'complement_size':312,
      'coordinate_relation_signatures':{str(k):v for k,v in want.items()},
      'signature_meaning':'(number of R1, R2, R3 relations from a non-cover coordinate to the 13 cover coordinates)',
      'weight8_shell_cover_intersection_histogram':{str(k):v for k,v in sorted(cover_intersections.items())},
      'restricted_dual_family_stats':family_stats,
      'conclusion':'The Hoffman complement has four exact cover-relative coordinate types. The three natural restricted weight-8-shell moment systems do not by themselves certify d=40, so a higher-order/type-coupled argument is required.',
      'boundary':'No exact shortened minimum is promoted. A bounded MILP/heuristic noncompletion is not a lower-bound certificate; d remains one of 28,32,36,40.'
    }
    OUT.write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
if __name__=='__main__': main()
