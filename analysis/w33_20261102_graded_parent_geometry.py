"""Explicit KO6 sign completion of the native commutator Dirac operator.

The sign table, Clifford-module doubling and finite-triple axioms are prior
noncommutative geometry. Minimality below is only within the stated tensor ansatz.
"""
import pathlib,sys,json,itertools
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261101_parent_control_quantum_geometry import parent_data
X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1])

def build():
    _,_,_,Q=parent_data();H=np.eye(9)-Q
    D0=np.kron(np.eye(9),H)-np.kron(H.T,np.eye(9));J0=np.zeros((81,81))
    for i,j in itertools.product(range(9),repeat=2):J0[j+9*i,i+9*j]=1
    # J=A K, with K ordinary conjugation in these vectorised coordinates.
    T=np.kron(X,np.eye(2));G=np.kron(Z,np.eye(2));A=np.kron(Y,Y)
    D=np.kron(T,D0);Gamma=np.kron(G,np.eye(81));J=np.kron(A,J0)
    I=np.eye(324);errors={
      'D_selfadjoint':np.linalg.norm(D-D.conj().T),
      'grading_square':np.linalg.norm(Gamma@Gamma-I),
      'D_odd':np.linalg.norm(D@Gamma+Gamma@D),
      'J_square_plus':np.linalg.norm(J@J.conj()-I),
      'JD_plus':np.linalg.norm(J@D.conj()-D@J),
      'J_grading_minus':np.linalg.norm(J@Gamma.conj()+Gamma@J)}
    rng=np.random.default_rng(61102)
    a,b=[rng.normal(size=(9,9))+1j*rng.normal(size=(9,9))for _ in range(2)]
    L=np.kron(np.eye(4),np.kron(np.eye(9),a));R=np.kron(np.eye(4),np.kron(b.T,np.eye(9)))
    C=D@L-L@D
    errors.update(order_zero=np.linalg.norm(L@R-R@L),first_order=np.linalg.norm(C@R-R@C),
                  grading_commutes_left=np.linalg.norm(Gamma@L-L@Gamma))
    assert max(errors.values())<1e-10
    assert np.linalg.norm(Y@Y.conj()+np.eye(2))<1e-12
    eig=np.linalg.eigvalsh(D);assert np.allclose(eig,[-1]*72+[0]*180+[1]*72)
    # All orienting zero-cycles act trivially on the external spin factor.
    # The single K0 generator e gives a vanishing intersection form.
    e=np.diag([1]+[0]*8);Le=np.kron(np.eye(4),np.kron(np.eye(9),e));Re=np.kron(np.eye(4),np.kron(e.T,np.eye(9)))
    intersection=float(np.trace(Gamma@Le@Re).real);assert abs(intersection)<1e-12
    return dict(status='PASS_KO6_PARENT_COMPLETION_WITH_ORIENTABILITY_DUALITY_OBSTRUCTIONS',dimension=324,
        exact_maps='H=I-Q; D0=ad_H on Mat9. On C2 tensor C2 tensor Mat9: D=sigma_x tensor I2 tensor D0; Gamma=sigma_z tensor I2 tensor I81; J=(sigma_y tensor sigma_y tensor transpose81) K. Mat9 acts by I4 tensor left multiplication.',
        KO6_signs={'J_squared':1,'JD_sign':1,'J_Gamma_sign':-1},matrix_identity_errors={k:float(v)for k,v in errors.items()},
        spectrum={'-1':72,'0':180,'1':72},intersection_form=[[intersection]],
        minimum_spin_multiplicity_in_tensor_ansatz=4,
        restricted_minimality='Assume D=T tensor ad_H and Gamma=G tensor I, with spin involutions T,G anticommuting, and a spin antiunitary reversing both. The complex Cl2 module has dimension2r; in canonical form the antiunitary is(sigma_y tensor B)K. Its square is-I2 tensor B conjugate(B). KO6 requires B conjugate(B)=-I_r; determinants force r even. Thus minimum spin dimension4, attained by B=sigma_y. This does not classify arbitrary Dirac operators or enlarged algebras.',
        two_spin_completion='With only C2, J=(sigma_y tensor transpose81)K obeys JD=+DJ and JGamma=-GammaJ but J^2=-1: KO2 signs, not KO6.',
        orientability_obstruction='Every zero-dimensional orienting cycle sum L_a J L_b^* J^-1 acts as I4 tensor an operator on Mat9; Gamma has nontrivial sigma_z on the spin factor. Hence no such cycle equals Gamma.',
        duality_obstruction='For the sole K0 generator of complex Mat9, Tr(Gamma L_e R_e)=0. The one-by-one intersection form is zero, so Poincare duality fails for this algebra/module.',
        spectral_action='180f(0)+144f(1/Lambda^2); external spin multiplicity changes counts but cannot distinguish the810 conjugate parents.',
        boundary='An explicit even real first-order construction with KO6 signs, failing orientability and duality. Sign completion alone does not produce a Standard Model, physical fermion multiplicity or Lorentzian gravity. No universal minimal-dimension theorem is asserted.')

if __name__=='__main__':
    out=build();(ROOT/'data/w33_20261102_graded_parent_geometry.json').write_text(json.dumps(out,indent=2)+'\n')
    print(out['status'],out['dimension'],flush=True)
