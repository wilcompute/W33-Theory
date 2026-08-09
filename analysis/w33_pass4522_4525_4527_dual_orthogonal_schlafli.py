#!/usr/bin/env python3
"""Passes 4522, 4525, 4527 -- the 366D dual quotient and its O^-(6,2) core.

4522 corrects the relation between the prism span P and the even dual E:
  dim D=1581, dim P=1215, dim E=1580, dim(P cap E)=1214,
  hence dim(D/P)=dim(E/(P cap E))=366.
The 366D quotient has a fixed line inside a fixed hyperplane.  In the resulting
364D middle module an outer-invariant 358D submodule is found explicitly; the
6D quotient is faithful for PSp(4,3), has a unique nondegenerate invariant
alternating form and a unique invariant minus-type quadratic refinement.  The
inner and outer images have orders 25920 and 51840 respectively, realizing the
standard O^-(6,2) shadow.  No claim is made that the displayed 358D submodule is
the entire Loewy series of the 364D middle module.

4525 uses the 27 nonzero singular vectors of that minus space. Polar
orthogonality gives SRG(27,10,1,5). An explicit graph isomorphism and generator
conjugation identify this permutation representation with the repo's existing
W(E6) action on the 27 cubic-surface lines.

4527 uses the 36 anisotropic vectors. Polar orthogonality gives
SRG(36,15,6,6). An explicit graph isomorphism and generator conjugation identify
this representation with the repo's 36 double-sixes, where adjacency means the
two 12-line double-six supports intersect in four cubic-surface lines.
"""
from __future__ import annotations

import importlib.util,itertools,json,math
from collections import Counter,deque
from pathlib import Path
import numpy as np

from w33_pass4495_4502_distance_prism_reconstruction import geometry
from w33_pass4511_4514_dual_even_prism_ihara import build_groups,perm_mask

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS4522_4525_4527_DUAL_ORTHOGONAL_SCHLAFLI.json'

class CoordBasis:
    def __init__(self):self.piv={};self.orig=[]
    def add(self,orig:int):
        y=int(orig);combo=0
        while y:
            p=y.bit_length()-1
            if p in self.piv:
                v,c=self.piv[p];y^=v;combo^=c
            else:
                i=len(self.orig);self.orig.append(int(orig));self.piv[p]=(y,combo^(1<<i));return True
        return False
    def coords(self,y:int):
        y=int(y);combo=0
        while y:
            p=y.bit_length()-1
            if p not in self.piv:return None
            v,c=self.piv[p];y^=v;combo^=c
        return combo

def rref_int_rows(rows,n):
    A=[int(x) for x in rows if x];r=0;piv=[]
    for c in range(n):
        k=next((i for i in range(r,len(A)) if (A[i]>>c)&1),None)
        if k is None:continue
        A[r],A[k]=A[k],A[r]
        for i in range(len(A)):
            if i!=r and ((A[i]>>c)&1):A[i]^=A[r]
        piv.append(c);r+=1
        if r==len(A):break
    return A[:r],piv

def nullspace_from_rows(rows,n):
    R,piv=rref_int_rows(rows,n);ps=set(piv);out=[]
    for f in range(n):
        if f in ps:continue
        x=1<<f
        for row,pc in zip(R,piv):
            if (row>>f)&1:x|=1<<pc
        out.append(x)
    return out

def perm_coordmask(x,p):
    out=0;y=int(x)
    while y:
        b=y&-y;i=b.bit_length()-1;out|=1<<p[i];y-=b
    return out

def apply_cols(cols,x):
    out=0;y=int(x)
    while y:
        b=y&-y;i=b.bit_length()-1;out^=cols[i];y-=b
    return out

def cols_to_np(cols,n):
    M=np.zeros((n,n),dtype=np.uint8)
    for j,c in enumerate(cols):
        y=int(c)
        while y:
            b=y&-y;i=b.bit_length()-1;M[i,j]=1;y-=b
    return M

def rank2(M):
    A=np.asarray(M,dtype=np.uint8).copy();m,n=A.shape;r=0;piv=[]
    for c in range(n):
        z=np.flatnonzero(A[r:,c])
        if not len(z):continue
        rr=r+int(z[0]);A[[r,rr]]=A[[rr,r]]
        for i in np.flatnonzero(A[:,c]):
            if i!=r:A[i]^=A[r]
        piv.append(c);r+=1
        if r==m:break
    return r,A,piv

def nullspace2(M):
    r,R,piv=rank2(M);n=R.shape[1];ps=set(piv);out=[]
    for f in range(n):
        if f in ps:continue
        x=np.zeros(n,dtype=np.uint8);x[f]=1
        for i,c in reversed(list(enumerate(piv))):x[c]=np.dot(R[i],x)%2
        out.append(x)
    return np.asarray(out,dtype=np.uint8)

