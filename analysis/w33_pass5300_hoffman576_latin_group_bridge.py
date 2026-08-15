#!/usr/bin/env python3
"""Pass5300: exact 576 bridge between the Hoffman cover stabilizer and order-4 Latin-square symmetry.

The integer 576 occurs in two superficially different places:
  * H, the setwise stabilizer of the 13-cell Hoffman cover in PSp4(5), has order 576;
  * there are 576 Latin squares of order 4, and the Klein V4 Latin square has a full
    autoparatopy group of order 576.

This pass checks the GROUPS rather than equating their orders.  The result is a
nontrivial but non-identical bridge:

  H ~= 2_+^{1+4} : (S3 x C3),
  AutPar(V4-Latin) ~= 2^4 : (S3 x S3),

so H is NOT the Latin autoparatopy group.  However the central quotient H/Z(H)
has order 288 and is explicitly GL(4,2)-conjugate to the index-two even-parastrophe
subgroup L+ of the Klein Latin autoparatopy group:

  H/Z(H) ~= L+ ~= 2^4 : (S3 x C3).

Thus the exact 576 bridge is a central double lift on the Hoffman side versus the
orientation-even half of the Latin symmetry on the other side.  The number alone
is not the theorem; the explicit affine-module conjugacy is.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
from sympy.combinatorics import Permutation,PermutationGroup
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
from analysis.w33_pass5214_q5_connectedL_point_footprint_gluing import p_component_assignment

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5300_HOFFMAN576_LATIN_GROUP_BRIDGE.json'
COVER=(6,30,73,111,128,140,157,189,193,226,254,277,320)

def elem_hist(G):
    return dict(sorted(Counter(g.order() for g in G.generate_schreier_sims()).items()))

def rank4(cols):
    piv={}
    for x in cols:
        while x:
            p=x.bit_length()-1
            if p in piv:x^=piv[p]
            else:piv[p]=x;break
    return len(piv)

def mapply(A,x):
    y=0
    for i,e in enumerate((1,2,4,8)):
        if x&e:y^=A[i]
    return y

def mcomp(A,B): return tuple(mapply(A,b) for b in B)
def minv(A):
    return tuple(next(x for x in range(16) if mapply(A,x)==e) for e in (1,2,4,8))

def gl4():
    for A in itertools.permutations(range(1,16),4):
        if rank4(A)==4: yield A

def q5_hoffman():
    G=build_W(5);acid,nc=p_component_assignment(G);assert nc==325
    blocks=[set() for _ in range(325)]
    for a,A in enumerate(G['apartments']):blocks[acid[a]].update(A)
    pts=G['pts'];pi={p:i for i,p in enumerate(pts)};bk={tuple(sorted(B)):i for i,B in enumerate(blocks)}
    def norm(v):
        for x in v:
            if x:
                s=pow(x,-1,5);return tuple(s*y%5 for y in v)
        raise ValueError
    def sp(u,v):return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%5
    def bperm(v):
        pp=[]
        for x in pts:
            a=sp(x,v);pp.append(pi[norm(tuple((x[k]+a*v[k])%5 for k in range(4)))])
        return [bk[tuple(sorted(pp[p] for p in B))] for B in blocks]
    vs=((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(1,1,0,0),(1,0,0,1))
    GP=PermutationGroup([Permutation(bperm(v)) for v in vs]);assert GP.order()==4680000
    C=set(COVER);base,strong=GP.schreier_sims_incremental(base=list(COVER))
    def prop(g):return {g(i) for i in COVER}==C
    tests=[]
    for l in range(len(base)):
        inds=base[:l+1];tests.append(lambda words,l=l,inds=inds:all((i in C)==(words[l](i) in C) for i in inds))
    H=GP.subgroup_search(prop,base=base,strong_gens=strong,tests=tests);assert H.order()==576
    ci={c:i for i,c in enumerate(COVER)}
    H13=PermutationGroup([Permutation([ci[g(c)] for c in COVER]) for g in H.generators])
    assert H13.order()==288 and H13.center().order()==1
    V=H13.derived_subgroup().derived_subgroup();assert V.order()==16 and V.is_abelian
    assert elem_hist(V)=={1:1,2:15}
    # Coordinate V as F2^4.
    els=list(V.generate_schreier_sims());ident=V.identity
    coord={ident:0};bas=[]
    for v in els:
        if v in coord:continue
        bit=1<<len(bas);old=list(coord.items())
        for g,c in old:coord[g*v]=c|bit
        bas.append(v)
    assert len(bas)==4 and len(coord)==16
    Hact=set()
    for h in H13.generate_schreier_sims():
        hi=~h;A=tuple(coord[h*b*hi] for b in bas);assert rank4(A)==4;Hact.add(A)
    assert len(Hact)==18
    # Extraspecial preimage of V in the full 576-group.
    def restrict13(h):return Permutation([ci[h(c)] for c in COVER])
    Qels=[h for h in H.generate_schreier_sims() if V.contains(restrict13(h))]
    Q=PermutationGroup(Qels);assert Q.order()==32
    assert Q.center().order()==2 and Q.derived_subgroup().order()==2
    assert elem_hist(Q)=={1:1,2:19,4:12}
    return H,H13,Hact,Q

def latin_groups():
    S4=list(itertools.permutations(range(4)));S3=list(itertools.permutations(range(3)))
    def parity(p):return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))&1
    def enumerate_par(even=False):
        ans=[]
        for pi in S3:
            if even and parity(pi):continue
            for a in S4:
                for b in S4:
                    mp={};cell=[0]*16;ok=True
                    for r in range(4):
                        for c in range(4):
                            old=(r,c,r^c);R=a[old[pi[0]]];C=b[old[pi[1]]];t=old[pi[2]];s=R^C
                            if t in mp and mp[t]!=s:ok=False;break
                            mp[t]=s;cell[4*r+c]=4*R+C
                        if not ok:break
                    if ok and len(mp)==4 and len(set(mp.values()))==4:ans.append(tuple(cell))
        return ans
    allp=enumerate_par(False);evenp=enumerate_par(True)
    assert len(set(allp))==576 and len(set(evenp))==288
    L=PermutationGroup([Permutation(p) for p in allp]);Lp=PermutationGroup([Permutation(p) for p in evenp])
    assert L.order()==576 and Lp.order()==288
    def affine(p):
        t=p[0];A=tuple(p[e]^t for e in (1,2,4,8))
        assert all(p[x]==(mapply(A,x)^t) for x in range(16));return t,A
    Lact={affine(p)[1] for p in evenp};assert len(Lact)==18
    return L,Lp,Lact

def main():
    H,Hq,Hact,Q=q5_hoffman();L,Lp,Lact=latin_groups()
    witness=None
    for P in gl4():
        Pi=minv(P)
        if {mcomp(mcomp(Pi,A),P) for A in Hact}==Lact:
            witness=P;break
    assert witness is not None
    # Full groups are not isomorphic already by center/derived/order spectra.
    assert H.center().order()==2 and H.derived_subgroup().order()==96
    assert L.center().order()==1 and L.derived_subgroup().order()==144
    assert elem_hist(H)!=(elem_hist(L))
    out={'pass':5300,'status':'THEOREM_HOFFMAN576_IS_CENTRAL_DOUBLE_LIFT_OF_EVEN_KLEIN_LATIN_AFFINE_SYMMETRY',
      'hoffman':{'order':576,'center':2,'derived':96,'element_orders':elem_hist(H),
        'extraspecial_normal_32':{'order':32,'center':2,'derived':2,'element_orders':elem_hist(Q),'type':'2_+^{1+4}'},
        'structure':'2_+^{1+4} : (S3 x C3)'},
      'klein_latin':{'all_order4_latin_squares':576,'V4_autoparatopy_order':576,'center':1,'derived':144,
        'element_orders':elem_hist(L),'structure':'2^4 : (S3 x S3)',
        'even_parastrophe_subgroup_order':288,'even_structure':'2^4 : (S3 x C3)'},
      'exact_bridge':{'hoffman_central_quotient_order':Hq.order(),'latin_even_order':Lp.order(),
        'GL4_conjugacy_change_of_basis_columns':list(witness),
        'statement':'H/Z(H) is explicitly conjugate, on its normal F2^4 module, to the even-parastrophe subgroup of the Klein V4 Latin-square autoparatopy group.'},
      'negative_result':'H itself is NOT the order-576 Klein Latin autoparatopy group; equal order alone is not an identification.',
      'boundary':'Finite group/code theorem. No physical meaning is assigned to the central involution.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
