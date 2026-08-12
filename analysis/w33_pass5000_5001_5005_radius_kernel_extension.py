#!/usr/bin/env python3
"""Pass5000/5001/5005: octahedral-local radius ILP witness, the exact
tritangent V20 identification inside the 30->10 binary quotient, and the
nonsplitting of that extension.
"""
from __future__ import annotations
import itertools,json,sys
from fractions import Fraction
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from analysis.w33_pass4992_4999_common import build_base,build_group,gf2_rank_int

O0=ROOT/'data/PART_W33_PASS5000_OCTAHEDRAL_RADIUS_ILP_BARRIER.json'
O1=ROOT/'data/PART_W33_PASS5001_KERNEL20_TRITANGENT_V20_INTERTWINER.json'
O5=ROOT/'data/PART_W33_PASS5005_NONSPLIT_20_30_10_EXTENSION.json'

def det(A):
    n=len(A);s=Fraction(0)
    for p in itertools.permutations(range(n)):
        inv=sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))
        z=Fraction(-1 if inv&1 else 1)
        for i in range(n):z*=A[i][p[i]]
        s+=z
    return s

def piv_basis(rows):
    piv={}
    for x0 in rows:
        x=int(x0)
        while x:
            p=x.bit_length()-1
            if p in piv:x^=piv[p]
            else:piv[p]=x;break
    return piv

def reduce_mask(x,piv):
    x=int(x)
    for p in sorted(piv,reverse=True):
        if x>>p&1:x^=piv[p]
    return x

def coord_basis(vectors):
    piv={};basis=[]
    for v in vectors:
        x=int(v)
        for p in sorted(piv,reverse=True):
            if x>>p&1:x^=piv[p][0]
        if x:
            i=len(basis);p=x.bit_length()-1
            piv[p]=(x,1<<i);basis.append(x)
    def express(x):
        x=int(x);c=0
        for p in sorted(piv,reverse=True):
            if x>>p&1:
                x^=piv[p][0];c^=piv[p][1]
        return x,c
    return basis,piv,express

def vbits(mask,n):return np.array([(int(mask)>>i)&1 for i in range(n)],dtype=np.uint8)
def maskbits(v):return sum(int(x&1)<<i for i,x in enumerate(v))

def nullspace(A):
    R=np.array(A,dtype=np.uint8)%2;m,n=R.shape;r=0;piv=[]
    for c in range(n):
        k=next((i for i in range(r,m) if R[i,c]),None)
        if k is None:continue
        if k!=r:R[[r,k]]=R[[k,r]]
        for i in range(m):
            if i!=r and R[i,c]:R[i]^=R[r]
        piv.append(c);r+=1
        if r==m:break
    free=[c for c in range(n) if c not in piv];out=[]
    for f in free:
        x=np.zeros(n,dtype=np.uint8);x[f]=1
        for rr,c in enumerate(piv):
            if R[rr,f]:x[c]=1
        out.append(x)
    return np.array(out,dtype=np.uint8)

def affine_feasible(A,b):
    A=np.array(A,dtype=np.uint8)%2;b=np.array(b,dtype=np.uint8)%2
    R=np.column_stack([A,b]);m,n=A.shape;r=0
    for c in range(n):
        k=next((i for i in range(r,m) if R[i,c]),None)
        if k is None:continue
        if k!=r:R[[r,k]]=R[[k,r]]
        for i in range(m):
            if i!=r and R[i,c]:R[i]^=R[r]
        r+=1
    return not any(not R[i,:n].any() and R[i,n] for i in range(m))

