#!/usr/bin/env python3
"""Does a four-address *noncontiguous* quantum-mode partition distinguish W/Q?
Analytical reduced-purity contraction, O(40^5), no 1600x1600 SVD required.

For a,b,c,d product addresses, psi=40^-2 S_ab S_bc S_cd.
Cut (a,c)|(b,d). Reduced rho_(ac,a'c')=
  (S^2)_{cc'} * [S diag(S_:c*S_:c') S]_{aa'} /40^4.
Hence purity = sum_{cc'} (S^2_cc')^2 *
     x_cc'^T [(S^2) hadamard (S^2)] x_cc' /40^8,
x_cc'=S_:c*S_:c'. Exact integer numerator.
"""
import json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_q43_cospectral_mode_entanglement_phase_complexity_20261023 import graphs

def alternating_four_integer_purity(A):
    S=1-2*A.astype(np.int64)
    H=S@S
    X=(S[:,:,None]*S[:,None,:]).transpose(1,2,0).reshape(1600,40)
    K=H*H
    moments=np.einsum('ni,ij,nj->n',X,K,X,optimize=True)
    numer=int(np.dot(H.reshape(-1).astype(np.int64)**2,moments.astype(np.int64)))
    denom=40**8
    xAx=np.einsum('ni,ij,nj->n',X,A.astype(np.int64),X,optimize=True).reshape(40,40)
    non=xAx[np.logical_and(A==0,~np.eye(40,dtype=bool))]
    v,n=np.unique(non,return_counts=True)
    return {'purity_numerator':numer,'denominator':denom,
       'purity':numer/denom,
       'nonadjacent_two_address_xAx_values':{str(int(vv)):int(nn) for vv,nn in zip(v,n)},
       'method':'Exact integer reduction formula for noncontiguous a,c | b,d cut of nearest-neighbor four-factor pure phase tensor'}

def certificate():
    W,Q=graphs()
    a=alternating_four_integer_purity(W)
    b=alternating_four_integer_purity(Q)
    return {'schema':'w33.q43.four_address_alternating_cut_purity.v1',
      'geometry_cut':'n4 path graph; odd-even factor cut (a,c)|(b,d)',
      'W33':a,'Q43':b,'numerators_different':a['purity_numerator']!=b['purity_numerator'],
      'physical_boundary':'Four independently addressable 40-state factors and three coherent cross-digit graph-controlled phase operations unbuilt'}
if __name__=='__main__':
    x=certificate()
    print('W purity',x['W33']['purity'],'Q purity',x['Q43']['purity'],'distinguish',x['numerators_different'])
    print('W xAx',x['W33']['nonadjacent_two_address_xAx_values'])
    print('Q xAx',x['Q43']['nonadjacent_two_address_xAx_values'])
    p=ROOT/'data/w33_q43_four_address_alternating_cut_purity_20261023.json'
    p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
