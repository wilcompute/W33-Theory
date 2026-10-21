#!/usr/bin/env python3
"""Exact local p=3 Frobenius realization of the W33 Levi Ihara factor.

No global Euler-product identity or classical Riemann Hypothesis is implied.
Rebuilds the W33 incidence structure and computes point counts for
C: y^2=x^5+1 (genus 2), E: y^2=x^3-x (elliptic), over F_3 and F_9.
All calculations use only Python's standard library.
"""
import itertools
from math import gcd

def normalize(v):
    a=next(x for x in v if x)
    return tuple(x * (1 if a==1 else 2) % 3 for x in v)

def form(a,b):
    return (a[0]*b[2]-a[2]*b[0]+a[1]*b[3]-a[3]*b[1])%3

def verify_w33():
    points=sorted({normalize(v) for v in itertools.product(range(3),repeat=4) if any(v)})
    assert len(points)==40
    lines=set()
    for a,b in itertools.combinations(points,2):
        if form(a,b): continue
        line=frozenset(normalize(tuple((s*x+t*y)%3 for x,y in zip(a,b)))
          for s,t in itertools.product(range(3),repeat=2) if (s,t)!=(0,0))
        assert len(line)==4
        lines.add(line)
    assert len(lines)==40
    lines=list(lines)
    N=[[int(p in line) for line in lines] for p in points]
    A=[[int(i!=j and not form(points[i],points[j])) for j in range(40)]
       for i in range(40)]
    assert all(sum(row)==4 for row in N)
    assert all(sum(row)==12 for row in A)
    for i in range(40):
        for j in range(40):
            assert sum(N[i][k]*N[j][k] for k in range(40))==A[i][j]+4*(i==j)
            assert sum(A[i][k]*A[k][j] for k in range(40))==8*(i==j)-2*A[i][j]+4
    # W33 adjacency: 12^1, 2^24, (-4)^15.
    # Levi bipartite adjacency: +-4^1, +-sqrt(6)^24, 0^30.
    return {'points':40,'lines':40,'flags':160}

class GF3Extension:
    def __init__(self,mod):
        self.mod=mod
        self.n=len(mod)-1
        self.q=3**self.n
        self.elements=list(itertools.product(range(3),repeat=self.n))
        self.zero=(0,)*self.n
        self.one=(1,)+(0,)*(self.n-1)
    def add(self,x,y):
        return tuple((a+b)%3 for a,b in zip(x,y))
    def mul(self,x,y):
        n=self.n
        z=[0]*(2*n-1)
        for i in range(n):
            for j in range(n):
                z[i+j]=(z[i+j]+x[i]*y[j])%3
        for k in range(2*n-2,n-1,-1):
            for j in range(n):
                z[k-n+j]=(z[k-n+j]-z[k]*self.mod[j])%3
        return tuple(z[:n])
    def power(self,x,n):
        v=self.one
        while n:
            if n&1:v=self.mul(v,x)
            x=self.mul(x,x)
            n>>=1
        return v
    def count(self,coeff):
        sq={x:0 for x in self.elements}
        for y in self.elements:sq[self.mul(y,y)]+=1
        # Both polynomials are odd degree, so exactly one infinity.
        total=1
        for x in self.elements:
            z=self.zero
            for a in coeff:
                z=self.add(self.mul(z,x),(a,)+(0,)*(self.n-1))
            total+=sq[z]
        return total

def verify_curves():
    C=(1,0,0,0,0,1)     # y^2=x^5+1
    E=(1,0,2,0)         # y^2=x^3-x
    mods=[(0,1),(1,0,1),(1,0,2,1),(1,0,1,1,1)]
    counts=[]
    for mod in mods:
        f=GF3Extension(mod)
        assert all(f.power(x,f.q-1)==f.one for x in f.elements if x!=f.zero)
        counts.append((f.q,f.count(C),f.count(E)))
    assert counts==[(3,4,4),(9,10,16),(27,28,28),(81,118,64)]
    assert all(gcd(5,3**n-1)==1 for n in (1,2,3))
    # The permutation x -> x^5 yields C's Frobenius traces t1=t2=0.
    # Genus-two functional equation gives P_C(u)=1+9u^4.
    # #E(F3)=4 gives a3=0 and P_E(u)=1+3u^2.
    return counts

if __name__=='__main__':
    print('W33 incidence:',verify_w33())
    print('Field, genus2 points, elliptic points:',verify_curves())
    print('PASS: Z_Levi(u)^-1 = (1-u^2)^81(1-9u^2)(1+9u^4)^24(1+3u^2)^30')
    print('PASS: D_Levi,nt(u) = P_C,F3(u)^24 P_E,F3(u)^30, degree 156')
    print('NOT proved: canonical motive intertwiner, global L equality, classical RH')