def vecint(v):return sum(int(b)<<i for i,b in enumerate(v) if b)
def intvec(x,n):return np.array([(x>>i)&1 for i in range(n)],dtype=np.uint8)

def cyclic_span(seed,gens):
    piv={};basis=[];q=deque()
    def add(x):
        y=int(x)
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;basis.append(int(x));q.append(int(x));return True
        return False
    add(seed)
    while q:
        x=q.popleft()
        for g in gens:add(apply_cols(g,x))
    return basis

def matrix_group(gens):
    n=gens[0].shape[0];I=np.eye(n,dtype=np.uint8)
    key=lambda M:bytes(M.ravel())
    seen={key(I):I};q=deque([I])
    while q:
        a=q.popleft()
        for g in gens:
            c=(g@a)%2;k=key(c)
            if k not in seen:seen[k]=c;q.append(c)
    return list(seen.values())

def pgroup(gens,n):
    I=tuple(range(n));seen={I};q=deque([I])
    while q:
        a=q.popleft()
        for g in gens:
            c=tuple(g[a[i]] for i in range(n))
            if c not in seen:seen.add(c);q.append(c)
    return seen

def srg(A):
    n=len(A);deg=set(map(int,A.sum(1)));aa=set();nn=set()
    for i,j in itertools.combinations(range(n),2):
        c=int(np.dot(A[i],A[j]));(aa if A[i,j] else nn).add(c)
    assert len(deg)==len(aa)==len(nn)==1
    return [n,next(iter(deg)),next(iter(aa)),next(iter(nn))]

def q_from_F(F,x):
    z=0
    for i in range(len(x)):
        for j in range(i+1,len(x)):
            z^=int(F[i,j]&x[i]&x[j])
    return z

def alt_form_space(gens):
    n=gens[0].shape[0];pairs=[(i,j) for i in range(n) for j in range(i+1,n)];eq=[]
    basis=[]
    for k in range(len(pairs)):
        F=np.zeros((n,n),dtype=np.uint8);i,j=pairs[k];F[i,j]=F[j,i]=1;basis.append(F)
    for g in gens:
        ds=[((g.T@F@g)%2)^F for F in basis]
        for i in range(n):
            for j in range(n):eq.append([int(D[i,j]) for D in ds])
    ns=nullspace2(np.asarray(eq,dtype=np.uint8));assert len(ns)==1
    F=np.zeros((n,n),dtype=np.uint8)
    for bit,(i,j) in zip(ns[0],pairs):F[i,j]=F[j,i]=bit
    return F

