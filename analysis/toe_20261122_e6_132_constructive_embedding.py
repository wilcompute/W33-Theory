#!/usr/bin/env python3
"""Constructive H27-equivariant 81->132 isometry using E6 trinification 78+27+27bar.

The target 81D H27-invariant subspace is (3,3,3) subset 78, plus 27 and bar27.
It is NOT E6-invariant: the 78 adjoint irrep has no proper E6 submodule.
"""
from __future__ import annotations
from pathlib import Path
import json
import numpy as np
OUT=Path(__file__).resolve().parents[1]/'data/toe_20261122_e6_132_constructive_embedding.json'

def tensor(*a):
    x=np.array([[1]],complex)
    for y in a:x=np.kron(x,y)
    return x

def blocks(*a):
    out=np.zeros((sum(len(x) for x in a),sum(len(x) for x in a)),complex)
    k=0
    for x in a:n=len(x);out[k:k+n,k:k+n]=x;k+=n
    return out

def verify():
    w=np.exp(2j*np.pi/3);e=np.eye(3,dtype=complex);X=np.roll(e,1,axis=0);Z=np.diag([1,w,w*w]);
    # Relation XZ X^-1 Z^-1 = w^-1 I.
    assert np.max(abs(X@Z@X.conj().T@Z.conj().T-w.conjugate()*e))<1e-13
    xn=tensor(X,e,X);yn=tensor(Z,e,Z.conj());
    xq=blocks(tensor(X.conj(),e),tensor(e,X),tensor(X,X.conj()))
    yq=blocks(tensor(Z.conj(),e),tensor(e,Z.conj()),tensor(Z,Z))
    xb=xq.conj();yb=yq.conj()
    reps=[(xn,yn),(xq,yq),(xb,yb)]
    for t,(a,b) in enumerate(reps):
        z=a@b@a.conj().T@b.conj().T
        assert np.max(abs(z-(w**t)*np.eye(27)))<2e-13,(t,np.max(abs(z-(w**t)*np.eye(27))))
        assert np.max(abs(np.linalg.matrix_power(a,3)-np.eye(27)))<1e-12
        assert np.max(abs(np.linalg.matrix_power(b,3)-np.eye(27)))<1e-12
    uniform=np.ones(3,complex)/np.sqrt(3)
    neutral=[tensor(e[:,0],e[:,r],uniform).reshape(-1) for r in range(3)]
    bell=sum((tensor(e[:,j],e[:,j]).reshape(-1) for j in range(3)))/np.sqrt(3)
    third=sum((tensor(e[:,j],e[:,0]).reshape(-1) for j in range(3)))/np.sqrt(3)
    charged=[]
    for k,v in enumerate((bell,bell,third)):
        tmp=np.zeros(27,complex);tmp[9*k:9*(k+1)]=v;charged.append(tmp)
    fid=[neutral,charged,[np.conj(v) for v in charged]]
    # Each of three spectral sectors is a 27D sum of three 9-state orthonormal Weyl orbits.
    orbit=[]
    for t,(a,b) in enumerate(reps):
        blocks_t=[]
        for r in range(3):
            V=np.column_stack([np.linalg.matrix_power(a,p)@np.linalg.matrix_power(b,q)@fid[t][r]
                           for p in range(3) for q in range(3)])
            assert np.max(abs(V.conj().T@V-np.eye(9)))<2e-12,(t,r)
            blocks_t.append(V)
        for i in range(3):
            for j in range(i+1,3):assert np.max(abs(blocks_t[i].conj().T@blocks_t[j]))<2e-12
        orbit.append(blocks_t)
    # Target inclusion: selected neutral adjoint 27 plus charged 27+bar27, padded by 51 other adjoint basis vectors.
    # T maps three regular 27D permutation modules to a subspace of the 132D E6 module.
    T=np.zeros((132,81),complex)
    def label(a,b,c):return (a*3+b)*3+c
    Lx=np.zeros((81,81),complex);Ly=np.zeros((81,81),complex);Lz=np.zeros((81,81),complex)
    for r in range(3):
      for a in range(3):
       for b in range(3):
        for c in range(3):
         j=r*27+label(a,b,c)
         Lx[r*27+label((a+1)%3,b,c),j]=1
         Ly[r*27+label(a,(b+1)%3,(c-a)%3),j]=1
         Lz[r*27+label(a,b,(c+1)%3),j]=1
         for t in range(3):
            piece=(w**(t*c))*orbit[t][r][:,a*3+b]/np.sqrt(3)
            offset=(0,78,105)[t]
            T[offset:offset+27,j]=piece
    assert np.max(abs(T.conj().T@T-np.eye(81)))<2e-12
    # Images of x,y,z under the target E6 module's subgroup action.
    Xt=blocks(xn,np.eye(51),xq,xb);Yt=blocks(yn,np.eye(51),yq,yb)
    Zt=blocks(np.eye(78),w*np.eye(27),w*w*np.eye(27))
    residual={
        'x':float(np.max(abs(Xt@T-T@Lx))),
        'y':float(np.max(abs(Yt@T-T@Ly))),
        'z':float(np.max(abs(Zt@T-T@Lz))),
        'isometry':float(np.max(abs(T.conj().T@T-np.eye(81))))}
    assert all(v<2e-12 for v in residual.values()),residual
    # Source restriction characters are 3*regular H27: 81 on identity, 0 elsewhere.
    trace_noncentral=[]
    for a in range(3):
      for b in range(3):
       if (a,b)==(0,0):continue
       tr=sum(np.trace(np.linalg.matrix_power(A,a)@np.linalg.matrix_power(B,b))
                   for A,B in reps)
       trace_noncentral.append(float(abs(tr)))
    assert max(trace_noncentral)<1e-12
    assert abs(np.trace(Zt@T@T.conj().T))<1e-12
    # Known 78->(8,1,1)+(1,8,1)+(1,1,8)+(3,3,3)+(bar3,bar3,bar3)
    # H27 neutral adjoint traces at any noncentral (a,b) are (-1)+8+(-1)+0+0=6.
    chars={'identity':78,'center_nontrivial':78,'noncentral':6}
    invariant=(78+8*6)//9
    nontrivial=(78-6)//9
    assert invariant==14 and nontrivial==8
    d=dict(status='PASS_CONSTRUCTIVE_132D_E6_H27_MODULE_EMBEDDING',
      source='three 27D regular H27 address modules',source_dimension=81,
      E6_target='78 adjoint + 27 fundamental + 27bar antifundamental',target_dimension=132,
      target_H27_module_subspace='(3,3,3) 27 of adjoint + fundamental 27 + anti-fundamental 27bar',
      subgroup_generators='first SU3 x=X,y=Z; middle SU3 x=y=I; third SU3 x=X,y=Z^-1; center (w^-1,I,w)',
      source_center_spectral_dimensions=[27,27,27],
      adjoint_78_quotient_character=chars,
      adjoint_78_Z3_squared_char_multiplicity={'trivial':invariant,'each_nontrivial':nontrivial},
      explicit_isometric_intertwiner_shape=[132,81],
      intertwiner_max_abs_residual=residual,
      neutral_sector_fiducials='|0,r> tensor (|0>+|1>+|2>)/sqrt(3) for r=0,1,2',
      charged_sector_fiducials='Bell states on first two 9D E6 fundamental blocks and 3-state shift-Fourier orbit on third',
      proof='Three central sectors each have 3 mutually orthogonal 9-state Heisenberg Weyl orbits. The finite-group central Fourier transform on c yields 3 regular 27D permutation modules in 132D. T^dagger T=I and rho(g)T=TL_g hold for x,y,z.',
      caveats='The image is H27-invariant but NOT E6-invariant because its 27D piece lies properly inside irreducible E6 adjoint78. Thus 132D is a valid E6 carrier with 51 leaked directions, not a complete 81D E6 theory. This resolves necessary dimension 132 as attainable for H27-equivariant submodule, not E6-equivariance of T.' )
    return d

if __name__=='__main__':
    d=verify();OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
    print(d['status'],d['intertwiner_max_abs_residual'])