def main()->int:
    # --------------------------------------------------------------- Pass5000
    # Exact integral witness for the strongest *octahedron-local* shell/moment
    # relaxation used here. Every one of 270 cells is assigned four negative
    # A3 faces and equator signs (-,-,+), so local products agree exactly.
    cells=270;T3=-1080;U4=-270;U6=1620;U8=-270;U9=-1080;U12=270
    # Reuse the exact degree-7 radial witness from Pass4960. The complementary
    # A4/A6 shell sums needed to attach the octahedral cells are integral,
    # parity-compatible, and lie strictly inside their shell bounds.
    T4,T5,T6,T7=-1936,75316,830590,-37193040
    A3,A4,A5,A6,A7=1080,10530,127656,2329680,37193040
    V4=T4-U4;V6=T6-U6
    assert abs(V4)<=A4-810 and (V4-(A4-810))%2==0
    assert abs(V6)<=A6-1620 and (V6-(A6-1620))%2==0
    assert abs(T5)<=A5 and (T5-A5)%2==0 and T7==-A7
    m=[Fraction(1),Fraction(0),Fraction(90)]
    m += [-Fraction(3,4)*T3,
          Fraction(24255)+Fraction(3,2)*T4,
          -Fraction(2685,4)*T3-Fraction(15,4)*T5,
          Fraction(10874340)+2010*T4+Fraction(45,4)*T6,
          -Fraction(5037081,8)*T3-Fraction(56175,8)*T5-Fraction(315,8)*T7]
    M=[[m[i+j] for j in range(4)] for i in range(4)]
    L=[[m[i+j+1]+7*m[i+j] for j in range(4)] for i in range(4)]
    mp=[det([row[:k] for row in M[:k]]) for k in range(1,5)]
    lp=[det([row[:k] for row in L[:k]]) for k in range(1,5)]
    assert all(x>0 for x in mp+lp)
    # This local ILP witness is nevertheless not a global character: T3=-A3
    # means every generating odd triangle has character -1; since the 1080
    # triangles span K^perp, parity forces chi(h)=(-1)^wt(h), hence T4=+A4.
    assert T4!=A4
    out0={
      'pass':5000,'status':'FEASIBLE_LOCAL_RELAXATION_GLOBAL_CLOSURE_REQUIRED',
      'octahedral_local_ILP_witness':{'cells':270,'per_cell_A3_signs':'(-1,-1,-1,-1)',
        'per_cell_equator_signs':'(-1,-1,+1)','T3':T3,'U4_residual':U4,'U6_restricted':U6,
        'U8_restricted':U8,'U9_restricted':U9,'U12_restricted':U12},
      'degree7_shell_witness':{'T3':T3,'T4':T4,'T5':T5,'T6':T6,'T7':T7,
        'A4_complement_sum':V4,'A6_complement_sum':V6,
        'moments':[str(x) for x in m],
        'moment_leading_minors':[str(x) for x in mp],
        'localized_X_plus_7_leading_minors':[str(x) for x in lp]},
      'global_character_cut':{'premise':'T3=-A3=-1080 and the 1080 A3 checks span K^perp',
        'consequence':'chi(h)=(-1)^wt(h) on all of K^perp, hence T4=+A4=10530',
        'local_witness_violates_global_cut':True},
      'covering_radius':{'proved_interval':[134,173],'improved_here':False},
      'theorem':'The exact 270-cell octahedral sign ILP plus independent complementary shell bounds and all degree-7 radial moment/localizing tests is feasible at the distance-173 frontier. An explicit integral witness exists. It is killed only when global character closure across the triangle-generated dual code is imposed. Therefore the octahedral cells and radial moments alone cannot lower 173; the next radius model must encode cross-octahedron character closure rather than independent shell complements.',
      'boundary':'This is an exact feasibility/obstruction result for the stated local-cell/truncated-moment ILP, not an actual distance-173 coset and not a proof that the full character-constrained ILP is feasible.'}
    O0.write_text(json.dumps(out0,indent=2,sort_keys=True)+'\n')

    # --------------------------------------------------------------- Pass5001
    b=build_base();g=build_group(b);E=b['E'];ei=b['ei'];spreads=b['spreads'];iso=b['iso_ds_sp']
    tri=b['tri_masks'];sq=[m for m,V in b['residual']];Msel=b['M']
    edge_line=[]
    for a,c in E:
        z=spreads[iso[a]]&spreads[iso[c]];assert len(z)==1;edge_line.append(next(iter(z)))
    def project(mask):
        y=0;x=int(mask)
        while x:
            lb=x&-x;k=lb.bit_length()-1;y^=1<<edge_line[k];x^=lb
        return y
    sqp=piv_basis(sq);simg=piv_basis(project(x) for x in sq)
    residues=[reduce_mask(x,sqp) for x in tri]
    qb,qp,qexpr=coord_basis(residues);assert len(qb)==30
    target_res=[reduce_mask(project(x),simg) for x in qb]
    tb,tp,texpr=coord_basis(target_res);assert len(tb)==10
    P=np.zeros((10,30),dtype=np.uint8)
    for j,x in enumerate(target_res):
        rem,c=texpr(x);assert rem==0;P[:,j]=vbits(c,10)
    K=nullspace(P);assert K.shape==(20,30)
    kmasks=[maskbits(row) for row in K];kb,kp,kexpr=coord_basis(kmasks);assert len(kb)==20
    ub,up,uexpr=coord_basis(maskbits(row) for row in (Msel%2));assert len(ub)==20
    def edgeperm(mask,p36):
        y=0;x=int(mask)
        while x:
            lb=x&-x;k=lb.bit_length()-1;u,v=E[k];kk=ei[tuple(sorted((p36[u],p36[v])))];y|=1<<kk;x^=lb
        return y
    def vertperm(mask,p36):
        y=0;x=int(mask)
        while x:
            lb=x&-x;i=lb.bit_length()-1;y|=1<<p36[i];x^=lb
        return y
    def action30(p36):
        A=np.zeros((30,30),dtype=np.uint8)
        for j,x in enumerate(qb):
            r=reduce_mask(edgeperm(x,p36),sqp);rem,c=qexpr(r);assert rem==0;A[:,j]=vbits(c,30)
        return A
    def actionK(A):
        Z=np.zeros((20,20),dtype=np.uint8)
        for j,x in enumerate(kb):
            w=(A@vbits(x,30))%2;rem,c=kexpr(maskbits(w));assert rem==0;Z[:,j]=vbits(c,20)
        return Z
    def actionU(p36):
        Z=np.zeros((20,20),dtype=np.uint8)
        for j,x in enumerate(ub):
            rem,c=uexpr(vertperm(x,p36));assert rem==0;Z[:,j]=vbits(c,20)
        return Z
    A30=[action30(p) for p in g['DPp']];KA=[actionK(A) for A in A30];UA=[actionU(p) for p in g['DPp']]
    eq=[]
    for Ak,Au in zip(KA,UA):
        for a in range(20):
            for cc in range(20):
                row=np.zeros(400,dtype=np.uint8)
                for j in range(20):
                    if Ak[a,j]:row[j*20+cc]^=1
                    if Au[j,cc]:row[a*20+j]^=1
                if row.any():eq.append(row)
    H=nullspace(np.array(eq,dtype=np.uint8));assert H.shape[0]==1
    X=H[0].reshape(20,20);assert gf2_rank_int(maskbits(row) for row in X)==20
    outer=g['DPf'][-1];Ao=action30(outer);Ko=actionK(Ao);Uo=actionU(outer)
    assert np.array_equal((Ko@X)%2,(X@Uo)%2)
    out1={
      'pass':5001,'source_quotient':'triangle span / residual-square span over F2','source_dimension':30,
      'target_quotient_dimension':10,'kernel_dimension':20,
      'tritangent_selector_code':{'matrix':'45x36 M mod2','rank':20},
      'intertwiner':{'group_generators_tested_PSp':len(g['DPp']),'Hom_dimension':1,
        'unique_nonzero_intertwiner_rank':20,'outer_PGSp_generator_also_intertwined':True,
        'full_group_equivariant_isomorphism':True},
      'exact_sequence':'0 -> V20_trit -> Q30 -> Q10 -> 0 over F2',
      'theorem':'The 20-dimensional kernel discovered in Pass4997 is exactly the binary tritangent selector V20, not a numerical coincidence. The PSp intertwiner space is one-dimensional and its unique nonzero map is invertible; the same map commutes with the outer PGSp generator, giving a full W(E6)/PGSp-equivariant identification.',
      'boundary':'This is a binary-module theorem. It does not identify the carrier with an unrelated real 20-dimensional representation without reduction data.'}
    O1.write_text(json.dumps(out1,indent=2,sort_keys=True)+'\n')

    # --------------------------------------------------------------- Pass5005
    # Target action and affine section equations. If an equivariant section S
    # existed, P S=I and A30(g)S=S Atarget(g) for every PSp generator.
    def p40(mask,p):
        y=0;x=int(mask)
        while x:
            lb=x&-x;i=lb.bit_length()-1;y|=1<<p[i];x^=lb
        return y
    TA=[]
    for p in g['LpP']:
        Z=np.zeros((10,10),dtype=np.uint8)
        for j,x in enumerate(tb):
            r=reduce_mask(p40(x,p),simg);rem,c=texpr(r);assert rem==0;Z[:,j]=vbits(c,10)
        TA.append(Z)
    assert all(np.array_equal((T@P)%2,(P@A)%2) for T,A in zip(TA,A30))
    rows=[];rhs=[]
    for A,T in zip(A30,TA):
        for a in range(30):
            for cc in range(10):
                row=np.zeros(300,dtype=np.uint8)
                for j in range(30):
                    if A[a,j]:row[j*10+cc]^=1
                for j in range(10):
                    if T[j,cc]:row[a*10+j]^=1
                if row.any():rows.append(row);rhs.append(0)
    for a in range(10):
        for cc in range(10):
            row=np.zeros(300,dtype=np.uint8)
            for j in range(30):
                if P[a,j]:row[j*10+cc]^=1
            rows.append(row);rhs.append(int(a==cc))
    feasible=affine_feasible(np.array(rows,dtype=np.uint8),np.array(rhs,dtype=np.uint8));assert not feasible
    out5={
      'pass':5005,'sequence':'0 -> V20_trit -> Q30 -> Q10 -> 0 over F2',
      'PSp_equivariant_section_exists':False,'section_system_variables':300,'section_system_equations':len(rows),
      'full_PGSp_section_exists':False,
      'theorem':'The canonical 20->30->10 binary sequence does not split PSp-equivariantly. Solving the complete affine section equations P S=I and gS=Sg for the PSp generators gives no solution. Therefore Q30 is a genuine nonsplit extension of Q10 by the tritangent V20; a fortiori there is no full-PGSp equivariant splitting.',
      'boundary':'Nonsplit refers to this exact finite-field module extension; it is not a claim about a real or complex extension class.'}
    O5.write_text(json.dumps(out5,indent=2,sort_keys=True)+'\n')
    return 0
if __name__=='__main__':raise SystemExit(main())
