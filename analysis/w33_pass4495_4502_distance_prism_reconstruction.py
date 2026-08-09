#!/usr/bin/env python3
"""Passes 4495, 4500--4502: distance, intrinsic W33 reconstruction, and prism duality.

Rebuilds W(3,3) from F_3^4 and proves:
  4495  The binary apartment code C=[1620,39] has d(C)=162 and exactly 40
        minimum words. A Walsh-polynomial branch-and-bound is exhaustive after
        fixing the global-reversal kernel.
  4500  Those 40 minimum words intrinsically reconstruct the dual W33 graph by
        Hamming distance 270 vs 312. Since the 1620 apartment columns are
        distinct, Aut(C) injects into Aut(W33); the natural PGSp(4,3) action
        supplies order 51840, hence Aut(C)=PGSp(4,3) using the established
        repository theorem |Aut(W33)|=51840.
  4501  The 2160 weight-3 words of C^perp are exactly triples of apartments
        forming the three rectangular faces of a triangular prism in the dual
        W33 line graph. Their span has rank 1215, so they do NOT generate C^perp.
  4502  Projecting each prism's six line vertices through A_* gives a protected
        240-orbit: every image has weight 20, every image has exactly nine prism
        preimages, the PSp stabilizer has order 108 and suborbits
        1,1,2,2,18,18,18,18,27,27,54,54. No identification with another
        240-object is inferred from the count alone.
"""
from __future__ import annotations
import itertools, json
from collections import Counter, defaultdict, deque
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"PART_W33_PASS4495_4502_DISTANCE_PRISM_RECONSTRUCTION.json"

def norm3(v):
    v=tuple(int(x)%3 for x in v)
    for x in v:
        if x:
            inv=1 if x==1 else 2
            return tuple((inv*y)%3 for y in v)
    raise ValueError("zero vector")

def geometry():
    pts=[]
    for lead in range(4):
        for tail in itertools.product(range(3),repeat=3-lead):
            pts.append((0,)*lead+(1,)+tail)
    pidx={p:i for i,p in enumerate(pts)}
    def symp(x,y):
        return (x[0]*y[1]-x[1]*y[0]+x[2]*y[3]-x[3]*y[2])%3
    lines=set()
    for i,x in enumerate(pts):
        for y in pts[i+1:]:
            if symp(x,y): continue
            span=set()
            for a,b in itertools.product(range(3),repeat=2):
                if a or b:
                    span.add(norm3(tuple((a*u+b*v)%3 for u,v in zip(x,y))))
            lines.add(frozenset(pidx[z] for z in span))
    lines=sorted(lines,key=lambda L:sorted(L))
    Astar=np.zeros((40,40),dtype=np.uint8)
    for i,j in itertools.combinations(range(40),2):
        if lines[i]&lines[j]:
            Astar[i,j]=Astar[j,i]=1
    nb=[set(np.flatnonzero(Astar[i])) for i in range(40)]
    apartments=set()
    for u,w in itertools.combinations(range(40),2):
        if Astar[u,w]: continue
        common=sorted(nb[u]&nb[w])
        for a,b in itertools.combinations(common,2):
            if not Astar[a,b]:
                apartments.add(tuple(sorted((u,w,a,b))))
    apartments=sorted(apartments)
    masks=[sum(1<<i for i in ap) for ap in apartments]
    H=np.zeros((40,1620),dtype=np.uint8)
    for j,ap in enumerate(apartments): H[list(ap),j]=1
    return pts,pidx,lines,Astar,apartments,masks,H

def restrict_poly(poly,bit,val):
    out=defaultdict(int);bm=1<<bit
    for m,c in poly.items():
        out[m^bm if m&bm else m]+=c*(val if m&bm else 1)
    return {m:c for m,c in out.items() if c}

def ub(poly):
    return poly.get(0,0)+sum(abs(c) for m,c in poly.items() if m)

def walsh_ge_counts(apartments,threshold):
    # sigma_0=+1 fixes the only global-reversal kernel.
    poly=defaultdict(int)
    for ap in apartments:
        m=0
        for l in ap:
            if l: m|=1<<(l-1)
        poly[m]+=1
    nodes=prunes=0; counts=Counter()
    def dfs(p,b):
        nonlocal nodes,prunes
        nodes+=1
        if ub(p)<threshold:
            prunes+=1; return
        if b==39:
            v=p.get(0,0)
            if v>=threshold: counts[v]+=1
            return
        has=any((m>>b)&1 for m in p)
        if has:
            dfs(restrict_poly(p,b,+1),b+1)
            dfs(restrict_poly(p,b,-1),b+1)
        else:
            # The objective can become independent of a still-free bit; both
            # coefficient assignments are distinct codewords after sigma_0 gauge.
            dfs(p,b+1); dfs(p,b+1)
    dfs(dict(poly),0)
    return counts,nodes,prunes

