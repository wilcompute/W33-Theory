#!/usr/bin/env python3
"""Pass 4752 — the apartment deck class descends to the Pass4738 normalizer cover.

There is a canonical PSp-equivariant projection from the 810 selected flags
(L,x) to their 270 selected lines L. We rebuild the Pass4713 double cover,
extract its binary edge voltage alpha, and solve the exact F2 descent problem

    alpha(u,v) + s_u + s_v = beta(pi(u),pi(v)).

The solution exists. The projected base relation has 2160 edges (degree 16),
distinct from the 405 hot and 1620 cold router relations. Beta defines a
connected 540-vertex double cover of that 270-vertex orbital graph.

The gauged apartment action descends to this 540-set. Its PSp image has order
25920 and is transitive, hence the point stabilizer has order 48. For the
selected-line stabilizer H of order 96, the local sheet character has kernel
exactly K=C_PSp(h), where h is a Pass4738 outer order-four root. Thus the
540->270 descended deck cover is literally the homogeneous normalizer cover
PSp/K -> PSp/H. This is a global identification, not a shared-C2 analogy.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict,deque
from pathlib import Path
import networkx as nx
import numpy as np
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry,build_line_perm,perm_group,transvection_matrix
from w33_pass4587_w33_derived_d4_triality import rank_basis_int
from w33_pass4716_selected270_bundle_connection import build_bundle
from w33_pass4745_invariant_h1_character import compose,pmask
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4752_DECK_NORMALIZER_TWIST_COMPARISON.json'

def fixed_mask(p):return sum(1<<i for i,j in enumerate(p) if i==j)
def solve_f2(rows):
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
    flags_by_line=defaultdict(list)
    for fi,r in enumerate(line_of_flag):flags_by_line[r].append(fi)
    assert set(map(len,flags_by_line.values()))=={3}
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

    # Deterministic Pass4713 orbital seed independently executed: y=173 is the
    # first connected self-paired valency-16 suborbit representative.
    y=173
    base_edges={tuple(sorted((afi(0,g),afi(y,g)))) for g in G}
    B=nx.Graph();B.add_nodes_from(range(810));B.add_edges_from(base_edges)
    assert len(base_edges)==6480 and set(dict(B.degree()).values())=={16} and nx.is_connected(B) and nx.diameter(B)==5
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

    # Exact cochain descent under pi:(flag)->selected line.
    ppairs=sorted(set(tuple(sorted((line_of_flag[u],line_of_flag[v]))) for u,v in base_edges));assert len(ppairs)==2160
    pidx2={e:i for i,e in enumerate(ppairs)};rows=[]
    for u,v in base_edges:
        pe=tuple(sorted((line_of_flag[u],line_of_flag[v])));rows.append(((1<<u)|(1<<v)|(1<<(810+pidx2[pe])),alpha[(u,v)]))
    sol=solve_f2(rows);assert sol is not None
    sgauge=[(sol>>f)&1 for f in range(810)];beta={e:(sol>>(810+i))&1 for e,i in pidx2.items()}
    assert Counter(beta.values())==Counter({1:1172,0:988})

    X=build_bundle();hot=set(tuple(sorted(e)) for e in X['hot']);cold=set(tuple(sorted(e)) for e in X['cold']);pset=set(ppairs)
    assert pset.isdisjoint(hot) and pset.isdisjoint(cold)
    P=nx.Graph();P.add_nodes_from(range(270));P.add_edges_from(ppairs);assert set(dict(P.degree()).values())=={16} and nx.is_connected(P)

    # Descended 540-vertex beta cover.
    D=nx.Graph();D.add_nodes_from(range(540))
    for (r,s),b in beta.items():
        for t in (0,1):D.add_edge(2*r+t,2*s+(t^b))
    assert D.number_of_edges()==4320 and set(dict(D.degree()).values())=={16} and nx.is_connected(D) and nx.diameter(D)==4

    # The gauged apartment action descends to the 540-set. Check independence
    # from the three flags over each line for the PSp generators.
    sorted_lifts={f:sorted(aindex[a] for a in flag_lifts[flags[f]]) for f in range(810)}
    def descend_perm(g):
        out=[]
        for r in range(270):
            for t in (0,1):
                vals=set()
                for f in flags_by_line[r]:
                    oldbit=t^sgauge[f];a=sorted_lifts[f][oldbit];aa=aai(a,g);f2,b2=lift_index[aa]
                    vals.add((line_of_flag[f2],b2^sgauge[f2]))
                assert len(vals)==1
                r2,t2=next(iter(vals));out.append(2*r2+t2)
        return tuple(out)
    gen540=[descend_perm(g) for g in gens]
    Dedges={tuple(sorted(e)) for e in D.edges()}
    for p in gen540:assert {tuple(sorted((p[u],p[v]))) for u,v in Dedges}==Dedges
    G540=perm_group(gen540,n=540,limit=30000);assert len(G540)==25920
    orbit0={p[0] for p in G540};assert len(orbit0)==540

    # Local selected-line stabilizer character.
    L0=selected[0];fl=[findex[(L0,x)] for x in L0];fpos={f:i for i,f in enumerate(fl)};assert len(fl)==3
    H=[g for g in G if acts(0,g)==0];assert len(H)==96
    local_lifts={i:sorted(aindex[a] for a in flag_lifts[flags[f]]) for i,f in enumerate(fl)}
    lbit={a:(i,b) for i,A in local_lifts.items() for b,a in enumerate(A)};deltas={}
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
    assert gauge_witness==(0,1,1) and eps is not None
    for a in H:
        for b in H:assert eps[compose(a,b)]==(eps[a]^eps[b])
    ker={g for g in H if eps[g]==0};assert len(ker)==48

    # Identify the corresponding involution residue and Pass4738 normalizer kernel.
    residues=[]
    for C in itertools.combinations(range(40),4):
        if not np.any(np.sum(Astar[:,C],axis=1)&1):residues.append(tuple(C))
    ridx={r:i for i,r in enumerate(residues)}
    def actr(i,g):return ridx[tuple(sorted(g[x] for x in residues[i]))]
    fixedres=[i for i in range(270) if all(actr(i,g)==i for g in H)];assert fixedres==[233];r0=233
    ident=tuple(range(40));rmask=sum(1<<x for x in residues[r0])
    invol=[g for g in G if g!=ident and compose(g,g)==ident and fixed_mask(g)==rmask];assert len(invol)==1;gi=invol[0]
    outer=build_line_perm(np.diag([1,2,1,2])%3,pts,pidx,lines,lidx);full=set(G)|{compose(outer,g) for g in G};assert len(full)==51840
    roots=[h for h in full-G if compose(h,h)==gi and fixed_mask(h).bit_count()==4];assert len(roots)==2;h=roots[0]
    K={g for g in G if compose(g,h)==compose(h,g)};Hres={g for g in G if actr(r0,g)==r0}
    assert Hres==set(H) and len(K)==48 and K<set(H) and ker==K

    out={'pass':4752,
      'equivariant_projection':{'flags':810,'selected_lines_or_residues':270,'fiber_size':3,'projected_base_edge_pairs':2160,'projected_relation_degree':16,'projected_relation':'distinct degree-16 orbital; disjoint from hot and cold router relations'},
      'global_cochain_descent':{'deck_voltage_descends_after_flag_gauge':True,'flag_gauge_weight':sum(sgauge),'projected_beta_weight':sum(beta.values()),'projected_beta_zero_edges':988,'projected_beta_one_edges':1172},
      'descended_double_cover':{'vertices':540,'edges':4320,'degree':16,'connected':True,'diameter':4,'PSp_image_order':25920,'PSp_vertex_orbit':540,'point_stabilizer_order':48},
      'local_stabilizer':{'H_order':96,'three_flag_sheet_gauge':list(gauge_witness),'sheet_character_nontrivial':True,'sheet_character_kernel_order':48,'Pass4738_normalizer_kernel_order':48,'kernels_equal_as_subgroups':True,'fixed_residue_index':233},
      'comparison':{'same_local_C2_character':True,'same_global_homogeneous_cover':True,'homogeneous_description':'PSp(4,3)/K -> PSp(4,3)/H with |K|=48, |H|=96','meaning':'the descended apartment deck character is exactly the Pass4738 normalizer quotient H/K'},
      'theorem':'The apartment deck cocycle descends through the canonical 810->270 projection to a connected 540->270 double cover of a degree-16 orbital graph. Its descended PSp action is transitive with order-48 point stabilizer, and that stabilizer is literally the Pass4738 kernel K=C_PSp(h) inside the order-96 residue stabilizer H. Hence the descended apartment deck cover is the homogeneous normalizer cover PSp/K -> PSp/H.',
      'boundary':'Exact finite graph-cover/group-cohomology identification. The descended degree-16 orbital is distinct from the hot and cold router relations; no optical or gauge-field interpretation is inferred.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
