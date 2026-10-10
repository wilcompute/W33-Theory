#!/usr/bin/env python3
"""Pass7324: integral/3-adic refinement of the common 1+20 tritangent carrier."""
from __future__ import annotations
import json,math
from collections import Counter
from pathlib import Path
import numpy as np
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
from w33_pass4992_4999_common import build_base,gf2_rank_matrix

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7324_INTEGRAL_SPREAD_LATTICES.json'

def rankp(A,p):
    M=np.array(A,dtype=np.int64)%p;m,n=M.shape;r=0
    for c in range(n):
        q=next((i for i in range(r,m) if M[i,c]%p),None)
        if q is None:continue
        M[[r,q]]=M[[q,r]];M[r]=(M[r]*pow(int(M[r,c]),-1,p))%p
        for i in range(m):
            if i!=r and M[i,c]:M[i]=(M[i]-M[i,c]*M[r])%p
        r+=1
        if r==m:break
    return r

def snf_profile(A):
    D=smith_normal_form(sp.Matrix(A),domain=sp.ZZ);diag=[abs(int(D[i,i])) for i in range(min(D.shape)) if D[i,i]!=0]
    return diag,Counter(diag)

def main():
    b=build_base();N=1-np.asarray(b['M'],dtype=np.int64) # 45 x 36 doily-slice columns
    # 27 cubic-line stars on the 45 tritangents: exactly the spread-code minimum words.
    tris=b['tritangents'];R=np.zeros((27,45),dtype=np.int64)
    for l in range(27):
        for j,t in enumerate(tris):
            if l in t:R[l,j]=1
    assert set(map(int,R.sum(1)))=={5} and set(map(int,R.sum(0)))=={3}
    assert np.array_equal(R@R.T,5*np.eye(27,dtype=np.int64)+nx_adj(b['G27']))
    assert sp.Matrix(N).rank()==sp.Matrix(R.T).rank()==21
    assert gf2_rank_matrix(N.T)==21 and gf2_rank_matrix(R)==21
    dn,cn=snf_profile(N);dr,cr=snf_profile(R.T)
    assert cn==Counter({1:14,3:7})
    # Both lattices live in the same rational 1+20 space.
    assert sp.Matrix.hstack(sp.Matrix(N),sp.Matrix(R.T)).rank()==21
    # Integer centered doily frame: X=3N-J has pure V20 rational span.
    X=3*N-np.ones_like(N);assert sp.Matrix(X).rank()==20 and np.all(X.sum(axis=0)==0)
    dx,cx=snf_profile(X)
    ranks={}
    for p in (2,3,5,7,11):ranks[str(p)]={'N':rankp(N,p),'Rstar':rankp(R.T,p),'Xcentered':rankp(X,p)}
    # Common primitive saturation index data from nonzero Smith factors.
    indN=math.prod(dn);indR=math.prod(dr);indX=math.prod(dx)
    out={'schema':'w33.pass7324.integral_spread_lattices.v1','status':'PASS',
      'rational_common_space':'1 + V20_trit','rational_dimension':21,
      'doily_lattice':{'matrix':'N 45x36','SNF':{str(k):v for k,v in sorted(cn.items())},'saturation_index':indN},
      'cubic_line_star_lattice':{'matrix':'R^T 45x27','SNF':{str(k):v for k,v in sorted(cr.items())},'saturation_index':indR},
      'centered_doily_V20_lattice':{'matrix':'X=3N-J','rank':20,'SNF':{str(k):v for k,v in sorted(cx.items())},'saturation_index':indX},
      'modular_ranks':ranks,
      'identity':'R R^T = 5 I_27 + A_(27,10,1,5), hence rational spectrum 15^1 + 6^20 + 0^6 and rank 21.',
      'interpretation':'The binary equality of the doily-slice and spread codes hides distinct integral lattices inside the same rational 1+20 carrier; their Smith profiles measure the exact 3-adic obstruction to splitting/identifying them integrally.',
      'boundary':'Integral lattice comparison only; no physical meaning is assigned to the 3-primary indices.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','SNF_N':out['doily_lattice']['SNF'],'SNF_R':out['cubic_line_star_lattice']['SNF'],'SNF_X':out['centered_doily_V20_lattice']['SNF'],'ranks':ranks}))

def nx_adj(G):
    A=np.zeros((len(G),len(G)),dtype=np.int64)
    for i,j in G.edges():A[i,j]=A[j,i]=1
    return A
if __name__=='__main__':main()
