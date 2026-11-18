"""Explicit 189x27 isometric intertwiner for the native W33 H27 torsor.

Construct in coordinates certified in toe_20261118_H27_Fourier_minimal7_E6_tensor_embedding.
Target is nine copies of the 3D H27 Schroedinger representation, tensored
with A7=1+rho+conj(rho). Group-average a seeded dense trial map, then
normalize its positive Gram to an exact-in-the-limit equivariant isometry.

This is a numeric reproducible H27 representation-level compiler,
not a full E6 gauge-equivariant physical map or a circuit.
"""
import math,hashlib,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
om=np.exp(2j*np.pi/3)
X=np.array([[0,0,1],[1,0,0],[0,1,0]],complex)
Z=np.diag([1,om,om**2])
Y=Z@Z
G=[(a,b,c) for a in range(3) for b in range(3) for c in range(3)]
I27=np.eye(27,dtype=complex)
def mul(g,h):
    a,b,c=g;A,B,C=h
    return ((a+A)%3,(b+B)%3,(c+C-b*A)%3)
def rho(g):
    a,b,c=g
    return om**c * np.linalg.matrix_power(X,a) @ np.linalg.matrix_power(Y,b)
def anc(g):
    R=rho(g)
    M=np.zeros((7,7),complex)
    M[0,0]=1
    M[1:4,1:4]=R
    M[4:7,4:7]=R.conj()
    return M
def run():
    ix={g:i for i,g in enumerate(G)}
    rng=np.random.default_rng(20261118)
    S=rng.normal(size=(189,27))+1j*rng.normal(size=(189,27))
    S/=np.sqrt(2*189)
    T=np.zeros_like(S)
    full=[]
    for h in G:
        L=np.zeros((27,27),complex)
        for g in G:L[ix[mul(h,g)],ix[g]]=1
        O=np.kron(np.eye(9),rho(h))
        Q=np.kron(O,anc(h))
        full.append((L,Q))
        T+=Q@S@L.conj().T/27
    gram=T.conj().T@T
    ev,V=np.linalg.eigh(gram)
    assert ev.min()>1e-6,ev
    invroot=(V*(ev**(-.5)))@V.conj().T
    E=T@invroot
    uniterr=float(np.max(abs(E.conj().T@E-I27)))
    equivarerr=float(max(np.max(abs(Q@E-E@L)) for L,Q in full))
    assert uniterr<3e-12 and equivarerr<3e-12,(uniterr,equivarerr)
    center=(0,0,1)
    Lc,Qc=full[ix[center]]
    assert np.max(abs(Qc@E-E@Lc))<3e-12
    # center charge sector of source 27 has dimension 9 each; target
    # center character labels by anc 1, rho, rho-bar (since O char ω).
    # Corresponding anc subspaces target have dimensions 27,81,81.
    proj_an=[np.diag([1]+[0]*6),np.diag([0]+[1]*3+[0]*3),
             np.diag([0]*4+[1]*3)]
    weights=[np.diag(E.conj().T@np.kron(np.eye(27),P)@E).real
             for P in proj_an]
    assert all(np.max(abs(w-1/3))<3e-12 for w in weights)
    # A hypothetical equivariant map with a fixed invariant ancilla
    # must land exclusively in the anc-trivial sector, rank <=9.
    reduced=np.kron(np.eye(27),proj_an[0])@E
    sv=np.linalg.svd(reduced,compute_uv=False)
    rank=int(np.count_nonzero(sv>1e-9))
    assert rank==9
    # reproducible hash of the 189x27 complex entries without storing
    # large git blobs. Full matrix reconstructed from seed and code.
    blob=np.ascontiguousarray(E).view(np.uint8).tobytes()
    out=dict(status="PASS",seed=20261118,source_dim=27,target_dim=189,
        trial_intertwiner_min_Gram_eigenvalue=float(ev.min()),
        trial_intertwiner_max_Gram_eigenvalue=float(ev.max()),
        explicit_189x27_isometry_unitarity_max_error=uniterr,
        explicit_intertwiner_all27_max_error=equivarerr,
        encoded_basis_states_ancilla_sector_probabilities=[float(w[0]) for w in weights],
        all27_basis_states_have_equal_sector_weights=True,
        invariant_ancilla_restricted_encoder_rank=rank,
        matrix_sha256=hashlib.sha256(blob).hexdigest(),
        construction="seeded complex Gaussian 189x27 T0; H Reynolds projection T=sum(U(h)T0 L(h)^dagger)/27; isometry E=T(T^dagger T)^-1/2; all 27 group actions verified",
        note="This concretely provides a group-equivariant isometric 189x27 matrix, improving prior existence proof. Fixed trivially transforming ancilla cannot implement it as E6 27->27; nontrivial ancilla charge sectors are populated in EVERY encoded address basis vector. No physical unitary circuit, charge/hypercharge/Yukawa extension to full E6, or Lorentzian spacetime.")
    dest=ROOT/"data/toe_20261118_H27_explicit189_intertwiner_reynolds.json"
    dest.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print("PASS native H27 explicit 189x27 isometry errors",uniterr,equivarerr,"sector 1/3 each, invariant anc rank9")
    return out
if __name__=="__main__":run()
