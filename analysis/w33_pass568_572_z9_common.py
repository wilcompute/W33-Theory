from __future__ import annotations
import itertools

class Cyc9:
    p=3;m=9;deg=6
    def zero(self):return (0,)*6
    def one(self):return (1,0,0,0,0,0)
    def canon(self,v):
        v=list(v)+[0]*max(0,6-len(v))
        for k in range(len(v)-1,5,-1):
            c=v[k]
            if c:
                v[k]=0;v[k-6]-=c;v[k-3]-=c
        return tuple(v[:6])
    def from_exp(self,e):
        v=[0]*9;v[e%9]=1;return self.canon(v)
    def add(self,a,b):return tuple(x+y for x,y in zip(a,b))
    def sub(self,a,b):return tuple(x-y for x,y in zip(a,b))
    def neg(self,a):return tuple(-x for x in a)
    def smul(self,k,a):return tuple(k*x for x in a)
    def mul(self,a,b):
        v=[0]*11
        for i,x in enumerate(a):
            if x:
                for j,y in enumerate(b):
                    if y:v[i+j]+=x*y
        return self.canon(v)

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

C=Cyc9();A9,A3=classes(9),classes(3);BIDX={b:i for i,b in enumerate(A3)}
ALPHAS=((1,0),(0,1),(1,1),(1,2))

def oriented(v):
    r=(v[0]%3,v[1]%3);q=cp(r,3)
    return v if r==q else ((-v[0])%9,(-v[1])%9)
def reduction_meta(v):
    if v[0]%3 or v[1]%3:
        w=oriented(v);b=(w[0]%3,w[1]%3);u=((w[0]-b[0])//3%3,(w[1]-b[1])//3%3);return b,u,True
    w=(v[0]//3%3,v[1]//3%3);return cp(w,3),(0,0),False
META=[reduction_meta(v) for v in A9]

def pair_deltas():
    out=[];E=range(9)
    for a,b in A9:
        vals=[]
        for c in (0,3,6):
            M=[[C.zero() for _ in E] for _ in E]
            for aa,bb,cc in ((a,b,c),((-a)%9,(-b)%9,(-c)%9)):
                for x in E:
                    z=(cc+2*x*bb+aa*bb)%9;j=(x+aa)%9
                    M[j][x]=C.add(M[j][x],C.from_exp(z))
            vals.append(M)
        out.append([mat_sub(vals[i],vals[0],C) for i in range(3)])
    return out
PD=pair_deltas();Z=C.zero()

def cp_from_trits(vals):
    D=[[Z for _ in range(9)] for _ in range(9)]
    for i,v in enumerate(vals):
        if v:
            M=PD[i][v]
            for r in range(9):
                for s in range(9):D[r][s]=C.add(D[r][s],M[r][s])
    return tuple(charpoly_from_traces(traces(D,9,C),C))
