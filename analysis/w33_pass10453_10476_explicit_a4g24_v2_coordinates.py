#!/usr/bin/env python3
"""Pass10453-10476: evaluate Wilson's explicit A4 x G2(4) words in the stored Co1 module.

Source for the words:
  R. A. Wilson, "Classification of subgroups isomorphic to PSL_2(27) in the Monster",
  LMS J. Comput. Math. 17 (2014), Sec. 4.1--4.2.

Work in the repo's actual 24-dimensional integral 2.Co1 standard generators, reduced mod 2
so the central -I disappears and the action is Co1 on Lambda/2Lambda.

Wilson's words in Co1:
  c1=(ab)^4 (ab^2)^3, i1=c1^13,
  c2=a b i1 [ab,i1]^5, i2=c2^13,
  n1=(a i1)^5 (ab)^-2 i2 (ab)^2 a (ab)^-2,
  n2=(a i1)^5 (i1 i2 a)^5,
  A4=<a1=i1, a2=(n1 n2)^13>,
  G2(4)=<g1=c1^2, g2=(n1 n2)^3>.

The script tests both widespread commutator conventions and accepts only a convention for
which Wilson's stated structural relations hold.  It then tests the resulting subgroup on
canonical V2=im((I-M8)^2), extracts the order-3 A4 quotient/scalar candidate, and records an
explicit order-13 G2(4) matrix g1.

If this particular standard-generator subgroup fixes a conjugate orbit-7 generator rather
than the stored V2, no identification is forced: the script reports the obstruction and
tries the fixed-space fingerprint of the A4 involution i1 as a candidate orbit-7 generator.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10453_10476_EXPLICIT_A4G24_V2_COORDINATES.json'
P=2; N=24

def mm(A,B): return (A@B)&1
def eye(): return np.eye(N,dtype=np.uint8)
def inv2(A):
    A=np.array(A,dtype=np.uint8)&1
    X=np.concatenate([A,eye()],axis=1); r=0
    for c in range(N):
        q=next((i for i in range(r,N) if X[i,c]),None)
        if q is None: raise ValueError('singular')
        X[[r,q]]=X[[q,r]]
        for i in range(N):
            if i!=r and X[i,c]: X[i]^=X[r]
        r+=1
    return X[:,N:]
def pw(A,n):
    if n<0:return pw(inv2(A),-n)
    R=eye();B=A.copy()
    while n:
        if n&1:R=mm(R,B)
        B=mm(B,B);n//=2
    return R
def order(A,limit=10000):
    R=eye()
    for k in range(1,limit+1):
        R=mm(R,A)
        if np.array_equal(R,eye()):return k
    return None
def rank2(A):
    A=np.array(A,dtype=np.uint8)&1;m,n=A.shape;r=0
    for c in range(n):
        q=next((i for i in range(r,m) if A[i,c]),None)
        if q is None:continue
        A[[r,q]]=A[[q,r]]
        for i in range(m):
            if i!=r and A[i,c]:A[i]^=A[r]
        r+=1
        if r==m:break
    return r
def colbasis(A):
    A=np.array(A,dtype=np.uint8)&1; cols=[]; r=0
    for j in range(A.shape[1]):
        T=np.column_stack(cols+[A[:,j]]) if cols else A[:,j:j+1]
        rr=rank2(T)
        if rr>r:cols.append(A[:,j]);r=rr
    return np.column_stack(cols) if cols else np.zeros((A.shape[0],0),dtype=np.uint8)
def kernel(A):
    A=np.array(A,dtype=np.uint8)&1;m,n=A.shape
    R=A.copy(); piv=[]; r=0
    for c in range(n):
        q=next((i for i in range(r,m) if R[i,c]),None)
        if q is None:continue
        R[[r,q]]=R[[q,r]]
        for i in range(m):
            if i!=r and R[i,c]:R[i]^=R[r]
        piv.append(c);r+=1
    free=[c for c in range(n) if c not in piv]; out=[]
    for f in free:
        x=np.zeros(n,dtype=np.uint8);x[f]=1
        for i in range(r-1,-1,-1):
            pc=piv[i]
            x[pc]=sum(int(R[i,j])*int(x[j]) for j in range(pc+1,n))&1
        out.append(x)
    return np.column_stack(out) if out else np.zeros((n,0),dtype=np.uint8)
def invariant(B,A): return rank2(np.column_stack([B,mm(A,B)]))==B.shape[1]
def same_space(A,B): return A.shape[1]==B.shape[1] and rank2(np.column_stack([A,B]))==A.shape[1]
def comm(x,y,conv):
    if conv=='x^-1y^-1xy':return mm(mm(mm(inv2(x),inv2(y)),x),y)
    if conv=='xyx^-1y^-1':return mm(mm(mm(x,y),inv2(x)),inv2(y))
    raise ValueError(conv)
def commute(x,y):return np.array_equal(mm(x,y),mm(y,x))

def load_pair():
    X=np.loadtxt(ROOT/'analysis/_co0_G.txt',dtype=np.int64)
    assert X.shape==(48,24)
    return X[:24].astype(np.uint8)&1,X[24:].astype(np.uint8)&1

def build(a,b,conv):
    ab=mm(a,b); ab2=mm(a,pw(b,2))
    c1=mm(pw(ab,4),pw(ab2,3)); i1=pw(c1,13)
    c2=mm(mm(mm(a,b),i1),pw(comm(ab,i1,conv),5)); i2=pw(c2,13)
    n1=mm(mm(mm(mm(mm(pw(mm(a,i1),5),pw(ab,-2)),i2),pw(ab,2)),a),pw(ab,-2))
    n2=mm(pw(mm(a,i1),5),pw(mm(mm(i1,i2),a),5))
    n12=mm(n1,n2)
    a1=i1; a2=pw(n12,13); g1=pw(c1,2); g2=pw(n12,3)
    checks={
      'c1_order':order(c1),'i1_order':order(i1),'c2_order':order(c2),'i2_order':order(i2),
      'c2_centralizes_i1':commute(c2,i1),'i1_i2_commute':commute(i1,i2),
      'a1_order':order(a1),'a2_order':order(a2),'a1a2_order':order(mm(a1,a2)),
      'g1_order':order(g1),'g2_order':order(g2),'g1g2_order':order(mm(g1,g2)),
      'A4_G2_commute':all(commute(x,y) for x in (a1,a2) for y in (g1,g2)),
    }
    return checks,{'c1':c1,'i1':i1,'c2':c2,'i2':i2,'n1':n1,'n2':n2,'a1':a1,'a2':a2,'g1':g1,'g2':g2}

def main():
    a,b=load_pair(); I=eye()
    # Repo standard-generator fingerprints in the mod-2 Co1 action.
    std={'a':order(a),'b':order(b),'ab':order(mm(a,b)),'ababb':order(mm(mm(mm(mm(a,b),a),b),b))}
    assert std=={'a':2,'b':3,'ab':40,'ababb':6},std

    candidates=[]
    for conv in ('x^-1y^-1xy','xyx^-1y^-1'):
        checks,els=build(a,b,conv)
        # Structural filter from Wilson Sec 4.1: c1 order26; i1,i2 involutions; c2 centralizes i1;
        # A4 and G2 factors commute; g1 order13.  a2/g2 orders are additionally recorded.
        good=(checks['c1_order']==26 and checks['i1_order']==2 and checks['i2_order']==2 and
              checks['c2_centralizes_i1'] and checks['i1_i2_commute'] and checks['g1_order']==13 and
              checks['A4_G2_commute'])
        candidates.append((conv,good,checks,els))
    good=[x for x in candidates if x[1]]
    assert len(good)==1,[(c,g,ch) for c,g,ch,_ in candidates]
    conv,_,checks,E=good[0]

    M=np.loadtxt(ROOT/'analysis/_co0_M8.txt',dtype=np.int64)
    assert M.shape==(24,24)
    Nmat=(I-(M.astype(np.uint8)&1))&1
    V2=colbasis(mm(Nmat,Nmat));assert V2.shape==(24,12)

    invs={k:invariant(V2,E[k]) for k in ('a1','a2','g1','g2')}
    fixes_stored=all(invs.values())

    # a2 is Wilson's non-2 A4 generator if its order is 3; this is the scalar candidate on
    # whichever orbit-7 generator this representative stabilizes.
    scalar=E['a2'] if checks['a2_order']==3 else mm(E['a1'],E['a2'])
    scalar_order=order(scalar)

    # A4 involution fixed-space fingerprint: orbit-7's V4 kernel acts trivially on its 12-space.
    F=kernel((E['a1']-I)&1)
    fixed_dim=F.shape[1]
    candidate12 = F if fixed_dim==12 else None
    candidate_invs=None
    if candidate12 is not None:
        candidate_invs={k:invariant(candidate12,E[k]) for k in ('a1','a2','g1','g2')}

    # If the subgroup fixes stored V2, calculate the induced 12x12 matrices by coordinates.
    # Otherwise record only ambient matrices and the exact missing conjugacy step.
    def solve_coords(B,Y):
        # B 24x12 full rank; solve B X = Y columnwise by elimination on augmented systems.
        X=np.zeros((12,Y.shape[1]),dtype=np.uint8)
        for j in range(Y.shape[1]):
            A=np.concatenate([B.copy(),Y[:,j:j+1]],axis=1);m,n0=24,12;r=0;piv=[]
            for c in range(n0):
                q=next((i for i in range(r,m) if A[i,c]),None)
                if q is None:continue
                A[[r,q]]=A[[q,r]]
                for i in range(m):
                    if i!=r and A[i,c]:A[i]^=A[r]
                piv.append(c);r+=1
            assert r==12
            x=np.zeros(12,dtype=np.uint8)
            for i,c in enumerate(piv):x[c]=A[i,-1]
            assert np.array_equal(mm(B,x[:,None]),Y[:,j:j+1])
            X[:,j]=x
        return X
    induced={}
    if fixes_stored:
        for k in ('a1','a2','g1','g2'):
            induced[k]=solve_coords(V2,mm(E[k],V2)).tolist()
        induced_scalar=solve_coords(V2,mm(scalar,V2))
        induced_g1=solve_coords(V2,mm(E['g1'],V2))
        assert order(induced_scalar)==3 and order(induced_g1)==13
    else:
        induced_scalar=None;induced_g1=None

    out={
      'schema':'w33.pass10453_10476.explicit_a4g24_v2_coordinates.v1','status':'PASS','passes':'10453-10476',
      'source':{'paper':'R. A. Wilson, LMS J. Comput. Math. 17 (2014), Sec. 4.1-4.2','construction':'explicit A4 x G2(4) words in Co1 standard generators'},
      'co1_standard_checks':std,
      'commutator_convention_selected':conv,
      'alternative_conventions':{c:{'accepted':bool(g),'checks':ch} for c,g,ch,_ in candidates},
      'wilson_subgroup_checks':checks,
      'stored_canonical_V2':{'dimension':12,'generator_invariance':invs,'this_representative_fixes_stored_V2':bool(fixes_stored)},
      'scalar_candidate':{'ambient_order':scalar_order,'chosen_as':'a2' if checks['a2_order']==3 else 'a1*a2'},
      'order13_candidate':{'ambient_matrix':'g1=c1^2','order':checks['g1_order']},
      'a1_fixed_space':{'dimension':fixed_dim,'is_12dim_candidate':candidate12 is not None,'candidate_invariance':candidate_invs},
      'induced_on_stored_V2':induced if fixes_stored else None,
      'theorem':('Wilson\'s published A4 x G2(4) standard-generator construction has been evaluated in the repository\'s actual mod-2 24-dimensional Co1 representation with the commutator convention selected by the paper\'s own structural identities. The script then decides, without conjugacy assumptions, whether this concrete representative is the stabilizer of the stored canonical V2; when it is, it exports explicit 12x12 scalar and order-13 actions.'),
      'boundary':('The subgroup word evaluation is exact. If this standard-generator representative does not fix stored V2, orbit-7 uniqueness proves it is conjugate to the desired stabilizer but this script does not invent the missing Co1 conjugator.')
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print('RESULT_JSON='+json.dumps(out,sort_keys=True))
    return 0
if __name__=='__main__':raise SystemExit(main())
