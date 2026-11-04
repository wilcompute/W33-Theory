#!/usr/bin/env python3
"""Fully local *linear* spin-2 constraint/Hamiltonian positive control on a
SUPPLIED three-dimensional cubic torus, contrasted against inhomogeneous
noncommuting local derivatives.

No W33 emergence, no non-linear Dirac/hypersurface algebra, no universal
gravitational matter coupling. Supports 2 tensor modes at each k!=0.
"""
from __future__ import annotations
import json,numpy as np
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'2026_11_03_local_spin2_hamiltonian_closure.json'
PAIRS=[(0,0),(1,1),(2,2),(0,1),(0,2),(1,2)]
def derivs(L):
    n=L**3; out=[np.zeros((n,n)) for _ in range(3)]
    def ix(x):return (x[0]*L+x[1])*L+x[2]
    for x in range(L):
      for y in range(L):
        for z in range(L):
          site=(x,y,z);u=ix(site)
          for i in range(3):
            a=list(site);b=list(site)
            a[i]=(a[i]+1)%L;b[i]=(b[i]-1)%L
            out[i][u,ix(a)]+=.5;out[i][u,ix(b)]-=.5
    assert all(np.max(abs(A+A.T))<1e-12 for A in out)
    return out
def operators(D):
    n=len(D[0]);dtype=np.result_type(*[A.dtype for A in D]);Z=np.zeros((n,n),dtype=dtype);delta=sum((A@A for A in D),Z.copy())
    # scalar Hamiltonian constraint H0 q=0; momentum Mi p=0
    H=np.hstack([delta-D[i]@D[i] if i==j else -(D[i]@D[j]+D[j]@D[i])
                  for i,j in PAIRS])
    M=np.vstack([np.hstack([
      D[k] if i==j==k else D[j]/2 if i!=j and i==k else
      D[i]/2 if i!=j and j==k else Z for i,j in PAIRS]) for k in range(3)])
    G6=np.zeros((6,6));G6[:3,:3]=2*np.eye(3)-np.ones((3,3))
    for a in range(3,6):G6[a,a]=1.
    G=np.kron(G6,np.eye(n))
    # Local Fierz--Pauli spatial gradient Hessian, in configuration
    # h_ij with canonical p_offdiag=2pi_ij.
    V=np.zeros((3*n,6*n),dtype=dtype)
    T=np.zeros((3*n,6*n),dtype=dtype)
    for j in range(3):
        for a in range(3):T[j*n:(j+1)*n,a*n:(a+1)*n]=D[j]
        for a,(i,k) in enumerate(PAIRS):
            if i==k and j==i:
                V[j*n:(j+1)*n,a*n:(a+1)*n]=D[i]
            if i!=k:
                if j==i:V[j*n:(j+1)*n,a*n:(a+1)*n]=D[k]
                if j==k:V[j*n:(j+1)*n,a*n:(a+1)*n]=D[i]
    W6=np.diag([1,1,1,2,2,2])
    K=np.kron(.5*W6,-delta)-V.conj().T@V+.5*(V.conj().T@T+T.conj().T@V)-.5*T.conj().T@T
    assert np.max(abs(K-K.conj().T))<1e-11
    assert np.max(abs(G-G.T))<1e-11
    divergence=np.hstack([sum((D[i]@M[i*n:(i+1)*n,j*n:(j+1)*n]
                            for i in range(3)),Z.copy()) for j in range(6)])
    return H,M,G,K,divergence
def checks(D):
    H,M,G,K,div=operators(D)
    n=len(D[0])
    b=float(np.max(abs(H@M.T)))
    hg=float(np.max(abs(H@G+2*div)))
    mk=float(np.max(abs(M@K)))
    # Quadratic hamiltonian equations qdot=Gp, pdot=-Kq:
    # H0dot=-2 div(Mp), Midot=0 if local derivatives commute.
    return {"sites":n,"symmetric_components":6*n,"momentum_constraint_rows":3*n,
        "scalar_constraint_rows":n,
        "max_scalar_momentum_Poisson_bracket":b,
        "max_scalar_evolution_minus_momentum_divergence":hg,
        "max_momentum_evolution_residual":mk,
        "derivative_commutator_norms":[float(np.linalg.norm(D[a]@D[b]-D[b]@D[a]))
                                       for a,b in ((0,1),(0,2),(1,2))]}
