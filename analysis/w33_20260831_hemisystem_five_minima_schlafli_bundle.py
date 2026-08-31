#!/usr/bin/env python3
"""Test an exact 216 = 27 x 8 bridge inside the W33 trade lattice.

The rank-15 integral trade lattice ker_Z(N) has 45 projective minimum-vector
lines of norm 8.  Their orthogonality graph is GQ(4,2), hence has 27 maximal
5-cliques (its lines).  Five pairwise orthogonal minima have every signed sum
at norm 40, exactly the norm of a centered W33 2-ovoid/hemisystem vector.

This audit asks a deliberately stronger question than count matching:
  * enumerate all 27 orthogonal 5-frames of minimum lines;
  * enumerate every signed sum in each frame;
  * retain only coordinatewise {+/-1} sums;
  * compare projectively with the independently generated 216 hemisystem lines;
  * test uniqueness of the base 5-frame and the 8-point fibre;
  * test whether each fibre is an affine F_2^3 subset of the 4-dimensional
    projective sign cube;
  * reconstruct the 27-base intersection graph and certify SRG(27,10,1,5),
    i.e. the GQ(2,4) / Schlaefli-complement carrier;
  * compute the PSp(4,3) stabilizer of one base frame and its action on the
    eight hemisystem lines above that frame.

The script is a certificate either way: if the proposed bundle fails, it emits
an exact NO_GO rather than forcing the 27 x 8 arithmetic.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict, deque
from pathlib import Path

import w33_20260828_trade_lattice_minimum_gq45 as trade
import w33_20260829_216_clifford_torsor_nogo as base
import w33_20260831_hemisystem_eigenframe_576 as hemi

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260831_HEMISYSTEM_FIVE_MINIMA_SCHLAFLI_BUNDLE.json'


def dot(u,v): return sum(a*b for a,b in zip(u,v))

def neg(v): return tuple(-x for x in v)

def canon_vec(v):
    i=next(k for k,x in enumerate(v) if x)
    return tuple(v) if v[i]>0 else neg(v)

def transform_vec(p,v):
    w=[0]*len(v)
    for i,z in enumerate(v): w[p[i]]=z
    return tuple(w)

def srg(G):
    deg={len(x) for x in G}; la=set(); mu=set()
    for i,j in itertools.combinations(range(len(G)),2):
        c=len(G[i]&G[j]); (la if j in G[i] else mu).add(c)
    return [len(G),sorted(deg),sorted(la),sorted(mu)]

def gf2_rank(vals, nbits=4):
    xs=list(vals); r=0
    for b in range(nbits-1,-1,-1):
        q=next((i for i in range(r,len(xs)) if (xs[i]>>b)&1),None)
        if q is None: continue
        xs[r],xs[q]=xs[q],xs[r]
        for i in range(len(xs)):
            if i!=r and ((xs[i]>>b)&1): xs[i]^=xs[r]
        r+=1
    return r

def compose(p,q): return tuple(p[q[i]] for i in range(len(q)))


def main():
    pts,idx,lines=trade.geometry(); assert len(pts)==len(lines)==40
    N=[[0]*40 for _ in range(40)]
    for l,L in enumerate(lines):
        for p in L: N[l][p]=1
    cols=[tuple(N[l][p] for l in range(40)) for p in range(40)]

    # Reconstruct the 45 projective minimum lines independently from the
    # four-column signature collisions used in the lattice-minimum theorem.
    d=defaultdict(list)
    for S in itertools.combinations(range(40),4):
        sig=tuple(sum(cols[p][l] for p in S) for l in range(40)); d[sig].append(S)
    collisions=[v for v in d.values() if len(v)>1]
    assert Counter(map(len,collisions))==Counter({2:45})
    pairs=sorted(tuple(sorted((tuple(a),tuple(b)))) for a,b in collisions)
    mins=[]
    for a,b in pairs:
        v=tuple(1 if i in b else -1 if i in a else 0 for i in range(40))
        assert dot(v,v)==8 and all(sum(N[l][p]*v[p] for p in range(40))==0 for l in range(40))
        mins.append(v)

    Orth=[set() for _ in range(45)]
    for i,j in itertools.combinations(range(45),2):
        if dot(mins[i],mins[j])==0: Orth[i].add(j); Orth[j].add(i)
    assert srg(Orth)==[45,[12],[3],[3]]

    # All 5-cliques are the 27 GQ(4,2) lines.
    cliques=set()
    def rec(prefix,cands):
        if len(prefix)==5:
            cliques.add(tuple(prefix)); return
        need=5-len(prefix)
        if len(cands)<need: return
        for i in sorted(cands):
            nxt={j for j in cands if j>i and j in Orth[i]}
            rec(prefix+[i],nxt)
    rec([],set(range(45)))
    frames=sorted(cliques); assert len(frames)==27

    # The line-intersection graph is the dual GQ(2,4) collinearity graph.
    BG=[set() for _ in range(27)]
    for i,j in itertools.combinations(range(27),2):
        if set(frames[i])&set(frames[j]): BG[i].add(j); BG[j].add(i)
    base_srg=srg(BG); assert base_srg==[27,[10],[1],[5]]

    # Enumerate all signed orthogonal sums.  Gauge bit 0 to zero to quotient
    # by global sign and test whether the valid sign patterns form affine F2^3.
    constructed=set(); owners=defaultdict(list); fibre_records=[]
    for fi,C in enumerate(frames):
        valid_masks=[]; local_lines=set()
        for mask in range(32):
            coeff=[-1 if (mask>>j)&1 else 1 for j in range(5)]
            v=tuple(sum(coeff[j]*mins[C[j]][k] for j in range(5)) for k in range(40))
            assert dot(v,v)==40
            if all(abs(x)==1 for x in v):
                valid_masks.append(mask)
                z=canon_vec(v); local_lines.add(z); constructed.add(z); owners[z].append(fi)
        gauge=sorted((m>>1) for m in valid_masks if (m&1)==0)
        affine=False; arank=None; functional=[]
        if gauge:
            x0=gauge[0]; translated={x^x0 for x in gauge}; arank=gf2_rank(translated)
            affine=(len(translated)==2**arank and 0 in translated and
                    all((a^b) in translated for a in translated for b in translated))
            if affine and arank==3:
                # Unique nonzero linear functional on F2^4 constant on this affine hyperplane.
                for c in range(1,16):
                    vals={((c & x).bit_count()&1) for x in gauge}
                    if len(vals)==1: functional.append([c,next(iter(vals))])
        fibre_records.append({'frame':list(C),'orientedValidMasks':len(valid_masks),
                              'projectiveValidLines':len(local_lines),'gaugePatterns':gauge,
                              'affine':affine,'affineRank':arank,'affineFunctionals':functional})

    # Independently generate all 432 2-ovoids and their 216 projective sign lines.
    gens=[]
    for v in pts:
        for a in (1,2):
            perm=[]
            for x in pts:
                c=a*base.form(x,v)%3
                y=base.norm(tuple((x[k]+c*v[k])%3 for k in range(4)))
                perm.append(idx[y])
            gens.append(tuple(perm))
    chosen=(18,62,77,10); gg=[gens[i] for i in chosen]
    ident=tuple(range(40)); G={ident}; q=deque([ident])
    while q:
        p=q.popleft()
        for g in gg:
            h=compose(g,p)
            if h not in G: G.add(h); q.append(h)
    assert len(G)==25920
    orbit={frozenset(g[x] for x in hemi.T0) for g in G}; assert len(orbit)==432
    hemi_lines={canon_vec(tuple(1 if i in T else -1 for i in range(40))) for T in orbit}
    assert len(hemi_lines)==216

    equality=(constructed==hemi_lines)
    owner_hist=Counter(len(v) for v in owners.values())
    fibre_hist=Counter(r['projectiveValidLines'] for r in fibre_records)
    affine_hist=Counter((r['affine'],r['affineRank']) for r in fibre_records)

    # Group action on the 45 minimum lines, then stabilizer of one 5-frame.
    min_index={canon_vec(v):i for i,v in enumerate(mins)}
    def act_min(p,i): return min_index[canon_vec(transform_vec(p,mins[i]))]
    C0=frozenset(frames[0])
    H960=[]
    for g in G:
        if frozenset(act_min(g,i) for i in C0)==C0: H960.append(g)
    assert len(H960)==960

    fibre0={z for z,oo in owners.items() if 0 in oo}
    def act_line(p,z): return canon_vec(transform_vec(p,z))
    if fibre0:
        z0=next(iter(fibre0))
        fib_orbit={act_line(g,z0) for g in H960}
        Hpoint=[g for g in H960 if act_line(g,z0)==z0]
        kernel=[g for g in H960 if all(act_line(g,z)==z for z in fibre0)]
    else:
        fib_orbit=set(); Hpoint=[]; kernel=[]

    exact_bundle=(equality and owner_hist==Counter({1:216}) and fibre_hist==Counter({8:27})
                  and affine_hist==Counter({(True,3):27}) and fib_orbit==fibre0 and len(Hpoint)==120)
    relation='EXACT_BUNDLE' if exact_bundle else 'NO_GO_OR_PARTIAL'

    out={
      'schema':'w33.20260831.hemisystem-five-minima-schlafli-bundle.v1','status':'PASS',
      'relation':relation,
      'tradeLattice':{'rank':15,'minimumLines':45,'minimumNormSquared':8,
                      'orthogonalityGraph':[45,12,3,3]},
      'base27':{'orthogonalFiveFrames':len(frames),'intersectionGraph':base_srg,
                'interpretation':'dual GQ(2,4) collinearity / Schlaefli-complement carrier'},
      'signedSums':{'constructedProjectiveLines':len(constructed),'hemisystemProjectiveLines':len(hemi_lines),
                    'exactSetEquality':equality,'ownershipMultiplicityHistogram':dict(sorted(owner_hist.items())),
                    'validLinesPerFrameHistogram':dict(sorted(fibre_hist.items())),
                    'affineFibreHistogram':{str(k):v for k,v in sorted(affine_hist.items(),key=str)}},
      'groupBundle':{'PSpOrder':len(G),'baseFrameStabilizerOrder':len(H960),
                     'fibre0Size':len(fibre0),'fibreOrbitSize':len(fib_orbit),
                     'fibrePointStabilizerOrder':len(Hpoint),'fibreActionKernelOrder':len(kernel)},
      'fibreRecords':fibre_records,
      'theorem':('Every one of the 216 hemisystem eigenlines is a signed sum of five mutually orthogonal '
                 'norm-8 trade-lattice minima, uniquely over one of the 27 GQ(4,2) lines; each base line '
                 'carries an affine F2^3 fibre of eight hemisystem lines.  Thus the hemisystem frame is an '
                 'exact 8-sheeted bundle over the 27-point dual GQ(2,4)/Schlaefli-complement carrier.'
                 if exact_bundle else
                 'The proposed 27-by-8 five-minimum construction is not exact; the certificate records the precise obstruction.'),
      'boundary':'The Schlaefli label refers to the exact 27-vertex SRG(27,10,1,5) complement carrier; no physical interpretation is asserted.'
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','relation':relation,'constructed':len(constructed),'equality':equality,
                      'frames':len(frames),'fibreHist':dict(fibre_hist),'ownerHist':dict(owner_hist),
                      'affineHist':{str(k):v for k,v in affine_hist.items()},'H960':len(H960),
                      'fibreOrbit':len(fib_orbit),'Hpoint':len(Hpoint),'kernel':len(kernel)},sort_keys=True))

if __name__=='__main__': main()
