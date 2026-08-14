#!/usr/bin/env python3
"""Pass5105: the C2 root controller unifies the BT865 dual torsors.

The type-C2 maximal unipotent U81 fixing one W33 chamber contains the canonical
BT865 point-state H27 and line-program F3^3 normal O3 subgroups.  Their product
is U, their intersection is U' of order 9, and the common characteristic
center has order 3.  On the protected native H1(F3), U acts as one regular
module; restricting that single regular module recovers BT865's three regular
copies for either index-three subgroup.
"""
from __future__ import annotations
import itertools,json,math,random
from collections import Counter,deque
from pathlib import Path
import numpy as np
from analysis.bt865_dual_torsor_steinberg_compiler import GF3Span,nullspace_mod3
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5105_U81_DUAL_TORSOR_CONTROLLER.json'
P=3

def canon(v):
    for x in v:
        if x%3:
            s=1 if x%3==1 else 2;return tuple((s*y)%3 for y in v)
    raise ValueError
def symp(x,y):return (x[0]*y[2]-x[2]*y[0]+x[1]*y[3]-x[3]*y[1])%3
def comp(a,b):return tuple(a[b[i]] for i in range(len(b)))
def invperm(g):
    z=[0]*len(g)
    for i,j in enumerate(g):z[j]=i
    return tuple(z)
def closure(gens,n=40):
    I=tuple(range(n));S={I};Q=deque([I])
    while Q:
        a=Q.popleft()
        for g in gens:
            z=comp(g,a)
            if z not in S:S.add(z);Q.append(z)
    return S
def order(g):
    I=tuple(range(len(g)));x=I
    for n in range(1,100):
        x=comp(g,x)
        if x==I:return n
    raise RuntimeError
def center(G):return {g for g in G if all(comp(g,h)==comp(h,g) for h in G)}
def derived(G):
    cs=[]
    for a,b in itertools.product(G,repeat=2):cs.append(comp(comp(comp(a,b),invperm(a)),invperm(b)))
    return closure(cs,len(next(iter(G))))

