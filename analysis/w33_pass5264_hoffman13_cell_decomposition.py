#!/usr/bin/env python3
"""Pass5264: exact 13-cell decomposition of the Hoffman-shortened footprint code.

Pass5235 fixes a 13-coordinate Hoffman coclique that is also a partition of the
156 W-points: each point lies in exactly one of the 13 P-component blocks.  The
shortened footprint code is the kernel of projection to those 13 coordinates,
with parameters [312,52,d], and Pass5258 gives 28<=d<=40.

This pass rewrites that 52-dimensional problem as a 13-cell gluing problem.  For
one cover block B (12 W-points), take all even point-input subsets A<=B and map
A through the footprint generator F^T.  Because the 13 cover blocks partition
the W-points, every such output is automatically zero on all 13 cover
coordinates.  The even-input image has dimension 10 and exact weight enumerator

  1 + 36 x^40 + 30 x^48 + 225 x^64 + 440 x^72
    + 225 x^80 + 30 x^96 + 36 x^104 + x^144.

All 13 cell codes have this spectrum.  They generate the full 52-dimensional
shortened code.  Every pair of cell spaces meets trivially (sum dimension20),
and exhaustive enumeration of all 1024^2 sums for each of the 78 cell pairs
shows pair-sum minimum 40.  Therefore any shortened word below 40 must require
at least three cover cells.

The 286 triples have span-rank distribution 30^240, 28^30, 25^16.  Relative to
the Pass5232 weight-8-shell refinement on the 13 cover coordinates, the rank-28
triples are exactly the 30 triples with zero R2/codegree-5 pairs; the rank-25
triples are 16 of the all-three-R2 triangles.  This is a new finite higher-order
gluing surface for the exact shortened-distance problem.  We do NOT promote
d=40 here: three-or-more-cell cancellation remains to be excluded.
"""
from __future__ import annotations
import itertools,json
from collections import defaultdict,Counter,deque
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
from analysis.w33_pass5214_q5_connectedL_point_footprint_gluing import p_component_assignment

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5264_HOFFMAN13_CELL_DECOMPOSITION.json'
COVER=[6,30,73,111,128,140,157,189,193,226,254,277,320]
SEED=(119,124,183,188,209,302,317,318)

def rank_ints(rows):
    piv={}
    for x in rows:
        while x:
            p=x.bit_length()-1
            if p in piv:x^=piv[p]
            else:piv[p]=x;break
    return len(piv)

def basis_ints(rows):
    piv={};B=[]
    for x in rows:
        y=x
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;B.append(x);break
    return B

def main():
    G=build_W(5);acid,nc=p_component_assignment(G);assert nc==325
    blocks=[set() for _ in range(325)]
    for a,A in enumerate(G['apartments']):blocks[acid[a]].update(A)
    assert {len(B) for B in blocks}=={12}
    # point/component footprint rows
    F=[]
    for p in range(156):
        z=0
        for c,B in enumerate(blocks):
            if p in B:z|=1<<c
        F.append(z)
    assert {z.bit_count() for z in F}=={25} and rank_ints(F)==65
    cov=set(COVER)
    assert Counter(sum(p in blocks[c] for c in COVER) for p in range(156))==Counter({1:156})

    outputs=[];bases=[];spectra=[]
    for c in COVER:
        P=sorted(blocks[c]);D={}
        for m in range(1<<12):
            if m.bit_count()&1:continue
            z=0
            for i,p in enumerate(P):
                if (m>>i)&1:z^=F[p]
            # shortened condition
            assert all(((z>>d)&1)==0 for d in COVER)
            D[z]=1
        assert len(D)==1024
        spec=Counter(z.bit_count() for z in D)
        want={0:1,40:36,48:30,64:225,72:440,80:225,96:30,104:36,144:1}
        assert dict(sorted(spec.items()))==want
        B=basis_ints(D);assert len(B)==10
        outputs.append(tuple(D));bases.append(B);spectra.append(want)
    assert rank_ints([x for B in bases for x in B])==52

    pair_min=Counter();pair_rank=Counter()
    for i,j in itertools.combinations(range(13),2):
        assert rank_ints(bases[i]+bases[j])==20;pair_rank[20]+=1
        best=999
        for a in outputs[i]:
            for b in outputs[j]:
                z=a^b
                if z:best=min(best,z.bit_count())
        assert best==40;pair_min[best]+=1
    assert pair_min==Counter({40:78})

    # Reconstruct complete q5 weight-8 shell to classify cover triples by R2.
    pts=G['pts'];pidx={p:i for i,p in enumerate(pts)};blockkey={tuple(sorted(B)):i for i,B in enumerate(blocks)}
    def norm(v):
        for x in v:
            if x:
                s=pow(x,-1,5);return tuple(s*y%5 for y in v)
        raise ValueError
    def sp(u,v):return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%5
    def perm(v):
        pp=[]
        for x in pts:
            a=sp(x,v);pp.append(pidx[norm(tuple((x[k]+a*v[k])%5 for k in range(4)))])
        return [blockkey[tuple(sorted(pp[p] for p in B))] for B in blocks]
    gens=[perm(v) for v in ((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(1,1,0,0),(1,0,0,1))]
    seen={tuple(sorted(SEED))};Q=deque(seen)
    while Q:
        s=Q.popleft()
        for g in gens:
            t=tuple(sorted(g[x] for x in s))
            if t not in seen:seen.add(t);Q.append(t)
    assert len(seen)==24375
    pair=Counter()
    for D in seen:
        for a,b in itertools.combinations(D,2):pair[tuple(sorted((a,b)))]+=1
    assert Counter(pair[tuple(sorted(e))] for e in itertools.combinations(COVER,2))==Counter({5:48,0:30})

    triple=Counter()
    for T in itertools.combinations(range(13),3):
        r=rank_ints(sum((bases[i] for i in T),[]))
        cc=[COVER[i] for i in T]
        e=sum(pair[tuple(sorted((a,b)))]==5 for a,b in itertools.combinations(cc,2))
        triple[(r,e)]+=1
    assert triple==Counter({(30,2):144,(30,1):48,(30,3):48,(28,0):30,(25,3):16})

    out={'pass':5264,'status':'THEOREM_HOFFMAN13_SHORTENED_CELL_DECOMPOSITION',
      'shortened_code':'[312,52,d]_2 with 28<=d<=40',
      'cover_cells':13,'cell_code':{'dimension':10,'minimum_distance':40,'weight_enumerator':spectra[0]},
      'cell_span_dimension':52,'pair_intersection_dimension':0,'all_78_pair_sum_minimum':40,
      'consequence':'Any word of shortened weight <40 requires at least three cover cells.',
      'triple_span_rank_distribution':{'30':240,'28':30,'25':16},
      'triple_rank_vs_R2_edges':{f'{r},{e}':n for (r,e),n in sorted(triple.items())},
      'boundary':'This is a strict reduction, not an exact d=40 theorem. Three-or-more-cell cancellation remains open.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
