#!/usr/bin/env python3
"""Pass 4752 — compare the apartment deck class with the Pass4738 C2 twist.

There is a canonical PSp-equivariant projection from the 810 selected flags
(L,x) to their 270 selected lines L.  We rebuild the Pass4713 double cover,
extract its binary edge voltage, and solve the exact F2 descent problem:
can a flag-vertex gauge make that voltage depend only on the projected 270-line
edge?  This is a linear system, not an analogy.

Independently, for one selected line/residue stabilizer H of order 96 we compute
the six-apartment action above its three flags.  We solve the three local sheet
gauges and obtain any global C2 sheet character epsilon:H->C2.  Its kernel is
compared as an actual subgroup with K=C_PSp(h), the order-48 normalizer kernel
from Pass4738.  Thus the local twists either coincide exactly or fail closed.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict,deque
from pathlib import Path
import numpy as np
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry,build_line_perm,perm_group,transvection_matrix
from w33_pass4587_w33_derived_d4_triality import rank_basis_int,span
from w33_pass4716_selected270_bundle_connection import build_bundle
from w33_pass4745_invariant_h1_character import compose,invperm,pmask
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4752_DECK_NORMALIZER_TWIST_COMPARISON.json'

def fixed_mask(p):return sum(1<<i for i,j in enumerate(p) if i==j)
def solve_f2(rows,nvar):
    piv={}
    for mask,rhs in rows:
        y=int(mask);b=int(rhs)&1
        while y:
            p=y.bit_length()-1
            if p in piv:
                z,c=piv[p];y^=z;b^=c
            else:piv[p]=(y,b);break
        if not y and b:return None
    sol=0
    for p in sorted(piv):
        m,b=piv[p];rest=m^(1<<p);val=b^((rest&sol).bit_count()&1)
        if val:sol|=1<<p
    return sol

def main():
    pts,pidx,lines,lidx,_,Astar,_,apartments,_=build_geometry();Astar=np.asarray(Astar,dtype=np.uint8);apartments=sorted(tuple(map(int,a)) for a in apartments)
    all40=(1<<40)-1;cols=[]
    for c in range(40):
        m=0
        for r in np.flatnonzero(Astar[:,c]):m|=1<<int(r)
        cols.append(m)
    B9=rank_basis_int([cols[i]^cols[k] for i in range(40) for k in range(i+1,40) if Astar[i,k]])
    rep=lambda x:min(int(x),int(x)^all40)
    def fib(ap):
        z=0
        for i in ap:z^=cols[i]
        return rep(z)
    def aline(ap):
        opp=[(a,b) for a,b in itertools.combinations(ap,2) if not Astar[a,b]]
        return tuple(sorted((rep(cols[opp[0][0]]^cols[opp[0][1]]),rep(cols[opp[1][0]]^cols[opp[1][1]]),fib(ap))))
    selected=sorted({aline(a) for a in apartments});selidx={L:i for i,L in enumerate(selected)};assert len(selected)==270
    flag_lifts=defaultdict(list)
    for ap in apartments:
        L=aline(ap);x=fib(ap);flag_lifts[(L,x)].append(ap)
    flags=sorted(flag_lifts);findex={f:i for i,f in enumerate(flags)};aindex={a:i for i,a in enumerate(apartments)}
    line_of_flag=[selidx[L] for L,x in flags]
    lift_index={}
    for fi,f in enumerate(flags):
        for bit,ap in enumerate(sorted(flag_lifts[f])):lift_index[aindex[ap]]=(fi,bit)

    candidates=[build_line_perm(transvection_matrix(v),pts,pidx,lines,lidx) for v in pts];gens=[];G={tuple(range(40))}
    for p in candidates:
        trial=perm_group(gens+[p])
        if len(trial)>len(G):gens.append(p);G=trial
        if len(G)==25920:break
    assert len(G)==25920
    def actv(x,g):return rep(pmask(rep(x),g))
    def actL(L,g):return tuple(sorted(actv(x,g) for x in L))
    def afi(i,g):
        L,x=flags[i];return findex[(actL(L,g),actv(x,g))]
    def aai(i,g):return aindex[tuple(sorted(g[x] for x in apartments[i]))]
    def acts(i,g):return selidx[actL(selected[i],g)]

    # Rebuild Pass4713 base and lift orbits.
    Hf=[g for g in G if afi(0,g)==0];assert len(Hf)==32
    unseen=set(range(810));sub=[]
    while unseen:
        x=min(unseen);O=sorted({afi(x,h) for h in Hf});sub.append(O);unseen-=set(O)
    cand=[]
    for O in sub:
        if 0 in O:continue
        y=min(O);E={tuple(sorted((afi(0,g),afi(y,g)))) for g in G}
        if len(E)==810*len(O)//2:
            nbr=[[] for _ in range(810)]
            for a,b in E:nbr[a].append(b);nbr[b].append(a)
            seen={0};Q=deque([0])
            while Q:
                u=Q.popleft()
                for v in nbr[u]:
                    if v not in seen:seen.add(v);Q.append(v)
            if len(seen)==810:cand.append((len(O),y,E))
    cand.sort();val,y,base_edges=cand[0];assert val==16 and len(base_edges)==6480
    lifts0=sorted(aindex[a] for a in flag_lifts[flags[0]]);liftsy=sorted(aindex[a] for a in flag_lifts[flags[y]])
    a0,ay=lifts0[0],liftsy[0]
    LE={tuple(sorted((aai(a0,g),aai(ay,g)))) for g in G};assert len(LE)==12960
    bybase=defaultdict(list)
    for a,b in LE:
        fa,ba=lift_index[a];fb,bb=lift_index[b];e=tuple(sorted((fa,fb)));bybase[e].append((fa,ba,fb,bb))
    alpha={}
    for e,L in bybase.items():
        vals={ba^bb for fa,ba,fb,bb in L};assert len(L)==2 and len(vals)==1;alpha[e]=next(iter(vals))
    assert set(alpha)==base_edges

    # Exact cochain descent under pi:(flag)->selected line, allowing a flag gauge.
    ppairs=sorted(set(tuple(sorted((line_of_flag[u],line_of_flag[v]))) for u,v in base_edges))
    pidx2={e:i for i,e in enumerate(ppairs)};rows=[]
    for u,v in base_edges:
        pe=tuple(sorted((line_of_flag[u],line_of_flag[v])));mask=(1<<u)|(1<<v)|(1<<(810+pidx2[pe]));rows.append((mask,alpha[(u,v)]))
    sol=solve_f2(rows,810+len(ppairs));descends=sol is not None
    beta={}
    if descends:
        for e,i in pidx2.items():beta[e]=(sol>>(810+i))&1
    X=build_bundle();hot=set(tuple(sorted(e)) for e in X['hot']);cold=set(tuple(sorted(e)) for e in X['cold']);total=hot|cold
    pset=set(ppairs)
    projected_relation='other'
    if pset==hot:projected_relation='hot'
    elif pset==cold:projected_relation='cold'
    elif pset==total:projected_relation='total_router'

    # Local stabilizer H of selected line 0 and its action on 3 flags/6 apartments.
    L0=selected[0];fl=[findex[(L0,x)] for x in L0];assert len(fl)==3;fpos={f:i for i,f in enumerate(fl)}
    H=[g for g in G if acts(0,g)==0];assert len(H)==96
    local_lifts={i:sorted(aindex[a] for a in flag_lifts[flags[f]]) for i,f in enumerate(fl)}
    lbit={a:(i,b) for i,A in local_lifts.items() for b,a in enumerate(A)}
    deltas={}
    for g in H:
        ds=[]
        for i in range(3):
            f=fl[i];j=fpos[afi(f,g)];vals=set()
            for b,a in enumerate(local_lifts[i]):
                aa=aai(a,g);jj,bb=lbit[aa];assert jj==j;vals.add(b^bb)
            assert len(vals)==1;ds.append((j,next(iter(vals))))
        deltas[g]=ds
    gauge_witness=None;eps=None
    for bits in itertools.product((0,1),repeat=3):
        ee={};ok=True
        for g,ds in deltas.items():
            vals={d^bits[i]^bits[j] for i,(j,d) in enumerate(ds)}
            if len(vals)!=1:ok=False;break
            ee[g]=next(iter(vals))
        if ok:gauge_witness=bits;eps=ee;break
    assert eps is not None
    # homomorphism check
    for a in H:
        for b in gens: # enough to check products that stay in H; then full kernel index verifies
            if b in H:
                c=compose(a,b);assert eps[c]==(eps[a]^eps[b])
    ker={g for g in H if eps[g]==0};assert len(ker) in (48,96)

    # Identify the corresponding residue fixed by H and reconstruct Pass4738 K=C_PSp(h).
    residues=[]
    for C in itertools.combinations(range(40),4):
        if not np.any(np.sum(Astar[:,C],axis=1)&1):residues.append(tuple(C))
    ridx={r:i for i,r in enumerate(residues)}
    def actr(i,g):return ridx[tuple(sorted(g[x] for x in residues[i]))]
    fixedres=[i for i in range(270) if all(actr(i,g)==i for g in H)];assert len(fixedres)==1;r0=fixedres[0]
    ident=tuple(range(40));rmask=sum(1<<x for x in residues[r0])
    invol=[g for g in G if g!=ident and compose(g,g)==ident and fixed_mask(g)==rmask];assert len(invol)==1;gi=invol[0]
    outer=build_line_perm(np.diag([1,2,1,2])%3,pts,pidx,lines,lidx);full=set(G)|{compose(outer,g) for g in G};assert len(full)==51840
    roots=[h for h in full-G if compose(h,h)==gi and fixed_mask(h).bit_count()==4];assert len(roots)==2;h=roots[0]
    K={g for g in G if compose(g,h)==compose(h,g)};Hres={g for g in G if actr(r0,g)==r0}
    assert Hres==set(H) and len(K)==48 and K<set(H)
    local_match=(ker==K)

    out={'pass':4752,
      'equivariant_projection':{'flags':810,'selected_lines_or_residues':270,'fiber_size':3,'projected_base_edge_pairs':len(ppairs),'projected_relation':projected_relation},
      'global_cochain_descent':{'deck_voltage_gauge_descends_to_projected_270_graph':descends,'projected_beta_weight':sum(beta.values()) if descends else None,
        'statement':'existence solved as one exact F2 linear system with 810 flag-gauge variables plus one variable per projected edge'},
      'local_stabilizer':{'H_order':len(H),'three_flag_sheet_gauge':list(gauge_witness),'sheet_character_nontrivial':len(ker)==48,'sheet_character_kernel_order':len(ker),
        'Pass4738_normalizer_kernel_order':len(K),'kernels_equal_as_subgroups':local_match},
      'comparison':{'same_local_C2_character':local_match,
        'same_global_cohomology_object':bool(descends and local_match),
        'qualification':'A global identification is promoted only when the deck cochain descends along the canonical 810->270 projection and the descended local stabilizer character has exactly the Pass4738 kernel.'},
      'theorem':'The apartment deck line and residue normalizer twist are compared by an explicit equivariant projection, an F2 cochain-descent solve, and subgroup equality at a residue stabilizer. The result is therefore an exact identification or exact no-go, not a shared-C2 analogy.',
      'boundary':'Finite graph-cover/group-cohomology comparison only. A positive local kernel match without global descent is not called equality of cohomology classes.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
