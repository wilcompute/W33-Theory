"""An anomaly-free cubic SU(3) supersymmetric completion of a nine-qutrit SIC.

Constructive EFT field content: Q_i (9 fundamentals), P_i (9 antifundamentals),
X (one fundamental), Y (one antifundamental), 45 meson singlets S_ij, T.
All 10 fundamentals and 10 antifundamentals cancel perturbative SU(3)^3.
This is deliberately engineered; not a physical E8/SM UV compactification.

W = sum_{(i,j) in CROSS} S_ij (P_i Q_j - C_ij)
    + X.Y + epsilon(X,Q_0,Q_1) + T (Y.Q_3 - beta).
All terms have field degree at most three; constants C, beta have dimensions.
"""
from itertools import combinations
from pathlib import Path
import json
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
I = (0, 1, 3)
CROSS = [(i,j) for i in range(9) for j in range(9) if i in I or j in I]
assert len(CROSS) == 45

def orbit(omega):
    v=np.array([0,1,-1], dtype=complex)
    return np.column_stack([
        np.roll(v*np.array([1,omega**b,omega**(2*b)]),a)
        for a in range(3) for b in range(3)
    ])

def numeric_certificate():
    omega=np.exp(2j*np.pi/3)
    Q=orbit(omega)
    H=np.diag([1/np.sqrt(2),1,1])
    P=Q.conj().T @ H
    X=np.zeros(3,complex)
    Y=-np.cross(Q[:,I[0]],Q[:,I[1]])
    beta=Y @ Q[:,I[2]]
    C=P @ Q
    B=np.linalg.det(Q[:,I])
    assert np.max(np.abs(Q@Q.conj().T-6*np.eye(3)))<1e-12
    assert np.max(np.abs(P.conj().T@P-np.diag([3,6,6])))<1e-12
    assert abs(np.vdot(Y,Y)-3)<1e-12
    assert abs(beta+B)<1e-12
    assert abs(B)>1
    D=Q@Q.conj().T+np.outer(X,X.conj())-P.conj().T@P-np.outer(Y.conj(),Y)
    assert np.max(np.abs(D))<1e-12
    pair=[abs(np.vdot(Q[:,a],Q[:,b]))**2 for a,b in combinations(range(9),2)]
    assert max(abs(v-1) for v in pair)<1e-12

    # Gauge invariant holomorphic constraints: 45 meson coordinates + 1 baryon.
    J=np.zeros((46,54),complex)
    for alpha,(i,j) in enumerate(CROSS):
        for c in range(3):
            J[alpha,3*j+c]=P[i,c]
            J[alpha,27+3*i+c]=Q[c,j]
    # epsilon derivative of det(Q_i,Q_j,Q_k).
    grad=[np.cross(Q[:,I[1]],Q[:,I[2]]),
          np.cross(Q[:,I[2]],Q[:,I[0]]),
          np.cross(Q[:,I[0]],Q[:,I[1]])]
    for j,v in zip(I,grad):
        J[45,3*j:3*j+3]=v
    rank=int(np.linalg.matrix_rank(J,tol=1e-9))
    assert rank==46
    pivotdet=np.linalg.det(C[np.ix_(I,I)])
    assert abs(pivotdet)>1e-8
    # 106 chiral components: 27 Q, 27 P, 3 X, 3 Y, 45 S, 1 T.
    Hess=np.zeros((106,106),complex)
    def add(i,j,z):
        Hess[i,j]+=z
        Hess[j,i]+=z
    for alpha,(i,j) in enumerate(CROSS):
        for c in range(3):
            add(60+alpha,3*j+c,P[i,c])
            add(60+alpha,27+3*i+c,Q[c,j])
    for c in range(3):
        add(54+c,57+c,1)
        add(105,57+c,Q[c,I[2]])
        add(105,3*I[2]+c,Y[c])
        for d in range(3):
            e=np.eye(3)[:,d]
            add(54+c,3*I[0]+d,np.cross(e,Q[:,I[1]])[c])
            add(54+c,3*I[1]+d,np.cross(Q[:,I[0]],e)[c])
    hrank=int(np.linalg.matrix_rank(Hess,tol=1e-8))
    assert hrank==98
    # Identify all 8 Hessian null vectors explicitly with sl(3,C) gauge tangents.
    algebra=[]
    for a in range(3):
        for b in range(3):
            if a!=b:
                G=np.zeros((3,3));G[a,b]=1;algebra.append(G)
    for a,b in ((0,1),(1,2)):
        G=np.zeros((3,3));G[a,a]=1;G[b,b]=-1;algebra.append(G)
    tangents=[]
    for G in algebra:
        tangent=np.zeros(106,complex)
        tangent[:27]=(G@Q).reshape(27,order='F')
        tangent[27:54]=(-P@G).reshape(27)
        tangent[57:60]=-Y@G
        assert np.linalg.norm(Hess@tangent)<1e-10
        tangents.append(tangent)
    assert np.linalg.matrix_rank(np.column_stack(tangents))==8
    # F_S = P_i Q_j - C_ij; F_T = Y Q_3 - beta;
    # F_X = Y+Q_0 x Q_1; F_Y = X+T Q_3;
    # F_Q,F_P vanish because S=T=X=0.
    assert np.max(np.abs([C[i,j]-(P@Q)[i,j] for i,j in CROSS]))<1e-12
    assert np.max(np.abs(Y+np.cross(Q[:,I[0]],Q[:,I[1]])))<1e-12
    return {
        "number_of_Q_fundamentals":9,"number_of_P_antifundamentals":9,
        "total_fundamental_count":10,"total_antifundamental_count":10,
        "one_loop_SU3_beta_coefficient_3Nc_minus_Nf":-1,
        "perturbatively_asymptotically_free":False,
        "gauge_singlet_count":46,"complex_chiral_components":106,
        "meson_coordinate_count":45,"baryon_coordinate_count":1,
        "holomorphic_constraint_rank":rank,"superpotential_hessian_rank":hrank,
        "complex_gauge_orbit_nullity":106-hrank,
        "max_D_matrix_residual":float(np.max(np.abs(D))),
        "min_45x45_meson_coordinate_pivot_determinant_abs":float(abs(pivotdet)),
        "baryon_value_imaginary":float(B.imag),"beta_imaginary":float(beta.imag),
        "smallest_nonzero_hessian_singular_value":float(np.linalg.svd(Hess,compute_uv=False)[97]),
        "max_SIC_pair_overlap_squared_error":float(max(abs(v-1) for v in pair)),
    }