J3=np.array([[0,1,0,0],[2,0,0,0],[0,0,0,1],[0,0,2,0]],dtype=int)
def transvection3(v):
    v=np.array(v,dtype=int).reshape(4,1)%3
    return (np.eye(4,dtype=int)+v@((J3@v).T))%3
def compose_perm(p,q): return tuple(p[q[i]] for i in range(len(q)))
def perm_group(gens):
    ident=tuple(range(40));seen={ident};Q=deque([ident])
    while Q:
        a=Q.popleft()
        for g in gens:
            c=compose_perm(g,a)
            if c not in seen: seen.add(c);Q.append(c)
    return seen
def build_line_perm(M,pts,pidx,lines):
    lidx={tuple(sorted(L)):i for i,L in enumerate(lines)}
    pp=[]
    for p in pts:
        y=(np.array(M,dtype=int)@np.array(p,dtype=int))%3
        pp.append(pidx[norm3(tuple(y))])
    return tuple(lidx[tuple(sorted(pp[i] for i in L))] for L in lines)
def permute_mask(m,p):
    out=0
    for i in range(40):
        if (m>>i)&1: out|=1<<p[i]
    return out
def rank_int_vectors(vals):
    piv={}
    for x in vals:
        y=x
        while y:
            p=y.bit_length()-1
            if p in piv: y^=piv[p]
            else: piv[p]=y;break
    return len(piv)

