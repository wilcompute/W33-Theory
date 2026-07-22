from __future__ import annotations
import itertools

class CycPrime:
    def __init__(self,p:int): self.p=p; self.deg=p-1
    def zero(self): return (0,)*self.deg
    def one(self): return (1,)+(0,)*(self.deg-1)
    def add(self,a,b): return tuple(x+y for x,y in zip(a,b))
    def sub(self,a,b): return tuple(x-y for x,y in zip(a,b))
    def neg(self,a): return tuple(-x for x in a)
    def smul(self,k,a): return tuple(k*x for x in a)
    def canon(self,v):
        v=list(v)+[0]*max(0,self.deg-len(v))
        for k in range(len(v)-1,self.deg-1,-1):
            c=v[k]
            if c:
                v[k]=0
                for j in range(self.deg): v[k-self.deg+j]-=c
        return tuple(v[:self.deg])
    def from_exp(self,e):
        e%=self.p
        if e<self.deg:
            v=[0]*self.deg;v[e]=1;return tuple(v)
        return (-1,)*self.deg
    def mul(self,a,b):
        v=[0]*(2*self.deg-1)
        for i,x in enumerate(a):
            if x:
                for j,y in enumerate(b):
                    if y:v[i+j]+=x*y
        return self.canon(v)
    def sigma(self,k,a):
        out=self.zero()
        for i,c in enumerate(a):
            if c:out=self.add(out,self.smul(c,self.from_exp(i*k)))
        return out

def cp(v,m):return min(v,((-v[0])%m,(-v[1])%m))
def classes(m):return sorted({cp(v,m) for v in itertools.product(range(m),repeat=2) if v!=(0,0)})
def matmul(A,B,C):
    n=len(A);r=len(B[0]);Z=C.zero();out=[[Z for _ in range(r)] for _ in range(n)]
    for i in range(n):
        for k in range(len(B)):
            a=A[i][k]
            if any(a):
                for j in range(r):
                    b=B[k][j]
                    if any(b):out[i][j]=C.add(out[i][j],C.mul(a,b))
    return out
def mat_sub(A,B,C):return [[C.sub(A[i][j],B[i][j]) for j in range(len(A))] for i in range(len(A))]
def trace(A,C):
    s=C.zero()
    for i in range(len(A)):s=C.add(s,A[i][i])
    return s
def traces(A,n,C):
    out=[];P=A
    for k in range(1,n+1):
        out.append(trace(P,C))
        if k<n:P=matmul(P,A,C)
    return out
def charpoly_from_traces(ts,C):
    e=[C.one()]
    for k in range(1,len(ts)+1):
        s=C.zero()
        for i in range(1,k+1):
            term=C.mul(e[k-i],ts[i-1])
            if (i-1)%2:term=C.neg(term)
            s=C.add(s,term)
        if any(x%k for x in s):raise ArithmeticError((k,s))
        e.append(tuple(x//k for x in s))
    return [C.one()]+[C.smul(-1 if k%2 else 1,e[k]) for k in range(1,len(e))]
def block_prime(p,offs):
    C=CycPrime(p);E=range(p);P=classes(p);sec={}
    for v,c in zip(P,offs):sec[v]=c%p;sec[((-v[0])%p,(-v[1])%p)]=(-c)%p
    B=[[C.zero() for _ in E] for _ in E]
    for (a,b),c in sec.items():
        for x in E:
            z=(c+2*x*b+a*b)%p;j=(x+a)%p
            B[j][x]=C.add(B[j][x],C.from_exp(z))
    return B
def difference_prime(p,offs):
    C=CycPrime(p);return mat_sub(block_prime(p,offs),block_prime(p,[0]*len(classes(p))),C)
def charpoly_prime(p,offs):
    C=CycPrime(p);D=difference_prime(p,offs);ts=traces(D,p,C);return charpoly_from_traces(ts,C),ts,D