def rank_modp(rows,p):
    piv={}
    for row in rows:
        r=[int(x)%p for x in row]
        for k in sorted(piv):
            f=r[k]
            if f:
                r=[(a-f*b)%p for a,b in zip(r,piv[k])]
        nz=next((k for k,v in enumerate(r) if v),None)
        if nz is not None:
            inv=pow(r[nz],-1,p)
            piv[nz]=[(t*inv)%p for t in r]
    return len(piv)

def exact_mod7_certificate():
    # Prime 7 splits the Q(omega) number field, omega -> 2, conjugate -> 4.
    w,p=2,7
    v=np.array([0,1,-1],dtype=int)%p
    cols=lambda root: np.column_stack([
        np.roll((v*np.array([1,pow(root,b,p),pow(root,2*b,p)]))%p,a)
        for a in range(3) for b in range(3)
    ])%p
    Q=cols(w)
    # sqrt(1/2)=2 mod 7. The companion (conjugate) embedding uses omega->4.
    P=(cols(4).T @ np.diag([2,1,1]))%p
    meson=(P@Q)%p
    J=[]
    for i,j in CROSS:
        row=[0]*54
        for c in range(3):
            row[3*j+c]=int(P[i,c])
            row[27+3*i+c]=int(Q[c,j])
        J.append(row)
    # cofactor derivatives in finite characteristic (avoid numerical determinants).
    def cross(u,v):
        return np.cross(u,v)%p
    grad=[cross(Q[:,I[1]],Q[:,I[2]]),
          cross(Q[:,I[2]],Q[:,I[0]]),
          cross(Q[:,I[0]],Q[:,I[1]])]
    last=[0]*54
    for j,g in zip(I,grad):
        for c in range(3):
            last[3*j+c]=int(g[c])
    assert rank_modp(J,p)==45
    assert rank_modp(J+[last],p)==46
    assert int(round(np.linalg.det(meson[np.ix_(I,I)])))%p != 0
    return {"field":"F_7","omega_image":w,"omega_conjugate_image":4,
            "meson_jacobian_rank":45,"meson_plus_baryon_rank":46,
            "meson_pivot_det_mod7":int(round(np.linalg.det(meson[np.ix_(I,I)])))%p}

def main():
    out={"numeric":numeric_certificate(),"exact_finite_field":exact_mod7_certificate(),
         "global_uniqueness_argument":"For rank-3 M=PQ, 45 cross entries (three rows union three columns) determine all 81 meson entries by M_AB=M_AI M_JI^(-1) M_JB, on the chart det M_JI != 0. All full-rank (P,Q) factorizations of fixed M differ by G in GL(3,C). Fixing nonzero det(Q_0,Q_1,Q_3) sets det G=1, so exactly one SL(3,C) orbit. The displayed D-flat representative is its unique SU(3) orbit by Kempf-Ness. F_Q,F_P enforce singlet multipliers zero by rank 46; massive X,Y can be eliminated. Thus local physical Hessian has full rank 98.",
         "limitations":"Highly tuned flavor-dependent constants, 46 singlets; SU3 fully Higgsed, not SM color. Nf=10 vectorlike flavors gives 3Nc-Nf=-1: one-loop gauge beta is IR-free, NOT asymptotically free, so renormalizability is not proof of UV completion to arbitrarily high energies. No naturally selected E8 vacuum, SM phenomenology, physical compactification, or quantum stability claim."}
    p=ROOT/"data"/"toe_20261118_susy_sic_uv_completion.json"
    p.write_text(json.dumps(out,indent=2)+"\n",encoding="utf8")
    print("PASS UV SIC: 45 meson + 1 baryon exact rank; D/F=0; anomaly-free; Hessian 98/106")
    print(json.dumps(out["numeric"],indent=2))
    print(json.dumps(out["exact_finite_field"],indent=2))
    print(p)
    return out

if __name__=="__main__":
    main()
