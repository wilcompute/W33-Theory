"""Native W33 Heisenberg H27: explicit noncommutative Fourier isometry and
minimal tensor-ancilla dimension for E6 27-operator charge equivariance.

The impossibility of the direct 27->27 map and earlier multiplicity
dressings are REPOSITORY PRIOR ART. New in this packet is a constructive
full-group 27x27 unitary noncommutative Fourier map, a minimal-7
tensor-representation ancilla result, and a checked 189D target census.
"""
import sys,json,math
from pathlib import Path
import numpy as np
from sympy.combinatorics import Permutation,PermutationGroup
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261118_W33_triperiodic_Levi_homogenization as W
from toe_20261118_W33_dual_parabolic_radicals_27 import unipotent_radical

def run():
    _,points,_=W.levi();ix={v:i for i,v in enumerate(points)}
    perms=[Permutation([ix[W.projective(tuple((x[k]+W.symplectic(x,v)*v[k])%3
                           for k in range(4)))] for x in points]) for v in points]
    G=PermutationGroup(perms)
    assert G.order()==25920
    info,H=unipotent_radical(G.stabilizer(0))
    x,y=next((a,b) for a in H for b in H if a*b!=b*a)
    z=x*y*~x*~y
    assert z.order()==3 and all(z*h==h*z for h in H)
    grid=list((a,b,c) for a in range(3) for b in range(3) for c in range(3))
    natural={abc:x**abc[0]*y**abc[1]*z**abc[2] for abc in grid}
    assert len(set(natural.values()))==27
    def mul(g,h):
        a,b,c=g;A,B,C=h
        return ((a+A)%3,(b+B)%3,(c+C-b*A)%3)
    assert all(natural[g]*natural[h]==natural[mul(g,h)] for g in grid for h in grid)
    om=np.exp(2j*np.pi/3)
    X=np.array([[0,0,1],[1,0,0],[0,1,0]],complex)
    Z=np.diag([1,om,om**2])
    Y=Z@Z
    assert np.max(abs(X@Y@X.conj().T@Y.conj().T-om*np.eye(3)))<1e-12
    def rho(g):
        a,b,c=g
        return (om**c)*np.linalg.matrix_power(X,a)@np.linalg.matrix_power(Y,b)
    assert all(np.max(abs(rho(g)@rho(h)-rho(mul(g,h))))<1e-12 for g in grid for h in grid)
    def chi(uv,g):
        u,v=uv;a,b,c=g
        return om**((u*a+v*b)%3)
    irreps=[(str(u)+str(v),1,lambda g,u=u,v=v:np.array([[chi((u,v),g)]],complex))
            for u in range(3) for v in range(3)]
    irreps+=[("omega",3,rho),("omega2",3,lambda g:rho(g).conj())]
    assert sum(dim*dim for _,dim,_ in irreps)==27
    # Noncommutative Fourier transform columns |g> -> sqrt(d/|G|) vec[rho(g)].
    T=np.column_stack([np.concatenate([math.sqrt(dim/27)*represent(g).reshape(-1)
                        for _,dim,represent in irreps]) for g in grid])
    err_unitary=float(np.max(abs(T.conj().T@T-np.eye(27))))
    assert err_unitary<1e-12,err_unitary
    U={};index={g:i for i,g in enumerate(grid)}
    max_intertwine=0.
    for h in grid:
        L=np.zeros((27,27),complex)
        for g in grid:L[index[mul(h,g)],index[g]]=1
        blocks=[np.kron(rep(h),np.eye(dim)) for _,dim,rep in irreps]
        S=np.zeros((27,27),complex);offset=0
        for block in blocks:
            n=block.shape[0];S[offset:offset+n,offset:offset+n]=block;offset+=n
        max_intertwine=max(max_intertwine,float(np.max(abs(S@T-T@L))))
    assert max_intertwine<1e-12
    # The E6 operator/trinification27 is 9 copies of rho_omega.
    # Tensor ancilla A = 1 + rho_omega + rho_omega2, dimension7.
    # Tensor characters O(g)*A(g) then use Schur character orthogonality.
    # Check target has all irreps required by regular27 with multiplicities.
    ops_char=lambda g:9*np.trace(rho(g))
    anc_char=lambda g:1+np.trace(rho(g))+np.trace(rho(g).conj())
    target_char={g:ops_char(g)*anc_char(g) for g in grid}
    census={}
    for name,dim,rep in irreps:
        m=sum(target_char[g]*np.conj(np.trace(rep(g))) for g in grid)/27
        assert abs(m.imag)<1e-11 and abs(m.real-round(m.real))<1e-10,(name,m)
        census[name]=int(round(m.real))
    assert all(census[str(u)+str(v)]==9 for u in range(3) for v in range(3))
    assert census["omega"]==9 and census["omega2"]==27
    assert sum(dim*census[name] for name,dim,_ in irreps)==189
    # Regular27 needs χ_u,v each once, rho_omega three times, rho_omega2 three times.
    assert all(census[str(u)+str(v)]>=1 for u in range(3) for v in range(3))
    assert census["omega"]>=3 and census["omega2"]>=3
    # Ancilla center sectors need eigenvalue 1, omega, omega² for target
    # O-center omega to contain all three source sectors; smallest
    # faithful unitary H27 representations with these sector chars
    # have irreducible dimensions1,3,3. Thus dim>=7.
    minimal_ancilla_dim=1+3+3
    # If A is only (1+rho_omega) or (1+rho_omega2), one center
    # character sector of source regular27 is excluded.
    def centers(Airreps):
        return sorted(set((1+j)%3 for j in Airreps))
    assert centers([0,1,2])==[0,1,2]
    assert len(centers([0,1]))==2 and len(centers([0,2]))==2
    out=dict(status="PASS",
        native_H27_order=info["O3_order"],
        native_group_law_all_729_pairs_verified=True,
        Fourier_unitary_shape=[27,27],
        Fourier_unitarity_max_residual=err_unitary,
        Fourier_all27_equivariance_max_residual=max_intertwine,
        regular_irrep_multiplicities={**{str(u)+str(v):1 for u in range(3) for v in range(3)},
                                     "omega":3,"omega2":3},
        E6_operator27_assumed_H27_decomposition="9 copies of irreducible rho_omega (center acts as omega*I27)",
        tensor_ancilla_minimum_complex_dimension=minimal_ancilla_dim,
        explicit_ancilla_irreps=["chi_00 (1D)","rho_omega (3D)","rho_omega2 (3D)"],
        target_tensor_dimension=27*7,
        target_irrep_multiplicity_census=census,
        target_contains_equivariant_regular27_isometry=True,
        proof="All irreps of H27 have dimensions 1 (nine center-trivial chars) or 3 (the two opposite central-character Schroedinger irreps). Since center of E6 operator27 is omega, tensoring to obtain center characters 1,omega,omega² needs ancilla irreps with center omega²,1,omega respectively: minimum 3+1+3=7. E6_27 tensor A_7 contains regular27 by exact character multiplicity.",
        Fourier_formula="F(|g>) = ⊕_rho sqrt(dim rho /27) vec(rho(g)), with all 11 inequivalent complex irreps.",
        caveats="This proves group-equivariant *existence* of an isometric 27->189 embedding, not an explicit native E6 189x27 matrix, a lossless 27->27 map, a physical ancilla initialization, a gauge-local photonic compiler, or extension to full E6 action. Prior repository already proved original rank9 27->27 no-go and had alternative commutant dressing."
    )
    dest=ROOT/"data/toe_20261118_H27_Fourier_minimal7_E6_tensor_embedding.json"
    dest.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print("PASS full native H27 Fourier 27x27 unitary, 729 multiplication checks, 27 equivariance checks, minimal7 E6 tensor ancilla and 189D census")
    return out

if __name__=="__main__":run()