def main():
    pts,pidx,lines,Astar,apartments,apmasks,H=geometry()
    assert len(apartments)==1620 and len(set(apmasks))==1620
    # Pass 4495 exact exhaustive frontier.
    gt,n_gt,p_gt=walsh_ge_counts(apartments,1297)
    assert gt==Counter({1620:1})
    ge,n_ge,p_ge=walsh_ge_counts(apartments,1296)
    assert ge==Counter({1296:40,1620:1})
    low,n_low,p_low=walsh_ge_counts(apartments,972)
    expected=Counter({1620:1,1296:40,1080:240,996:540,972:200})
    assert low==expected
    # w=(1620-W4)/2.
    weight_counts={str((1620-W)//2):int(c) for W,c in expected.items() if W!=1620}
    assert weight_counts=={"162":40,"270":240,"312":540,"324":200}

    # Minimum words are exactly the 40 rows of H.
    row_masks=[]
    for i in range(40):
        m=0
        for j,b in enumerate(H[i]):
            if b: m|=1<<j
        row_masks.append(m)
    assert len(set(row_masks))==40 and {m.bit_count() for m in row_masks}=={162}
    # Reconstruct dual W33 from pairwise Hamming distances.
    D=np.zeros((40,40),dtype=int)
    for i,j in itertools.combinations(range(40),2):
        d=(row_masks[i]^row_masks[j]).bit_count()
        D[i,j]=D[j,i]=d
        assert d==(270 if Astar[i,j] else 312)
    assert np.array_equal((D==270).astype(np.uint8),Astar)
    # Kernel of an Aut(C)->Aut(minword distance graph) action is trivial because
    # every apartment coordinate has a distinct 40-bit column pattern.
    col_patterns=[]
    for j in range(1620):
        m=sum(int(H[i,j])<<i for i in range(40))
        col_patterns.append(m)
    assert len(set(col_patterns))==1620

    # Build inner PSp and outer PGSp line actions; each permutes apartment supports.
    all_trans=[build_line_perm(transvection3(v),pts,pidx,lines) for v in pts]
    selected=[];inner={tuple(range(40))}
    for p in all_trans:
        trial=perm_group(selected+[p])
        if len(trial)>len(inner):
            selected.append(p);inner=trial
        if len(inner)==25920: break
    assert len(inner)==25920
    outer3=np.diag([1,2,1,2])%3
    assert np.array_equal((outer3.T@J3@outer3)%3,(2*J3)%3)
    outerp=build_line_perm(outer3,pts,pidx,lines)
    pgsp=perm_group(selected+[outerp])
    assert len(pgsp)==51840
    apset=set(apmasks)
    for p in selected+[outerp]:
        assert {permute_mask(m,p) for m in apmasks}==apset

    # Pass 4501: weight-3 dual relations.
    apidx={m:i for i,m in enumerate(apmasks)}
    triples=[]
    for i in range(1620):
        mi=apmasks[i]
        for j in range(i+1,1620):
            k=apidx.get(mi^apmasks[j])
            if k is not None and j<k:
                triples.append((i,j,k))
    assert len(triples)==2160
    tri_vecs=[]; unions=[]
    for a,b,c in triples:
        ma,mb,mc=apmasks[a],apmasks[b],apmasks[c]
        assert tuple(sorted(((ma&mb).bit_count(),(ma&mc).bit_count(),(mb&mc).bit_count())))==(2,2,2)
        u=ma|mb|mc;unions.append(u)
        vs=[i for i in range(40) if (u>>i)&1]
        assert len(vs)==6
        deg=sorted(sum(int(Astar[x,y]) for y in vs if y!=x) for x in vs)
        edges=sum(int(Astar[x,y]) for x,y in itertools.combinations(vs,2))
        triangles=sum(1 for xyz in itertools.combinations(vs,3)
                      if all(Astar[x,y] for x,y in itertools.combinations(xyz,2)))
        assert deg==[3]*6 and edges==9 and triangles==2  # triangular prism
        tri_vecs.append((1<<a)|(1<<b)|(1<<c))
    prism_span_rank=rank_int_vectors(tri_vecs)
    assert prism_span_rank==1215

    # Six-line prism subsets give a fixed primal weight and a protected 240-orbit.
    protected=Counter()
    def code_weight(coeff_mask):
        return sum(((m&coeff_mask).bit_count()&1) for m in apmasks)
    for u in unions:
        assert code_weight(u)==534
        b=np.array([(u>>i)&1 for i in range(40)],dtype=np.uint8)
        y=(Astar@b)%2
        assert int(y.sum())==20
        ym=sum(int(z)<<i for i,z in enumerate(y))
        protected[ym]+=1
    assert len(protected)==240 and set(protected.values())=={9}
    images=set(protected)
    base=next(iter(images))
    orbit={permute_mask(base,p) for p in inner}
    assert orbit==images
    stab=[p for p in inner if permute_mask(base,p)==base]
    assert len(stab)==108
    rem=set(images);suborbits=[]
    while rem:
        x=next(iter(rem))
        o={permute_mask(x,p) for p in stab}
        suborbits.append(len(o));rem-=o
    suborbits=sorted(suborbits)
    assert suborbits==[1,1,2,2,18,18,18,18,27,27,54,54]

    result={
      "passes":[4495,4500,4501,4502],
      "4495_primal_distance":{
        "code_parameters":"[1620,39,162]",
        "minimum_distance":162,
        "minimum_word_count":40,
        "walsh_gauge":"sigma_0=+1",
        "branch_proof_gt_1296":{"nodes":n_gt,"prunes":p_gt,"solutions":{"1620":1}},
        "branch_count_ge_1296":{"nodes":n_ge,"prunes":p_ge,"solutions":{"1620":1,"1296":40}},
        "exact_low_weight_counts":{"162":40,"270":240,"312":540,"324":200},
        "branch_count_ge_W4_972":{"nodes":n_low,"prunes":p_low},
        "proof_boundary":"Exhaustive Walsh branch-and-bound over all 2^39 codewords after the exact global-reversal gauge."
      },
      "4500_intrinsic_reconstruction":{
        "minimum_words":40,
        "distance_if_dual_lines_intersect":270,
        "distance_if_dual_lines_disjoint":312,
        "reconstructed_graph":"SRG(40,12,2,4), the dual W(3,3) line-collinearity graph",
        "apartment_columns_distinct":1620,
        "natural_PGSp_automorphism_subgroup_order":51840,
        "aut_code_conclusion":"Aut(C)=PGSp(4,3), order 51840, conditional only on the already-certified repository theorem Aut(W33)=PGSp(4,3)."
      },
      "4501_dual_prisms":{
        "dual_minimum_weight":3,
        "weight3_words":2160,
        "geometry":"each relation is the three rectangular apartment faces of a triangular prism on six dual-W33 lines",
        "weight3_span_rank":1215,
        "dual_dimension":1581,
        "generate_full_dual":False
      },
      "4502_prism_protected_orbit":{
        "prism_six_line_primal_weight":534,
        "protected_image_count":240,
        "protected_image_weight":20,
        "prisms_per_image":9,
        "PSp_orbit_transitive":True,
        "stabilizer_order":108,
        "stabilizer_suborbits":suborbits,
        "boundary":"The 240-orbit is reported by its actual action fingerprint. It is not identified with E8 roots, W33 edges, or any other 240-set from cardinality alone."
      }
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("PASS 4495/4500-4502")
    print("  d(C)=162, A_162=40")
    print("  low weights:",result["4495_primal_distance"]["exact_low_weight_counts"])
    print("  Aut(C)=PGSp(4,3) after intrinsic minword reconstruction")
    print("  Cperp weight-3 = 2160 triangular prisms; span rank 1215")
    print("  prism -> H10: 240 weight-20 images, 9-to-1, stab 108")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