def build_module():
    pts,pidx,lines,A,apartments,apmasks,H=geometry();n=1620
    Hrows=[]
    for row in H:
        x=0
        for j,b in enumerate(row):
            if b:x|=1<<j
        Hrows.append(x)
    Dnull=nullspace_from_rows(Hrows,n);assert len(Dnull)==1581
    apidx={m:i for i,m in enumerate(apmasks)}
    triples=[]
    for i in range(n):
        mi=apmasks[i]
        for j in range(i+1,n):
            k=apidx.get(mi^apmasks[j])
            if k is not None and j<k:triples.append((i,j,k))
    assert len(triples)==2160
    B=CoordBasis()
    for a,b,c in triples:B.add((1<<a)|(1<<b)|(1<<c))
    assert len(B.orig)==1215
    for x in Dnull:B.add(x)
    assert len(B.orig)==1581
    # P has odd vectors, so P cap E is codimension one in P.
    assert any(x.bit_count()&1 for x in B.orig[:1215])

    selected,psp,outer,pgsp=build_groups(pts,pidx,lines)
    linegens=[x[1] for x in selected]
    apgens=[]
    for lp in linegens+[outer]:apgens.append(tuple(apidx[perm_mask(m,lp)] for m in apmasks))
    def quotient_cols(pg):
        cols=[]
        for j in range(1215,1581):
            c=B.coords(perm_coordmask(B.orig[j],pg));assert c is not None;cols.append(c>>1215)
        return cols
    Qgens=[quotient_cols(pg) for pg in apgens[:5]];Qouter=quotient_cols(apgens[5])
    Qm=[cols_to_np(c,366) for c in Qgens]
    fixed=nullspace2(np.vstack([g^np.eye(366,dtype=np.uint8) for g in Qm]));assert fixed.shape==(1,366)
    dualfixed=nullspace2(np.vstack([g.T^np.eye(366,dtype=np.uint8) for g in Qm]));assert dualfixed.shape==(1,366)
    assert int(fixed[0]@dualfixed[0]%2)==0

    # H=ker(dual fixed), with fixed vector first; M=H/<fixed> has dim 364.
    Hb=nullspace2(dualfixed);C=CoordBasis();C.add(vecint(fixed[0]))
    for x in Hb:C.add(vecint(x))
    assert len(C.orig)==365
    Mgens=[]
    for qg in Qgens:
        cc=[]
        for j in range(1,365):
            z=C.coords(apply_cols(qg,C.orig[j]));assert z is not None;cc.append(z>>1)
        Mgens.append(cc)
    Mouter=[]
    for j in range(1,365):
        z=C.coords(apply_cols(Qouter,C.orig[j]));assert z is not None;Mouter.append(z>>1)

    # Exact standard-basis cyclic census and an outer-stable 358D submodule.
    cyc=Counter(len(cyclic_span(1<<i,Mgens)) for i in range(364))
    assert cyc==Counter({364:303,358:49,330:10,284:2})
    seed=54;S=cyclic_span(1<<seed,Mgens);assert len(S)==358
    SB=CoordBasis()
    for x in S:SB.add(x)
    assert all(SB.coords(apply_cols(Mouter,x)) is not None for x in SB.orig)
    for i in range(364):SB.add(1<<i)
    assert len(SB.orig)==364
    def q6cols(g):
        out=[]
        for j in range(358,364):
            z=SB.coords(apply_cols(g,SB.orig[j]));assert z is not None;out.append(z>>358)
        return out
    G6=[cols_to_np(q6cols(g),6) for g in Mgens];O6=cols_to_np(q6cols(Mouter),6)
    assert len(matrix_group(G6))==25920 and len(matrix_group(G6+[O6]))==51840
    F=alt_form_space(G6);assert rank2(F)[0]==6 and np.array_equal((O6.T@F@O6)%2,F)
    # Unique G-invariant quadratic refinement of F.
    good=[]
    for ellm in range(64):
        ell=intvec(ellm,6);ok=True
        for g in G6:
            for xm in range(64):
                x=intvec(xm,6);gx=(g@x)%2
                if (q_from_F(F,x)^int(np.dot(ell,x)%2)) != (q_from_F(F,gx)^int(np.dot(ell,gx)%2)):
                    ok=False;break
            if not ok:break
        if ok:good.append(ell)
    assert len(good)==1
    ell=good[0]
    q=lambda m:q_from_F(F,intvec(m,6))^int(np.dot(ell,intvec(m,6))%2)
    assert all(q(vecint((O6@intvec(m,6))%2))==q(m) for m in range(64))
    singular=[m for m in range(1,64) if q(m)==0];anis=[m for m in range(1,64) if q(m)==1]
    assert (len(singular),len(anis))==(27,36)
    def polar_graph(vals):
        Z=np.zeros((len(vals),len(vals)),dtype=np.uint8)
        for i,j in itertools.combinations(range(len(vals)),2):
            if int(intvec(vals[i],6)@F@intvec(vals[j],6)%2)==0:Z[i,j]=Z[j,i]=1
        return Z
    return {'pts':pts,'pidx':pidx,'lines':lines,'G6':G6,'O6':O6,'F':F,'singular':singular,'anis':anis,
            'Asing':polar_graph(singular),'Aanis':polar_graph(anis),'cyc':cyc,'seed':seed}

def old_cubic_data():
    path=ROOT/'tools'/'compute_double_sixes.py';spec=importlib.util.spec_from_file_location('cds4525',path)
    mod=importlib.util.module_from_spec(spec);assert spec.loader is not None;spec.loader.exec_module(mod)
    roots=mod.construct_e8_roots();orbits=mod.compute_we6_orbits(roots);orb27=[o for o in orbits if len(o)==27][0]
    r=roots[orb27];gram=np.rint(r@r.T).astype(int)
    meet=(gram==0);skew=(gram==1);np.fill_diagonal(meet,False);np.fill_diagonal(skew,False)
    k6=mod.find_k_cliques(skew,6)
    # Deterministic complete pairing of the 72 half-sixes into 36 double-sixes.
    ds=[]
    for ai,A in enumerate(k6):
        SA=set(A)
        for bi in range(ai+1,len(k6)):
            B=k6[bi];SB=set(B)
            if SA&SB:continue
            if all(sum(bool(skew[a,b]) for b in B)==1 for a in A) and all(sum(bool(skew[a,b]) for a in A)==1 for b in B):
                ds.append((tuple(A),tuple(B)))
    assert len(ds)==36
    supp=[frozenset(A)|frozenset(B) for A,B in ds]
    Ads=np.zeros((36,36),dtype=np.uint8)
    for i,j in itertools.combinations(range(36),2):
        if len(supp[i]&supp[j])==4:Ads[i,j]=Ads[j,i]=1
    rootkeys=[mod.snap_to_lattice(x) for x in roots];rmap={k:i for i,k in enumerate(rootkeys)};pos={x:i for i,x in enumerate(orb27)}
    old27=[]
    for alpha in mod.E6_SIMPLE_ROOTS:
        p=[]
        for idx in orb27:p.append(pos[rmap[mod.snap_to_lattice(mod.weyl_reflect(roots[idx],alpha))]])
        old27.append(tuple(p))
    dsidx={tuple(sorted(s)):i for i,s in enumerate(supp)};old36=[]
    for p in old27:
        old36.append(tuple(dsidx[tuple(sorted(p[x] for x in s))] for s in supp))
    return meet.astype(np.uint8),Ads,old27,old36

