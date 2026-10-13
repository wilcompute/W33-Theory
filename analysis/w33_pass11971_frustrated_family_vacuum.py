"""An explicit stable three-family CP orientation EFT, not a W33 prediction.

11924 owns triplet misalignment;11321 owns full-field degenerate CP vacua;
11967 owns the trace-alignment obstruction. Higher invariants evade that
obstruction here, at the cost of supplied spectra and EFT coefficients.
"""
from pathlib import Path
import json
import numpy as np
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
LAM=[1,2,4];DIAG=[3,4,5];PAIRS=[(0,1),(1,2),(2,0)]


def basis():
    out=[]
    for i in range(3):
        M=s.zeros(3);M[i,i]=1;out.append(M)
    for i,j in ((0,1),(0,2),(1,2)):
        M=s.zeros(3);M[i,j]=M[j,i]=1;out.append(M)
        M=s.zeros(3);M[i,j]=s.I;M[j,i]=-s.I;out.append(M)
    return out


def residuals(A,B):
    P=[]
    for i in range(3):
        j,k=[z for z in range(3) if z!=i]
        P.append((A-LAM[j]*np.eye(3))@(A-LAM[k]*np.eye(3))/((LAM[i]-LAM[j])*(LAM[i]-LAM[k])))
    return np.array([*(np.trace(np.linalg.matrix_power(A,k)).real-sum(x**k for x in LAM) for k in (1,2,3)),
                     *(np.trace(P[i]@B).real-DIAG[i] for i in range(3)),
                     *(np.trace(P[i]@B@P[j]@B).real-1 for i,j in PAIRS),
                     np.trace(P[0]@B@P[1]@B@P[2]@B).real])


def payload():
    A=s.diag(*LAM);B=s.Matrix([[3,1,-s.I],[1,4,1],[s.I,1,5]])
    P=[s.diag(*[int(j==i) for j in range(3)]) for i in range(3)]
    J=s.zeros(10,18)
    for col in range(18):
        dA=basis()[col] if col<9 else s.zeros(3)
        dB=basis()[col-9] if col>=9 else s.zeros(3)
        dP=[]
        for i in range(3):
            j,k=[z for z in range(3) if z!=i]
            dP.append((dA*(A-LAM[k]*s.eye(3))+(A-LAM[j]*s.eye(3))*dA)/((LAM[i]-LAM[j])*(LAM[i]-LAM[k])))
        values=[s.trace(k*A**(k-1)*dA) for k in (1,2,3)]
        values += [s.trace(dP[i]*B+P[i]*dB) for i in range(3)]
        values += [s.trace(dP[i]*B*P[j]*B+P[i]*dB*P[j]*B+P[i]*B*dP[j]*B+P[i]*B*P[j]*dB) for i,j in PAIRS]
        factors=[P[0],B,P[1],B,P[2],B];df=[dP[0],dB,dP[1],dB,dP[2],dB]
        values.append(sum(s.trace(s.Mul(*[df[z] if z==t else factors[z] for z in range(6)])) for t in range(6)))
        for row,z in enumerate(values):J[row,col]=s.simplify(s.re(z))
    assert J.rank()==10
    H=2*J.T*J
    assert H.rank()==10 # PSD exactly, hence8 common-conjugation zero modes.
    An=np.asarray(A,complex);Bn=np.asarray(B,complex)
    assert np.max(abs(residuals(An,Bn)))==0
    invariant=s.im(s.trace((A*B-B*A)**3));assert invariant!=0
    ev,U=np.linalg.eigh(Bn);assert min(ev)>0 and min(np.diff(ev))>0
    s13=abs(U[0,2]);s12=abs(U[0,1])/np.sqrt(1-s13*s13);s23=abs(U[1,2])/np.sqrt(1-s13*s13)
    angles=np.rad2deg(np.arcsin([s12,s23,s13]))
    quartet=float(np.imag(U[0,0]*U[1,1]*U[0,1].conjugate()*U[1,0].conjugate()))
    rng=np.random.default_rng(11971);X=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3));R,_=np.linalg.qr(X)
    covariance=float(np.max(abs(residuals(R@An@R.conj().T,R@Bn@R.conj().T))))
    assert covariance<1e-12
    evh=np.linalg.eigvalsh(np.asarray(H,float));assert sum(evh>1e-8)==10
    return dict(status='PASS',fields='Two Hermitian3x3 flavon Gram fields A,B,18 real coordinates; common U3 conjugation symmetry.',
        potential='V=sum_{k=1}^3(Tr A^k-sum lambda_i^k)^2 +sum_i(Tr P_i(A)B-d_i)^2 +sum_cyclic_ij(Tr P_i B P_j B-1)^2 +[Re Tr P0 B P1 B P2 B]^2. P_i(A)=prod_{j!=i}(A-lambda_j I)/(lambda_i-lambda_j). All real coefficients, polynomial EFT.',
        supplied_spectra_lambda=LAM,supplied_diagonal_d=DIAG,
        exact_zero='A=diag(1,2,4), B=[[3,1,-i],[1,4,1],[i,1,5]] and CP conjugate. V>=0, V=0, all18 gradients zero.',
        physical_stability='Exact residual Jacobian rank10; Hessian2 J.T J is positive semidefinite rank10. Its8-dimensional kernel is exactly the common U3 conjugation orbit: A has simple spectrum, B connects every pair, so the common stabilizer is the scalar U1. Ten physical directions have positive curvature.',
        exact_Im_trace_commutator_cubed=str(invariant),
        positive_normal_Hessian_eigenvalues=evh[8:].tolist(),
        B_eigenvalues=ev.tolist(),Yukawa_singular_ratios=np.sqrt(ev/ev[-1]).tolist(),
        unfitted_CKM_angles_deg=angles.tolist(),unfitted_J=quartet,
        covariance_residual=covariance,
        conclusion='A genuine isolated three-family CP-breaking orientation modulo the family orbit exists with competing invariants. It does not give physical quark hierarchy or small CKM angles. This falsifies sufficiency of stable generic orientation for observed flavour.',
        scope='Constructed higher-degree EFT control, not derived from W33/E6, not a Majorana model or realistic flavour vacuum. Spectral scales, diagonal targets and operator coefficients are chosen. If common U3 is global,8 physical Goldstones remain; gauging it requires anomaly cancellation and gauge-loop matching.',
        prior=['11924 Delta54 triplet misalignment','11321 full-field CP branches with doublet degeneracy','11967 orientation/counterterm audit'],
        primary='https://arxiv.org/abs/1103.2915')


if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass11971_frustrated_family_vacuum.json').write_text(json.dumps(d,indent=2)+'\n')
    print('PASS',d['exact_Im_trace_commutator_cubed'],d['unfitted_CKM_angles_deg'])
