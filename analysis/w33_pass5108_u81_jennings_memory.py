#!/usr/bin/env python3
"""Pass5108 (bonkers): augmentation/Jennings memory layers of the U81 controller."""
from __future__ import annotations
import json
from collections import deque
from pathlib import Path
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5108_U81_JENNINGS_MEMORY.json'

class Span:
    def __init__(self,p,n):self.p=p;self.n=n;self.rows={}
    def add(self,v):
        p=self.p;v=[int(x)%p for x in v]
        while True:
            k=next((i for i,x in enumerate(v) if x),None)
            if k is None:return False
            if k not in self.rows:break
            f=v[k];r=self.rows[k];v=[(v[i]-f*r[i])%p for i in range(self.n)]
        z=pow(v[k],-1,p);v=[z*x%p for x in v]
        for j,r in list(self.rows.items()):
            if r[k]:
                f=r[k];self.rows[j]=[(r[i]-f*v[i])%p for i in range(self.n)]
        self.rows[k]=v;return True
    @property
    def rank(self):return len(self.rows)
    def basis(self):return list(self.rows.values())

def group(gens,p=3):
    I=np.eye(4,dtype=int)%p;key=lambda A:tuple(map(int,A.flat));G={key(I):I};Q=deque([I])
    while Q:
        a=Q.popleft()
        for g in gens:
            b=(a@g)%p;k=key(b)
            if k not in G:G[k]=b;Q.append(b)
    return list(G.values())

def powers(G,gens,p=3):
    key=lambda A:tuple(map(int,A.flat));idx={key(a):i for i,a in enumerate(G)};n=len(G);perms=[[idx[key((a@g)%p)] for a in G] for g in gens]
    cur=Span(p,n)
    for perm in perms:
        for i,j in enumerate(perm):
            v=[0]*n;v[j]=1;v[i]=(v[i]-1)%p;cur.add(v)
    dims=[n,cur.rank]
    while cur.rank:
        nxt=Span(p,n)
        for v in cur.basis():
            for perm in perms:
                out=[0]*n
                for i,c in enumerate(v):
                    if c:out[perm[i]]=(out[perm[i]]+c)%p;out[i]=(out[i]-c)%p
                nxt.add(out)
        cur=nxt;dims.append(cur.rank)
    return dims,[dims[i]-dims[i+1] for i in range(len(dims)-1)]

def main():
    I=np.eye(4,dtype=int)%3
    def E(i,j):M=np.zeros((4,4),dtype=int);M[i,j]=1;return M
    X=[E(0,1)-E(3,2),E(1,3),E(0,3)+E(1,2),E(0,2)];r=[(I+Z)%3 for Z in X]
    U=group([r[0],r[1]]);Hs=group([r[0],r[2]]);Hf=group([r[1],r[2],r[3]])
    du,lu=powers(U,[r[0],r[1]]);ds,ls=powers(Hs,[r[0],r[2]]);df,lf=powers(Hf,[r[1],r[2],r[3]])
    assert du==[81,80,78,74,69,62,54,45,36,27,19,12,7,3,1,0]
    assert ds==[27,26,24,20,16,11,7,3,1,0] and df==[27,26,23,17,10,4,1,0]
    t=sp.symbols('t');PU=sp.Poly((1+t+t**2)**2*(1+t**2+t**4)*(1+t**3+t**6),t);PS=sp.Poly((1+t+t**2)**2*(1+t**2+t**4),t);PF=sp.Poly((1+t+t**2)**3,t)
    assert lu==[int(x) for x in reversed(PU.all_coeffs())] and ls==[int(x) for x in reversed(PS.all_coeffs())] and lf==[int(x) for x in reversed(PF.all_coeffs())]
    out={'pass':5108,'status':'THEOREM_U81_JENNINGS_ROOT_HEIGHT_MEMORY','field':'F3',
         'U81':{'augmentation_power_dimensions':du,'successive_layers':lu,'Hilbert_series':'(1+t+t^2)^2(1+t^2+t^4)(1+t^3+t^6)','root_heights':[1,1,2,3]},
         'H27_state':{'augmentation_power_dimensions':ds,'successive_layers':ls,'Hilbert_series':'(1+t+t^2)^2(1+t^2+t^4)','root_heights':[1,1,2]},
         'F3_3_program':{'augmentation_power_dimensions':df,'successive_layers':lf,'Hilbert_series':'(1+t+t^2)^3','flat_degrees':[1,1,1]},
         'interpretation':'Because Pass5105 proves H1(F3)|U ~= F3[U], these augmentation layers are an exact nilpotent filtration of the protected 81-dimensional memory. The U81 profile records the C2 positive-root heights and refines both BT865 order-27 coordinatizations.',
         'boundary':'Finite modular-representation/Jennings data only; memory depth here is algebraic nilpotence, not a hardware latency or coherence time.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
