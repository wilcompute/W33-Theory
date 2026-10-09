"""Interacting 40-line low-energy W33 selector cells on finite chains.

40-state effective cell Hamiltonian H1=-h A_lines (already projected
from the 160-triple model). For N=2,3 cells on an OPEN chain,
H=-h sum_i A_i-J sum_i 1[line_i=line_(i+1)].
Diagonalize sparse real symmetric H; compare exact noninteracting
gap, pair alignment, and symmetry-forced uniform one-site marginals.
Finite volumes cannot certify spontaneous SSB or FCC spacetime.
"""
from pathlib import Path
import json,sys
import numpy as np
from scipy.sparse import eye,csr_matrix,kron,diags
from scipy.sparse.linalg import eigsh
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import bt1688_exact_h1_character_irreducibility as B
def certificate():
    lines=B.w33_lines(B.make_points())
    L=np.array([[int(len(set(x)&set(y))==1) for y in lines] for x in lines],dtype=float)
    assert np.all(L.sum(axis=1)==12)
    A=csr_matrix(L);I=eye(40,format='csr')
    h=.2
    results=[]
    for N,J in [(2,0.),(2,.2),(2,.8),(2,2.0),(3,0.),(3,.5)]:
        D=40**N
        H=csr_matrix((D,D))
        for i in range(N):
            mats=[A if j==i else I for j in range(N)]
            kronmatrix=mats[0]
            for z in mats[1:]:kronmatrix=kron(kronmatrix,z,format='csr')
            H=H-h*kronmatrix
        coords=np.indices((40,)*N,sparse=False).reshape(N,-1)
        align=np.sum(coords[:-1]==coords[1:],axis=0)
        H=H-J*diags(align.astype(float),format='csr')
        ev,vec=eigsh(H,k=2,which='SA',tol=1e-8,maxiter=1300)
        order=np.argsort(ev);ev=ev[order];psi=vec[:,order[0]]
        if psi.sum()<0:psi=-psi
        assert psi.min()>-1e-8
        prob=psi*psi
        marginal=np.bincount(coords[0],weights=prob,minlength=40)
        # unique G-invariant ground state => each W33 line equiprobable.
        marginal_err=float(max(abs(marginal-1/40)))
        p_align=float(prob@align/(N-1))
        if J==0:
            assert abs(ev[0]+12*N*h)<1e-7
            assert abs((ev[1]-ev[0])-10*h)<1e-5
            assert abs(p_align-.025)<1e-8
        assert marginal_err<2e-5
        results.append(dict(cells=N,alignment_coupling_J=J,local_hopping_h=h,
            ground_energy=float(ev[0]),first_ordered_energy=float(ev[1]),
            first_ordered_gap=float(ev[1]-ev[0]),
            mean_neighbor_line_agreement=p_align,
            max_error_from_uniform_onesite_marginal=marginal_err,
            Hilbert_dimension=D))
        print('COUPLED',N,J,'gap',round(float(ev[1]-ev[0]),8),
          'P_align',round(p_align,6),flush=True)
    assert results[3]['mean_neighbor_line_agreement']>results[0]['mean_neighbor_line_agreement']+.04
    assert results[-1]['mean_neighbor_line_agreement']>results[4]['mean_neighbor_line_agreement']+.005
    return dict(status='PASS',schema='w33.20261009.coupled_selector.v1',results=results,
        cell_space='40 distinct W33 lines; 160-state collinear triples projected to uniform K4 line subspace',
        graph_L_eigenvalues={'12':1,'2':24,'-4':15},
        noninteracting_Ncell_Eground='-12*N*h',noninteracting_gap='10*h',
        finite_volume_theorem='Each finite connected stoquastic selector-chain Hamiltonian has unique positive PF ground state. Exact W33 automorphism transitivity forces uniform single-site line marginals. Local ferromagnetic alignment can raise intersite correlations without finite-volume spontaneous breaking.',
        distinction='This is an imposed finite open chain of W33 line contexts and equality interaction, not a derived physical lattice, thermodynamic limit, universal speed or Einstein dynamics.')
if __name__=='__main__':
    d=certificate()
    (ROOT/'data/w33_20261009_coupled_finite_selector_cells.json').write_text(json.dumps(d,indent=2)+'\n')
    print('PASS')
