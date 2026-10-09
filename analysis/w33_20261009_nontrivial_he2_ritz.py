"""PSp(4,3)-symmetry-resolved He2 Ritz sectors of the 78D W33
Hamiltonian, correcting the prior singlet-only 11-state limitation.

40 point and 40 line He2 waves each decompose as 1+24+15.
The point-line incidence operator N has singular values 4(1),
sqrt6(24),0(15); the 24-isotypic He2 doublet gives a true 2x2
Rayleigh upper bound for at least 24 eigenvalues (counting multiplicity).
"""
from pathlib import Path
import sys,json
from math import sqrt
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261009_11state_corrected_ritz as C
import w33_20261008_5state_ritz as F
import w33_pass11769_quantized_current_vacuum as V
def certificate(order=13):
    edges,N,A,B,Wp,Wl=F.geometry()
    tr=V.exact_trial();spec=[('p',A,Wp),('l',B,Wl)]
    he={}
    for side,adj,W in spec:
        ids=[0,int(np.flatnonzero(adj[0])[0]),
             int(np.flatnonzero((adj[0]==0)&(np.arange(40)!=0))[0])]
        he[side]=[complex(C.block(edges,W[0],W[j],side,side,tr,order,left=(2,),right=(2,))[0,0])
                for j in ids]
        assert max(abs(z.imag) for z in he[side])<1e-9,he[side]
    inc=int(np.flatnonzero(N[0])[0]);non=int(np.flatnonzero(N[0]==0)[0])
    cross=[C.block(edges,Wp[0],Wl[j],'p','l',tr,order,left=(2,),right=(2,))[0,0]
           for j in (inc,non)]
    def gram(lambda_):
        return 1-1/81+lambda_*(1/9-1/81)
    def orbital(c,lambda_):
        diagonal,adjacent,non=c
        return diagonal+lambda_*adjacent+(-1-lambda_)*non
    for side in he:
        # A diagonal-orbit block is a Hermitian matrix on 40 site states.
        assert abs(orbital(he[side],2).imag)<1e-8
    n24=gram(2);n15=gram(-4)
    diag=[orbital(he[x],2)/n24 for x in ('p','l')]
    mixing=sqrt(6)*(cross[0]-cross[1])/n24
    h24=np.array([[diag[0],mixing],[mixing.conjugate(),diag[1]]],complex)
    assert np.max(abs(h24-h24.conj().T))<1e-8
    ev24=np.linalg.eigvalsh(h24)
    ev15=[float(orbital(he[x],-4).real/n15) for x in ('p','l')]
    return dict(status='PASS',schema='w33.20261009.nontrivial_he2_ritz.v1',
        quadrature_order=order,irreps={'24_point_line_doublet':list(map(float,ev24)),
           '15_point_and_line_singlets':ev15},
        Gram_sector_norms={'24':n24,'15':n15},
        orbital_diagonal_blocks={k:[[z.real,z.imag] for z in v] for k,v in he.items()},
        incidence_cross_blocks=[[z.real,z.imag] for z in cross],
        theorem='For PSp(4,3), each He2 point/line permutation module is 1+24+15. Incidence singular value sqrt6 on24, zero on15. Rayleigh-Ritz on the symmetry sectors gives ordered minmax UPPER bounds, with 24-fold or 15-fold representation multiplicities.',
        caveat='States need not be true eigenstates and no statement about the actual ground irrep, lower energies, or physical gap follows. Quadrature comparisons required.')
if __name__=='__main__':
    a=certificate(13);b=certificate(14)
    assert max(abs(x-y) for key in a['irreps'] for x,y in zip(a['irreps'][key],b['irreps'][key]))<1e-7
    a['quadrature_13_14_max_energy_difference']=max(abs(x-y) for key in a['irreps'] for x,y in zip(a['irreps'][key],b['irreps'][key]))
    (ROOT/'data/w33_20261009_nontrivial_he2_ritz.json').write_text(json.dumps(a,indent=2)+'\n')
    print('RITZ',a['irreps'],'error',a['quadrature_13_14_max_energy_difference'])