def matperm(M,vals):
    idx={m:i for i,m in enumerate(vals)}
    return tuple(idx[vecint((M@intvec(m,6))%2)] for m in vals)

def conjugate(p,iso):
    inv=[0]*len(iso)
    for i,j in enumerate(iso):inv[j]=i
    return tuple(iso[p[inv[j]]] for j in range(len(iso)))

def main()->int:
    d=build_module();assert srg(d['Asing'])==[27,10,1,5] and srg(d['Aanis'])==[36,15,6,6]
    old27graph,old36graph,old27gens,old36gens=old_cubic_data()
    assert srg(old27graph)==[27,10,1,5] and srg(old36graph)==[36,15,6,6]
    # Frozen explicit isomorphisms new orthogonal labels -> existing repo carriers.
    iso27=[0,6,7,12,25,3,17,13,24,14,22,26,4,19,5,8,23,20,9,2,16,11,15,21,10,18,1]
    iso36=[0,21,5,14,13,31,34,6,22,20,12,8,18,4,26,30,1,32,35,24,10,25,16,2,15,28,33,19,23,7,17,9,11,29,27,3]
    assert all(d['Asing'][i,j]==old27graph[iso27[i],iso27[j]] for i in range(27) for j in range(27))
    assert all(d['Aanis'][i,j]==old36graph[iso36[i],iso36[j]] for i in range(36) for j in range(36))
    oldG27=pgroup(old27gens,27);oldG36=pgroup(old36gens,36);assert len(oldG27)==len(oldG36)==51840
    new27=[matperm(g,d['singular']) for g in d['G6']+[d['O6']]]
    new36=[matperm(g,d['anis']) for g in d['G6']+[d['O6']]]
    assert all(conjugate(g,iso27) in oldG27 for g in new27)
    assert all(conjugate(g,iso36) in oldG36 for g in new36)
    out={
      'passes':[4522,4525,4527],
      '4522_dual_module':{
        'dual_dimension':1581,'prism_span_dimension':1215,'even_dual_dimension':1580,
        'prism_intersect_even_dimension':1214,'quotient_D_mod_P_dimension':366,
        'quotient_even_mod_intersection_dimension':366,
        'fixed_line_dimension':1,'fixed_hyperplane_dimension':365,'middle_dimension':364,
        'middle_standard_basis_cyclic_dimensions':{str(k):v for k,v in sorted(d['cyc'].items())},
        'outer_invariant_submodule_dimension':358,'chosen_deterministic_seed':d['seed'],
        'orthogonal_quotient_dimension':6,'inner_image_order':25920,'outer_image_order':51840,
        'invariant_alternating_form_rank':6,'quadratic_type':'minus','singular_including_zero':28,'anisotropic':36,
        'group_reading':'PSp(4,3)=Omega^-(6,2) on the faithful 6D quotient; adjoining the projective outer involution gives O^-(6,2)',
        'boundary':'The 358D submodule and 6D quotient are exact; this pass does not claim a complete Loewy series for the 364D middle.'},
      '4525_schlafli_bridge':{
        'singular_nonzero':27,'orthogonality_graph_srg':[27,10,1,5],
        'existing_repo_carrier':'W(E6) 27 cubic-surface lines with meet adjacency',
        'explicit_isomorphism_new_to_repo':iso27,'repo_group_order':51840,
        'generator_conjugation_verified':True,'conclusion':'the 27 singular-vector action is explicitly the repo Schlaefli/cubic-line action, not a parameter-only match'},
      '4527_double_six_bridge':{
        'anisotropic_vectors':36,'orthogonality_graph_srg':[36,15,6,6],
        'existing_repo_carrier':'36 cubic-surface double-sixes; adjacency iff 12-line supports intersect in 4 lines',
        'explicit_isomorphism_new_to_repo':iso36,'repo_group_order':51840,
        'generator_conjugation_verified':True,'conclusion':'the 36 anisotropic action is explicitly the repo double-six action'},
      'boundary':'All bridges are verified by explicit graph isomorphisms and permutation-generator conjugation. No physical identification follows.'}
    OUT.parent.mkdir(exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2,sort_keys=True));return 0

if __name__=='__main__':raise SystemExit(main())