def harmonic_sector(k):
    d=np.array([1j*np.sin(2*np.pi*x/3) for x in k])
    D=[np.array([[z]]) for z in d]
    H,M,G,K,div=operators(D)
    # Use complex transpose with no conjugation for formal Fourier symbol:
    # rank and dynamical constraints are calculated from operator symbols.
    R=np.vstack((H,M))
    return {"momentum":list(k),"rank_constraints":int(np.linalg.matrix_rank(R,tol=1e-8)),
       "remaining_configuration_modes":6-int(np.linalg.matrix_rank(R,tol=1e-8)),
       "hamiltonian_wave_eigenvalues_realparts":
         sorted(float(v.real) for v in np.linalg.eigvals(G@K)),
       "max_eigenvalue_imag":float(max(abs(v.imag) for v in np.linalg.eigvals(G@K)))}
def run():
    D=derivs(3);good=checks(D)
    assert max(good['derivative_commutator_norms'])<1e-12
    assert good['max_scalar_momentum_Poisson_bracket']<1e-11
    assert good['max_scalar_evolution_minus_momentum_divergence']<1e-11
    assert good['max_momentum_evolution_residual']<1e-11,good
    # Every nonzero k has 4 independent first-class constraints, leaving
    # 2 transverse-traceless configuration DOFs. At k=0 all six remain.
    spectrum=[harmonic_sector(k) for k in
              ((0,0,0),(1,0,0),(1,1,0),(1,1,1))]
    assert spectrum[0]['remaining_configuration_modes']==6
    assert all(z['remaining_configuration_modes']==2 for z in spectrum[1:])
    assert all(z['max_eigenvalue_imag']<5e-8 for z in spectrum)
    for z in spectrum[1:]:
        lattice_wave=float(sum(np.sin(2*np.pi*x/3)**2 for x in z['momentum']))
        assert all(abs(v-lattice_wave)<1e-8 for v in z['hamiltonian_wave_eigenvalues_realparts'][-2:])
        assert all(abs(v)<1e-7 for v in z['hamiltonian_wave_eigenvalues_realparts'][:-2])
    # A scalar positive local modulation of y derivative by an x-dependent
    # site weight keeps it antisymmetric and 1-hop local, but destroys
    # commuting Cartesian shift structure and the naive constraint algebra.
    W=np.diag([1+.05*np.cos(2*np.pi*x/3) for x in range(3)
                              for y in range(3) for z in range(3)])
    alt=[D[0],W@D[1]@W,D[2]]
    bad=checks(alt)
    assert bad['derivative_commutator_norms'][0]>1e-3,bad
    assert bad['max_scalar_momentum_Poisson_bracket']>1e-4,bad
    assert bad['max_momentum_evolution_residual']>1e-4,bad
    out={"status":"PASS_LOCAL_LINEAR_SPIN2_FIRST_CLASS_AND_INHOMOGENEOUS_OBSTRUCTION",
      "discrete_geometry_given":"3×3×3 spatial periodic Cartesian lattice with central difference operators D_i=(shift_i+-shift_i-)/2. Time evolution is Hamiltonian and not derived from an emergent clock.",
      "linear_constraints":"H0=Σ_i D_i² tr(h)−Σ_i,j D_iD_j h_ij; Mi=Σ_j D_j pi_ij, canonical p_off=2pi_off. Hamiltonian H=0.5 p^T Gp+0.5 h^T Kh using local ADM linear kinetic DeWitt G and spatial Fierz-Pauli quadratic Hessian K.",
      "local_Fierz_Pauli_potential":"V=1/4 sum_{kij}(D_k h_ij)²−1/2 sum_j(sum_i D_i h_ij)²+1/2 sum_j(sum_i D_i h_ij) D_j tr h−1/4 sum_j(D_j tr h)².",
      "algebraic_closure":"For commuting skew-adjoint D_i: H0 Mi^T=0, H0 G=-2 Σ_i D_i Mi, Mi K=0. All local identities. On Fourier k!=0 rank constraints=4 leaving 2 physical configuration modes; k=0 retains 6 global modes.",
      "commuting_cartesian_control":good,"nonzero_and_zero_momentum_sector_tests":spectrum,
      "inhomogeneous_local_skew_derivative_defect":bad,
      "important_limit":"A valid *linear*, locally first-class spin-2 positive control on a GIVEN flat periodic spatial lattice. No emergent 3-space, Lorentzian metric dynamics, nonlinear hypersurface deformation algebra or universal matter coupling. The modulated skew derivative failure is for this specific naive prescription, not a general curved discrete-gravity no-go.",
      "prior_repo":["analysis/w33_pass11968_native_spin2_constraint_completion.py","analysis/2026_11_03_alternative_torus_spin2_controls.py"],
      "literature":["https://doi.org/10.1103/PhysRev.135.B1049","https://doi.org/10.1103/PhysRevD.96.084048"]}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print("SPIN2 LOCAL",{"commuting":good,"perturbed":bad,"modes":[z['remaining_configuration_modes'] for z in spectrum]},flush=True)
if __name__=="__main__":run()
