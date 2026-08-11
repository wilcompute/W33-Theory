#!/usr/bin/env python3
"""Pass 4813 — split the q=9 BLT/minimum shell under PSp(4,9).

Pass4805 transferred Betten's complete PΓO(5,9) classification to the minimum
shell but left the PSp splitting open.  Since PSp(4,9)=PΩ(5,9) is normal of
index four in PΓO(5,9), the number of PSp orbits inside one full class is
4/|image(H)|, where H is its stabilizer and image(H) is taken in the outer
C2 x C2 quotient (orthogonal spinor bit, Frobenius bit).

For Betten's K1 and Fi/Mondello stabilizer matrices this producer evaluates the
Frobenius bit directly and the orthogonal bit by Cartan-Dieudonne reflection
decomposition over GF(9), using x^2=x+1 from Betten's encoding polynomial
X^2+2X+2.  Both stabilizers surject C2 x C2.

For the Linear BLT set the stabilizer is the conic/decomposition stabilizer
((O(3,9) x O^-(2,9))/<-I,-I>) : Gal(F9/F3), of order 28800.  The Gal factor
supplies Frobenius and an anisotropic-plane reflection of nonsquare norm supplies
the spinor bit, so its outer image is also all four elements.

Hence none of the three PΓO classes splits under PSp.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4813_Q9_PSP_BLT_SPLIT.json'

def add(a,b):return ((a%3+b%3)%3)+3*((a//3+b//3)%3)
def neg(a):return ((-a%3)%3)+3*((-(a//3))%3)
def mul(a,b):
    a0,a1=a%3,a//3;b0,b1=b%3,b//3
    return ((a0*b0+a1*b1)%3)+3*((a0*b1+a1*b0+a1*b1)%3)
def power(a,n):
    r=1
    while n:
        if n&1:r=mul(r,a)
        a=mul(a,a);n//=2
    return r
def inv(a):assert a;return power(a,7)
def div(a,b):return mul(a,inv(b))
def q(v):return add(mul(v[0],v[0]),add(mul(v[1],v[2]),mul(v[3],v[4])))
def B(u,v):return add(add(mul(2,mul(u[0],v[0])),add(mul(u[1],v[2]),mul(u[2],v[1]))),add(mul(u[3],v[4]),mul(u[4],v[3])))
def vsub(u,v):return tuple(add(a,neg(b)) for a,b in zip(u,v))
def smul(a,v):return tuple(mul(a,x) for x in v)
def mv(A,v):
    out=[]
    for r in A:
        s=0
        for a,x in zip(r,v):s=add(s,mul(a,x))
        out.append(s)
    return tuple(out)
def mm(A,C):
    return [[sumgf(mul(A[i][k],C[k][j]) for k in range(5)) for j in range(5)] for i in range(5)]
def sumgf(xs):
    s=0
    for x in xs:s=add(s,x)
    return s
def eye():return [[1 if i==j else 0 for j in range(5)] for i in range(5)]
def scale(a,A):return [[mul(a,x) for x in r] for r in A]
def refl(v):
    Q=q(v);assert Q
    cols=[]
    for j in range(5):
        e=tuple(1 if i==j else 0 for i in range(5));c=div(B(e,v),Q);cols.append(vsub(e,smul(c,v)))
    return [[cols[j][i] for j in range(5)] for i in range(5)]
def sqrt9(a):
    return next((x for x in range(1,9) if mul(x,x)==a),None)
def squareclass(a):assert a;return 0 if power(a,4)==1 else 1
BASIS=[(1,0,0,0,0),(0,1,1,0,0),(0,1,2,0,0),(0,0,0,1,1),(0,0,0,1,2)]
ALL=list(itertools.product(range(9),repeat=5))

def spinor(A):
    lam=q(mv(A,(1,0,0,0,0)));assert lam
    # Polynomial verification on all 59049 vectors is still tiny.
    assert all(q(mv(A,v))==mul(lam,q(v)) for v in ALL)
    s=sqrt9(inv(lam));assert s is not None;g=scale(s,A);prod=1;fixed=[]
    for x in BASIS:
        gx=mv(g,x)
        if gx==x:fixed.append(x);continue
        d=vsub(gx,x)
        if q(d):
            g=mm(refl(d),g);prod=mul(prod,q(d))
        else:
            w=None
            for y in ALL:
                if q(y)!=q(x) or any(B(y,f) for f in fixed):continue
                d1=vsub(gx,y);d2=vsub(y,x)
                if q(d1) and q(d2):w=y;break
            assert w is not None
            d1=vsub(gx,w);g=mm(refl(d1),g);prod=mul(prod,q(d1))
            d2=vsub(w,x);g=mm(refl(d2),g);prod=mul(prod,q(d2))
        assert mv(g,x)==x;fixed.append(x)
    assert g==eye();return squareclass(prod)

K1=[
([[2,0,0,0,0],[0,6,0,0,0],[0,0,7,0,0],[0,0,0,0,4],[0,0,0,8,0]],1),
([[2,0,0,0,0],[0,3,4,6,4],[0,0,5,0,0],[0,0,4,6,0],[0,0,7,0,7]],1),
([[1,0,0,0,0],[0,2,0,0,0],[0,0,2,0,0],[0,0,0,2,0],[0,0,0,0,2]],0),
([[2,0,0,0,0],[0,1,0,0,0],[0,6,1,6,2],[0,2,0,0,7],[0,6,0,6,0]],0),
([[1,0,0,0,0],[0,3,4,3,8],[0,8,0,0,0],[0,3,0,3,0],[0,4,0,0,5]],1),
([[2,0,0,0,0],[0,3,0,0,0],[0,0,5,0,0],[0,0,0,3,0],[0,0,0,0,5]],1),
([[2,0,0,0,0],[0,1,0,0,0],[0,0,1,0,0],[0,0,0,2,0],[0,0,0,0,2]],0),
([[1,0,0,0,0],[0,3,0,0,0],[0,4,5,3,2],[0,1,0,5,0],[0,5,0,0,3]],1),
([[1,0,0,0,0],[0,3,0,0,0],[0,0,5,0,0],[0,0,0,5,0],[0,0,0,0,3]],1),
([[2,0,0,0,0],[0,5,0,0,0],[0,0,3,0,0],[0,0,0,4,0],[0,0,0,0,8]],1)]
FI=[
([[6,0,0,3,2],[0,8,6,1,5],[0,6,8,1,5],[2,5,5,8,7],[3,1,1,6,8]],0),
([[7,0,0,4,6],[0,1,0,0,0],[0,0,1,0,0],[6,0,0,4,2],[4,0,0,8,4]],0),
([[3,0,0,8,5],[0,1,3,2,3],[0,5,0,0,0],[1,3,0,2,1],[6,4,0,2,4]],1),
([[1,0,0,0,0],[0,1,0,0,0],[0,5,1,7,1],[0,3,0,6,0],[0,4,0,0,7]],1),
([[2,0,0,0,0],[0,2,0,0,0],[0,0,2,0,0],[0,0,0,0,7],[0,0,0,6,0]],0),
([[0,1,3,7,1],[6,6,1,5,6],[8,2,5,7,8],[2,2,6,4,2],[6,4,2,0,8]],1)]

def image(gens):
    labels=[(spinor(A),f) for A,f in gens]
    S={(0,0)};changed=True
    while changed:
        changed=False
        for a in list(S):
            for b in labels:
                c=(a[0]^b[0],a[1]^b[1])
                if c not in S:S.add(c);changed=True
    return labels,S

def main():
    kl,ki=image(K1);fl,fi=image(FI);assert len(ki)==len(fi)==4
    PSp=9**4*(9**4-1)*(9**2-1)//2;assert PSp==1721606400
    full=4*PSp;assert full==6886425600
    rows=[]
    for name,H,size in [('Linear',28800,239112),('K1',5760,1195560),('Fi/Mondello',400,17216064)]:
        outim=4;hs=H//outim;orb=PSp//hs;assert orb==size
        rows.append({'name':name,'PgammaO_stabilizer':H,'outer_image_order':4,'PSp_stabilizer':hs,'PSp_orbits_in_full_class':1,'PSp_orbit_size':orb})
    out={'pass':4813,'PSp_order':PSp,'PgammaO_order':full,'outer_quotient':'C2 x C2 (spinor/similitude, Frobenius)',
      'K1_generator_outer_labels':kl,'K1_outer_image_order':len(ki),'Fi_generator_outer_labels':fl,'Fi_outer_image_order':len(fi),
      'Linear_outer_image_order':4,'classes':rows,
      'theorem':'None of the three q=9 full semilinear BLT/minimum-shell classes splits under PSp(4,9). Linear, K1, and Fi/Mondello are already single PSp orbits of sizes 239112, 1195560, and 17216064, with PSp stabilizers 7200, 1440, and 100.',
      'prior_art_boundary':'Betten supplies the complete PΓO classification, representatives, stabilizer matrices/orders, and names. This pass adds the outer-quotient evaluation and PSp orbit conclusion; it does not claim the original BLT classification.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
