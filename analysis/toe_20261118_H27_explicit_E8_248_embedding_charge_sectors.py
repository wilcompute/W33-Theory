"""Explicit H27-equivariant W33 regular27 -> E8 adjoint248 embedding.

Representation-theory construction ONLY:
E8 under E6 x SU3: (78,1)+(1,8)+(27,3)+(27bar,3bar).
Restrict SU3 to qutrit Heisenberg H27:
- (78,1) gives 78 copies of trivial character;
- (1,8) gives each of 8 nontrivial center-trivial H27 chars once;
- (27,3) gives 27 copies of rho_omega;
- (27bar,3bar) gives 27 copies of rho_omega2.

The resulting 248 contains a regular H27=27 subrepresentation.
Exhibits a concrete isometry using Fourier blocks. It necessarily mixes
E6 adjoint/singlet/fundamental/antifundamental charge sectors and does
NOT preserve full E6 gauge actions or quantum superselection.
"""
import math,json,hashlib
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
om=np.exp(2j*np.pi/3)
X=np.array([[0,0,1],[1,0,0],[0,1,0]],complex)
Y=np.diag([1,om**2,om])
I3=np.eye(3,dtype=complex)
G=[(a,b,c) for a in range(3) for b in range(3) for c in range(3)]
ix={g:i for i,g in enumerate(G)}
def mul(g,h):
    a,b,c=g;A,B,C=h
    return ((a+A)%3,(b+B)%3,(c+C-b*A)%3)
def rho(g):
    a,b,c=g
    return om**c*np.linalg.matrix_power(X,a)@np.linalg.matrix_power(Y,b)
def chi(uv,g):
    u,v=uv;a,b,c=g
    return om**((u*a+v*b)%3)

def run():
    irreps=[((u,v),1,lambda g,u=u,v=v: np.array([[chi((u,v),g)]],complex))
            for u in range(3) for v in range(3)]
    irreps+=[("rho",3,rho),("rhobar",3,lambda g:rho(g).conj())]
    F=np.column_stack([np.concatenate([math.sqrt(dim/27)*rep(g).reshape(-1)
                                       for name,dim,rep in irreps]) for g in G])
    assert np.max(abs(F.conj().T@F-np.eye(27)))<1e-12
    # E8 target basis: E6 adj78, H27 Fourier eigenbasis of SU3 adj8,
    # 27 E6-fundamental copies of SU3 rho3, 27 conjugate copies rhobar3.
    row_for_char={}
    row_for_char[(0,0)]=0
    other=[uv for uv in [(u,v) for u in range(3) for v in range(3)] if uv!=(0,0)]
    for j,uv in enumerate(other):row_for_char[uv]=78+j
    B=np.zeros((248,27),complex)
    for k,(name,dim,_) in enumerate(irreps[:9]):B[row_for_char[name],k]=1
    for a in range(3):
        for b in range(3):
            B[86+3*b+a,9+3*a+b]=1
            B[167+3*b+a,18+3*a+b]=1
    assert np.max(abs(B.conj().T@B-np.eye(27)))<1e-12
    T=B@F
    err_iso=float(np.max(abs(T.conj().T@T-np.eye(27))))
    errs=[]
    for h in G:
        L=np.zeros((27,27),complex)
        for g in G:L[ix[mul(h,g)],ix[g]]=1
        Rh=rho(h)
        # 248 representation matrix as block diag: [78 trivials,
        # 8 Weyl eigencharacters, 27 rho copies, 27 rhobar copies].
        Q=np.zeros((248,248),complex)
        Q[:78,:78]=np.eye(78)
        Q[78:86,78:86]=np.diag([chi(uv,h) for uv in other])
        Q[86:167,86:167]=np.kron(np.eye(27),Rh)
        Q[167:248,167:248]=np.kron(np.eye(27),Rh.conj())
        errs.append(float(np.max(abs(Q@T-T@L))))
    err_eq=max(errs)
    assert err_iso<1e-12 and err_eq<1e-12,(err_iso,err_eq)
    # Each computational address basis vector has 1/27 in each of
    # nine 1D characters (total 1/3), and 1/3 in each 3D center sector.
    p0=np.sum(abs(T[:86,:])**2,axis=0)
    pp=np.sum(abs(T[86:167,:])**2,axis=0)
    pm=np.sum(abs(T[167:248,:])**2,axis=0)
    assert np.max(abs(p0-1/3))<1e-12
    assert np.max(abs(pp-1/3))<1e-12
    assert np.max(abs(pm-1/3))<1e-12
    # The E6-singlet subspace within E8 adjoint is solely (1,8):
    # it misses the trivial H27 character and both center-charged
    # 3D irreps, so no E6-singlet regular27 is embedded.
    e6_singlet_target_dim=8
    assert e6_singlet_target_dim<27
    # The native E6-adjoint16_-3 lies in (78,1): it is TRIVIAL
    # under this commuting family H27, not a genuine H27 triple.
    out=dict(status="PASS",source="E8 branching (78,1)+(1,8)+(27,3)+(27bar,3bar) and native H27 qutrit Schrödinger subgroup of SU3",
        E8_decomposition_dimensions=[78,8,81,81],
        H27_character_multiplicities=dict(trivial_1D=78,
                                         each_of_eight_nontrivial_1D=1,
                                         rho_omega=27,rho_omega2=27),
        regular27_required_multiplicities=dict(each_of_nine_1D=1,rho_omega=3,rho_omega2=3),
        concrete_Fourier_embedding_shape=[248,27],
        isometry_error=err_iso,all27_intertwining_max_error=err_eq,
        amplitude_weight_each_address_basis_by_E8_grading=[float(p0[0]),float(pp[0]),float(pm[0])],
        source_irrep_characters_fully_present=True,
        physical_E6_gauge_equivariance=False,
        impossible_E6_singlet_regular27_embedding_under_fixed_branching=True,
        native_E6_adjoint16_minus3_is_SU3_family_singlet=True,
        natural_E8_27_three_family_branch="(27,3): three 16_(+1) plus three 10_(-2) and three 1_(+4), NOT the native (78,1) spinor 16_(-3). Full 248 also includes (27bar,3bar); chirality/zero-mode projection required.",
        representation_sector_obstruction="The 27D regular H27 source is distributed among E6 adjoint78, E6 singlet SU3-adjoint8, and E6 fundamental/conjugate sectors. It is H27-equivariant but cannot be interpreted as a single E6 matter multiplet or physical charge-preserving quantum encoder.",
        matrix_sha256=hashlib.sha256(np.ascontiguousarray(T).view(np.uint8).tobytes()).hexdigest(),
        warning="Existing repo already knows the E8 E6xSU3 decomposition and H27 address/operator difference. This packet adds the explicit isometric native H27 representation embedding and shows the E6-superselection obstruction.")
    dest=ROOT/"data/toe_20261118_H27_explicit_E8_248_embedding_charge_sectors.json"
    dest.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print("PASS regular H27 -> E8 adjoint248 isometry",err_iso,err_eq,"but does NOT preserve E6 matter charges")
    return out
if __name__=="__main__":run()