def main():
    pts=sorted({canon(v) for v in itertools.product(range(3),repeat=4) if any(v)});pi={p:i for i,p in enumerate(pts)};assert len(pts)==40
    adj=[[False]*40 for _ in range(40)]
    for i,j in itertools.combinations(range(40),2):
        if symp(pts[i],pts[j])==0:adj[i][j]=adj[j][i]=True
    lines=[frozenset(c) for c in itertools.combinations(range(40),4) if all(adj[i][j] for i,j in itertools.combinations(c,2))];li={L:i for i,L in enumerate(lines)};assert len(lines)==40
    def lperm(g):return tuple(li[frozenset(g[x] for x in L)] for L in lines)
    # PSp(4,3) from transvections.
    def trans(v):
        out=[]
        for x in pts:
            w=symp(x,v);out.append(pi[canon(tuple((x[t]+w*v[t])%3 for t in range(4)))])
        return tuple(out)
    PSp=closure([trans(v) for v in pts]);assert len(PSp)==25920
    # Four standard positive-root groups in one C2 Borel.
    I4=np.eye(4,dtype=int)%3
    def E(i,j):M=np.zeros((4,4),dtype=int);M[i,j]=1;return M
    X=[E(0,1)-E(3,2),E(1,3),E(0,3)+E(1,2),E(0,2)]
    def mperm(M):
        return tuple(pi[canon(tuple(map(int,(M@np.array(x,dtype=int))%3)))] for x in pts)
    rg=[mperm((I4+Z)%3) for Z in X];U0=closure(rg);assert len(U0)==81
    fixedp=[p for p in range(40) if all(g[p]==p for g in U0)];fixedl=[l for l in range(40) if all(lperm(g)[l]==l for g in U0)];assert fixedp==fixedl==[13]
    # Align the root chamber with BT865's point0/line0 chamber.
    gmap=next(g for g in PSp if g[13]==0 and lperm(g)[13]==0);gi=invperm(gmap)
    conj=lambda h:comp(comp(gmap,h),gi)
    r=[conj(x) for x in rg];U={conj(x) for x in U0};assert len(U)==81
    Hstate=closure([r[0],r[2]]);Hflat=closure([r[1],r[2],r[3]]);assert len(Hstate)==len(Hflat)==27
    point_stab={g for g in PSp if g[0]==0};line_stab={g for g in PSp if lperm(g)[0]==0};assert len(point_stab)==len(line_stab)==648
    assert all(comp(comp(g,h),invperm(g)) in Hstate for g in point_stab for h in Hstate)
    assert all(comp(comp(g,h),invperm(g)) in Hflat for g in line_stab for h in Hflat)
    inter=Hstate&Hflat;Ud=derived(U);assert len(inter)==len(Ud)==9 and inter==Ud
    assert len(center(U))==3 and center(Hstate)==center(U) and len(center(Hflat))==27
    assert closure(list(Hstate|Hflat))==U
    # Torsor actions reproduce BT865's point-state and disjoint-line program shells.
    point_shell=[x for x in range(40) if x!=0 and not adj[0][x]];line_shell=[l for l in range(40) if l!=0 and not (lines[l]&lines[0])]
    assert len({g[point_shell[0]] for g in Hstate})==27
    assert len({lperm(g)[line_shell[0]] for g in Hflat})==27
    # Canonical diagonal V4 complement; it preserves both O3 subgroups.
    Dm=[]
    for vals in itertools.product((1,2),repeat=4):
        if vals[0]*vals[2]%3==vals[1]*vals[3]%3:
            M=np.diag(vals)%3;p=mperm(M);pc=conj(p)
            if pc not in Dm:Dm.append(pc)
    V4=set(Dm);assert len(V4)==4 and Counter(order(g) for g in V4)==Counter({2:3,1:1}) and closure(list(U|V4)) .__len__()==324
    assert all(comp(comp(v,h),invperm(v)) in Hstate for v in V4 for h in Hstate)
    assert all(comp(comp(v,h),invperm(v)) in Hflat for v in V4 for h in Hflat)
    # Steinberg character on U from alternating fixed-building trace.
    flags=[(p,l) for l,L in enumerate(lines) for p in L];lp={g:lperm(g) for g in U}
    def stchar(g):
        fixedp=sum(g[p]==p for p in range(40));fixedl=sum(lp[g][l]==l for l in range(40));fixedf=sum(g[p]==p and lp[g][l]==l for p,l in flags)
        return fixedf-fixedp-fixedl+1
    assert Counter(stchar(g) for g in U)==Counter({0:80,81:1})
    # Native H1(F3): one U-orbit supplies all 81 classes modulo boundaries.
    edges=sorted((i,j) for i,j in itertools.combinations(range(40),2) if adj[i][j]);ei={e:i for i,e in enumerate(edges)}
    triangles=sorted({tuple(sorted(t)) for L in lines for t in itertools.combinations(sorted(L),3)})
    d0=[[0]*240 for _ in range(40)]
    for k,(a,b) in enumerate(edges):d0[a][k]=2;d0[b][k]=1
    d1=[]
    for x,y,z in triangles:
        col=[0]*240;col[ei[(y,z)]]=1;col[ei[(x,z)]]=2;col[ei[(x,y)]]=1;d1.append(col)
    cycles,_=nullspace_mod3(d0);B=GF3Span(d1);assert len(cycles)==201 and B.rank==120
    def act_edges(g,v):
        out=[0]*240
        for k,c in enumerate(v):
            if not c:continue
            a,b=edges[k];ga,gb=g[a],g[b]
            if ga<gb:j,s=ei[(ga,gb)],1
            else:j,s=ei[(gb,ga)],2
            out[j]=(out[j]+s*c)%3
        return out
    rng=random.Random(5104);ordered=sorted(U);witness=None
    for attempt in range(1,51):
        cand=[0]*240
        for basis in cycles:
            c=rng.randrange(3)
            if c:cand=[(cand[i]+c*basis[i])%3 for i in range(240)]
        trial=B.copy();old=trial.rank;orb=[act_edges(g,cand) for g in ordered]
        for v in orb:trial.add(v)
        if trial.rank-old==81:
            witness={'seed':5104,'attempt':attempt,'orbit_size':len({tuple(v) for v in orb}),'rank_gain_mod_boundaries':81,'seed_support_size':sum(bool(x) for x in cand)};break
    assert witness is not None and witness['orbit_size']==81
    out={'pass':5105,'status':'THEOREM_U81_DUAL_TORSOR_CONTROLLER','U':{'order':81,'center':3,'derived':9,'order_census':dict(Counter(order(g) for g in U))},
         'state_H27':{'order':27,'center':3,'normal_in_point_stabilizer':True,'regular_on_27_noncollinear_points':True},
         'program_F3_3':{'order':27,'center':27,'normal_in_line_stabilizer':True,'regular_on_27_disjoint_lines':True},
         'weld':{'intersection_order':9,'intersection_equals_U_derived':True,'generated_product_order':81,'state_center_equals_U_center':True},
         'V4':{'order':4,'normalizes_state_H27':True,'normalizes_program_F3_3':True,'semidirect_controller_order':324},
         'Steinberg':{'complex_restriction':'Reg(U81)','character':{'81':1,'0':80},'native_restriction':'H1(F3)|U ~= F3[U] free rank 1','witness':witness,
                      'BT865_restrictions':'Restricting Reg(U81) to either index-3 subgroup gives 3 Reg(H27) and 3 Reg(F3^3).'},
         'boundary':'Exact finite group/module/controller theorem. It does not identify this algebraic controller with fabricated optical hardware or timing.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
