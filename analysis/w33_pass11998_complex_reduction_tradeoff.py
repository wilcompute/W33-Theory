"""Actual U3 reduction of the atlas SO6 gates, with the lost controls explicit.

A supplied link penalty reduces the connection; the original polar transport
is not claimed to preserveJ. Standard Spin6 branching is tested on actual gates.
"""
import json,itertools
from pathlib import Path
import numpy as np
import sympy as s
from scipy.linalg import eigh,polar
from w33_pass11987_atlas_spin_gate_alphabet import gamma6,lift
ROOT=Path(__file__).resolve().parents[1]


def payload():
    source=json.loads((ROOT/'data/w33_pass11983_atlas_projector_descent.json').read_text())['compact_holonomy_closure']
    repair=json.loads((ROOT/'data/w33_pass11988_spinor_weil_intertwiner.json').read_text())['exact_projective_tangent_repair']
    gates=json.loads((ROOT/'data/w33_pass11987_atlas_spin_gate_alphabet.json').read_text())['gates']
    G=s.Matrix(source['source_fiber_Gram']);Jn=s.Matrix(repair['complex_structure_numerator_Q'])
    variables=s.symbols('a:36');A=s.Matrix(6,6,variables)
    equations=list(A.T*G+G*A)+list(A*Jn-Jn*A)
    M,_=s.linear_eq_to_matrix(equations,variables);basis=M.nullspace();assert len(basis)==9
    full=[];projected=[];broken=[]
    for i,j in itertools.combinations(range(6),2):
        E=s.zeros(6);E[i,j]=1;E[j,i]=-1;B=G.inv()*E
        keep=(B-Jn*B*Jn/3)/2;drop=(B+Jn*B*Jn/3)/2
        assert keep*Jn==Jn*keep and drop*Jn==-Jn*drop
        full.append(B);projected.append(s.Matrix(keep).reshape(36,1));broken.append(s.Matrix(drop).reshape(36,1))
    assert s.Matrix.hstack(*projected).rank()==9 and s.Matrix.hstack(*broken).rank()==6
    for x,y in itertools.combinations(basis,2):
        B=s.Matrix(6,6,x);C=s.Matrix(6,6,y);br=B*C-C*B
        assert br*Jn==Jn*br and br.T*G+G*br==s.zeros(6)
    gf=np.array(G,float);ev,v=eigh(gf);root=(v*np.sqrt(ev))@v.T;inv=(v/np.sqrt(ev))@v.T
    J=root@np.array(Jn,float)@inv/np.sqrt(3);assert np.max(abs(J@J+np.eye(6)))<1e-12
    gamma,chir,selected=gamma6()
    generator=sum(.5*J[i,j]*gamma[i]@gamma[j] for i,j in itertools.combinations(range(6),2))
    charge=(-1j*generator)[np.ix_(selected,selected)];ec,U=eigh(charge)
    clusters=[np.flatnonzero(abs(ec-val)<1e-8) for val in np.unique(np.round(ec,8))]
    assert sorted(map(len,clusters))==[1,3]
    one=next(ix for ix in clusters if len(ix)==1);e=U[:,one];P=e@e.conj().T
    loops=[]
    for row in source['first_three_loop_matrices_Q_sqrt3']:
        h=np.array(s.Matrix(row['rational'])+s.sqrt(3)*s.Matrix(row['sqrt3_coefficient']),float)
        loops.append(root@h@inv)
    a,b,c=loops;rotations=[a@a,b@a.T,c@a.T,a@b,a@c];rows=[]
    for gate,R in zip(gates,rotations):
        K=(R-J@R@J)/2;sv=np.linalg.svd(K,compute_uv=False);assert min(sv)>1e-9
        reduced,_=polar(K);assert np.linalg.det(reduced)>0 and np.max(abs(reduced@J-J@reduced))<1e-10
        S,cover,_=lift(reduced,gamma);Ur=S[np.ix_(selected,selected)]
        actual=np.array(gate['gate_real'])+1j*np.array(gate['gate_imag'])
        raw_leak=float(np.linalg.norm((np.eye(4)-P)@actual@e)**2)
        reduced_leak=float(np.linalg.norm((np.eye(4)-P)@Ur@e)**2)
        assert reduced_leak<1e-20
        anti=(R+J@R@J)/2
        assert abs(np.linalg.norm(anti)**2-np.linalg.norm(R@J-J@R)**2/4)<1e-10
        rows.append(dict(word=gate['even_word'],complex_linear_singular_values=sv.tolist(),
            native_singlet_to_triplet_probability=raw_leak,reduced_singlet_to_triplet_probability=reduced_leak,
            anti_linear_Frobenius_squared=float(np.linalg.norm(anti)**2),
            rotation_change_Frobenius=float(np.linalg.norm(reduced-R)),reduced_spin_cover_error=cover,
            reduced_gate_real=Ur.real.tolist(),reduced_gate_imag=Ur.imag.tolist()))
    assert max(row['native_singlet_to_triplet_probability'] for row in rows)>.01
    return dict(status='PASS',exact_so6_dimension=15,exact_J_centralizer_dimension=9,exact_J_anticommuting_dimension=6,
        centralizer_basis_Q=[list(map(str,v)) for v in basis],
        exact_split='For J=Jn/sqrt3, A_keep=(A-JAJ)/2=(A-Jn A Jn/3)/2 and A_drop=(A+JAJ)/2. Their ranks are9 and6. Keep is a Lie subalgebra u3.',
        spinor_charge_eigenvalues=ec.tolist(),spinor_branch_dimensions=[1,3],actual_native_gate_reductions=rows,
        link_penalty='Supply E(R)=kappa ||RJ-JR||_F². Its zero set inside SO6 is U3. The six anticommuting infinitesimal generators have positive quadratic cost; the nine commuting directions have zero cost. This changes the original polar connection.',
        finite_repair='For each tested actual even loop, K=(R-JRJ)/2 is nonsingular; its polar factor commutes withJ and is a closest U3 transport in Frobenius norm. Native finite stabilizer remains complex-linear.',
        computational_tradeoff='The reduced spinor action preserves a1+3 decomposition and is therefore not dense inSU4. The six removed pairing controls are precisely the complement needed for the original15dimensional one-block gate algebra. A chargedfamily3 reading and the full gate algebra cannot use an identical unbrokenU3 connection without additional controlled symmetry breaking.',
        interpretation='J may instead define a Majorana particle-hole polarization; then native SO6 Bogoliubov mixing remains consistent with a fixed complex Fock Hilbert space. This differs from conserving a charged family triplet.',
        boundary='Explicit conditional U3-reduced transport and control tradeoff, not a dynamically selected vacuum, physical family charges, derived gauge bosons, scalar masses or observed generations. The original exactSO6 holonomy certificate remains valid.',
        prior=['11988 exact tangent map,J and holonomy obstruction','11987 actual denseSU4 spin gates','11993 Majorana carrier, Gaussian scalability obstruction and added quartic repair'],
        primary=['https://arxiv.org/abs/quant-ph/0003137','https://moroianu.perso.math.cnrs.fr/tex/2010cmp.pdf'])

if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass11998_complex_reduction_tradeoff.json').write_text(json.dumps(d,indent=2)+'\n');print(d['status'],d['spinor_charge_eigenvalues'])
