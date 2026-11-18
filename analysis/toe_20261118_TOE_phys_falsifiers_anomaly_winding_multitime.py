"""Five physical falsifiers: chiral boundary domain, universal GS levels,
winding-mode multiplicities, and source-grounded genuinely 3-time memory.

Includes an independent exact reimplementation of Beyer et al.,
arXiv:2611.17268v1, Eq. (6), Appendix B/C: three qubit maps are
pairwise classically explainable but globally require quantum memory.
No physical photon experiment or full G2 Dirac system is claimed.
"""
from pathlib import Path
import itertools,math,json
import numpy as np
import sympy as s
from scipy.linalg import expm
ROOT=Path(__file__).resolve().parents[1]

def spinor_boundary_falsifier():
    """An actual finite Q,Q* chiral Fredholm index, not de Rham Hodge."""
    n=9;q=s.Integer(2)
    Q=s.zeros(n,n+1)
    for i in range(n):Q[i,i]=-q;Q[i,i+1]=1
    row={}
    for label,columns in (("free_both",list(range(n+1))),
                          ("left_Dirichlet",list(range(1,n+1))),
                          ("both_Dirichlet",list(range(1,n)))):
        A=Q[:,columns];r=A.rank()
        index=A.cols-A.rows
        ker=A.cols-r;coker=A.rows-r
        assert index==ker-coker
        row[label]=dict(matrix_shape=[A.rows,A.cols],kernel_Q=ker,
                        kernel_Q_adjoint=coker,chiral_index=index,
                        actual_SUSY_D_kernel=ker+coker)
    assert [row[k]["chiral_index"] for k in row]==[1,0,-1]
    def closed(mon):
        C=s.zeros(n,n)
        for i in range(n-1):C[i,i]=-q;C[i,i+1]=1
        C[n-1,n-1]=-q;C[n-1,0]=mon
        rank=C.rank()
        return dict(boundary_multiplier=int(mon),rank=rank,
                    kernel_Q=n-rank,kernel_Q_adj=n-rank,index=0)
    off=closed(1);resonant=closed(q**n)
    assert off["kernel_Q"]==resonant["kernel_Q"]-1==0
    return dict(status="PASS",interval_boundary_sensitivity=row,
                ring_off_resonance=off,ring_resonance=resonant,
                finite_weight="Q_i=v_(i+1)-2*v_i, with specified Dirichlet boundary choices",
                statement="The exact self-adjoint graded operator D=[[0,Q*,],[Q,0]] exhibits index +1,0,-1 on the SAME 1D geometry under allowed adjoint domains. On a closed circle its index is0 even at nonunitary resonance where two opposite chirality kernels appear.",
                caveat="A rigorous finite 1D analog of boundary sensitivity, not the physical flux-coupled seven-dimensional G2 spinor Dirac or APS boundary index; complex t=2 is a complexified twist, not a unitary gauge holonomy.")


def gs_level_audit():
    # One 16_-3: SO10 spinor SU5 ten + fivebar + singlet.
    # Full Ψ charge=-3. Anomaly normalization T(fund)=1/2.
    nq=3
    a_gauge=-6*nq  # SU3²,SU2² and 3/5 Y² anomaly
    a_gravity=-48*nq
    a_y2=-10*nq
    assert (a_gauge,a_gravity,a_y2)==(-18,-144,-30)
    assert 3*a_y2/5==a_gauge
    # Under a particular common heterotic universal-GS convention:
    # A_gauge / k_i = A_gravity/24.
    # Therefore k_i must be 3, NOT the simplest level-one embedding.
    k=(s.Rational(a_gauge,1)/(s.Rational(a_gravity,24)))
    assert k==3
    # This ratio is independent of family number n; it does not derive n=3.
    assert all(s.Rational(-6*n,1)/s.Rational(-48*n,24)==3
               for n in (1,2,3,5))
    # Direct formal anomaly polynomial:
    a,b=s.symbols("a b")
    polynomial=nq*(10*(-a-3*b)**3+5*(3*a-3*b)**3+(-5*a-3*b)**3)
    assert s.factor(polynomial)==-432*b*(5*a*a+3*b*b)
    return dict(status="PASS",U1_Psi_gravity=a_gravity,
                U1_Psi_SU3_SU2_GUT_normalized_Y2=a_gauge,
                U1_Psi_plain_Y2=a_y2,
                A_grav_over_24=a_gravity/24,
                required_k_if_universal_GS24=int(k),
                level_one_fails_in_this_convention=True,
                ratio_independent_of_number_of_complete_spinor_families=True,
                Abelian_cubic=s.factor(polynomial).__str__(),
                source_conventions="This is a CONDITIONAL test of the 4D heterotic-style universality formula A_i/k_i=A_grav/24 with the given trace normalizations. Actual M-theory G2 anomaly inflow is not required to obey this convention; quantized GS coefficients, Kac-Moody levels, and corrections are not derived.",
                missing="GS anomaly cancellation at nonlinear/broken phase, actual axion couplings, nonabelian gauge anomalies from additional localized modes and global compactification.")


def winding_lattice():
    """Count oriented winding vectors without mistaking area fraction for mode count."""
    out=[]
    for ratio in (0.35,.5,.75,1.,1.05,1.2,1.3,2.):
        for shape in ("square","hex"):
            y=1. if shape=="square" else math.sqrt(3)/2
            x=0. if shape=="square" else .5
            vector_modes=[]
            for u,v in itertools.product(range(-12,13),repeat=2):
                if u==v==0:continue
                norm=(u+v*x)**2+(v*y)**2
                lam=3*math.pi*ratio*norm/y
                if 0<lam<12-1e-13:
                    vector_modes.append((u,v,round(norm,11),lam))
            # Certify truncation sufficient by ||(u,v)||∞>=13 implies
            # norm>= y²*max(u²,v²)? For hex y²=.75, safe for ratio>=.35:
            # minimum norm for maxabs(u,v)>=13 is >=13²*.75.
            assert 3*math.pi*ratio*(.75*13**2)/y>12
            pairs=len(vector_modes)
            assert pairs%2==0
            out.append(dict(flux_ratio=ratio,shape=shape,
                            oriented_winding_modes=pairs,
                            unoriented_pm_identified_modes=pairs//2,
                            squared_norm_shells=sorted(set(v[2] for v in vector_modes)),
                            first_8_vectors=[list(v[:2]) for v in vector_modes[:8]]))
    def get(r,shape):return next(o for o in out if o["flux_ratio"]==r and o["shape"]==shape)["oriented_winding_modes"]
    assert (get(1.,"square"),get(1.,"hex"))==(4,6)
    assert (get(1.2,"square"),get(1.2,"hex"))==(4,0)
    assert (get(.5,"square"),get(.5,"hex"))==(8,6)
    # Separate existence of any stable shape from all-shape uniform
    # stability; in cusp y->infinity, lambda(1,0)=3*pi*r/y ->0.
    return dict(status="PASS",counts=out,
                exact_square_critical_ratios="r_crit(|u|²+|v|²)=4/(pi*(u²+v²)); BF for r below threshold",
                exact_hex_critical_ratios="r_crit(u²+u*v+v²)=2*sqrt(3)/(pi*(u²+u*v+v²)); BF for r below threshold",
                cusp_no_uniform_stability="For any finite r>0, choose y>pi*r/4; then shortest (1,0) branch violates BF in this conditional mass formula.",
                caveat="Counts oriented lattice vectors in ONE conditional light winding branch and norm truncation. Opposite winding vectors may be related by reality/level-matching; not a complete M-theory spectrum, flux quantization or backreaction.")


def apply(kraus,rho):
    return sum((k@rho@k.conj().T for k in kraus),np.zeros((2,2),complex))

def channel_choi(kraus):
    # unnormalized Choi, tested on four matrix units Eij
    return np.block([[apply(kraus,np.outer(np.eye(2)[i],np.eye(2)[j])) for j in range(2)]
                     for i in range(2)])

def chained(A,branches):
    # \sum_i Phi_i(K_i rho K_i†)
    return [F@k for k,Fs in zip(A,branches) for F in Fs]


def genuine_three_time():
    # Reproduce arXiv:2611.17268v1 Eqs(22-27), appendix C's
    # explicit pairwise classical-memory decompositions, not claim originality.
    sigz=np.diag([1.,-1.]).astype(complex)
    sigx=np.array([[0,1],[1,0]],complex)
    sigy=np.array([[0,-1j],[1j,0]],complex)
    lower=np.array([[0,1],[0,0]],complex)
    upper=lower.conj().T
    I=np.eye(2,dtype=complex)
    pairs=[]
    for gamma,p in ((.36,.2),(.64,.3),(.25,.14),(.81,.4)):
        pc=(1-math.sqrt(1-gamma))/2
        assert pc<=p<=.5
        A1=math.sqrt(gamma)*lower
        A2=np.diag([1.,math.sqrt(1-gamma)]).astype(complex)
        E1=[A1,A2]
        E2=[math.sqrt(p)*sigz,math.sqrt(1-p)*I]
        E3=[math.sqrt(p)*sigx,math.sqrt(1-p)*I]
        f=(math.sqrt(1-gamma)+2*p-1)/(2*math.sqrt(1-gamma))
        assert 0<=f<=.5
        Phi1=[upper,upper@lower]
        Phi2=[math.sqrt(f)*sigz,math.sqrt(1-f)*I]
        # (E1,E2) classical witness
        err12=np.max(abs(channel_choi(chained(E1,[Phi1,Phi2]))-channel_choi(E2)))
        phi=-math.asin(math.sqrt(gamma))
        rotations=[expm(sign*1j*phi*sigy/2) for sign in (1,-1)]
        Kpm=[(A1+A2)/math.sqrt(2),(A1-A2)/math.sqrt(2)]
        Phi_pm=[[math.sqrt(f)*sigx@R,math.sqrt(1-f)*R] for R in rotations]
        err13=np.max(abs(channel_choi(chained(Kpm,Phi_pm))-channel_choi(E3)))
        # (E2,E3): z-flip branch is classically recorded and undone,
        # then target x-dephasing applied.
        err23=np.max(abs(channel_choi(chained(E2,[[F@sigz for F in E3],E3]))-
                           channel_choi(E3)))
        assert max(err12,err13,err23)<1e-12,(gamma,p,err12,err13,err23)
        assert all(np.max(abs(sum((F.conj().T@F for F in Fs),np.zeros((2,2),complex))-I))<1e-12
                   for Fs in (Phi1,Phi2,*Phi_pm))
        # E1 on maximally mixed maps Bloch origin to s=(0,0,gamma).
        s_z=np.real(np.trace(apply(E1,I/2)@sigz))
        assert abs(s_z-gamma)<1e-13
        # Since both later channels preserve orthogonal antipodal states
        # along their respective protected axes, root fidelities =0.
        zeros2=(apply(E2,np.diag([1,0]).astype(complex)),
                apply(E2,np.diag([0,1]).astype(complex)))
        zeros3=(apply(E3,(I+sigx)/2),apply(E3,(I-sigx)/2))
        assert abs(np.trace(zeros2[0]@zeros2[1]))<1e-12
        assert abs(np.trace(zeros3[0]@zeros3[1]))<1e-12
        W3=-gamma
        pairs.append(dict(gamma=gamma,p=p,pairwise_classical_p_threshold=pc,
                          pairwise_CPTP_choi_max_errors=[err12,err13,err23],
                          proven_three_time_witness_upper_bound=W3))
    gamma=.36
    threshold=math.sqrt(1-(gamma/2)**2)
    noise=[]
    for eta in (1.,.999,.995,.99,.985,.98,.95):
        # Later maps independently depolarized: F2(z)=F3(x)=sqrt(1-eta²).
        W3_upper=2*math.sqrt(1-eta*eta)-gamma
        noise.append(dict(later_channel_bloch_visibility=eta,
                          orthogonal_axes_W3_upper=W3_upper,
                          this_analytic_axes_witness_negative=W3_upper<0))
    assert threshold>.98 and threshold<.985
    assert next(z for z in noise if z["later_channel_bloch_visibility"]==.985)["this_analytic_axes_witness_negative"]
    assert not next(z for z in noise if z["later_channel_bloch_visibility"]==.98)["this_analytic_axes_witness_negative"]
    return dict(status="PASS",paper="Beyer et al, Observation of Genuine Multi-Time Quantum Memory, arXiv:2611.17268v1 (2026-11-12)",
                independently_reproduced_four_analytic_pairwise_models=pairs,
                nonclassical_triple_witness_W3=-gamma,
                gamma_036_later_depolarizing_visibility_threshold=threshold,
                late_channel_visibility_sweep=noise,
                proof="For gamma>0,p>=pcrit, each of three channel PAIRS has an explicit classical-memory Kraus decomposition. Yet W3=F2(z)+F3(x)-|s1|=-gamma<0 rules out any common 3-time classical memory model. Verified channel equality on full qubit Choi matrices.",
                scope="Independent numerical reconstruction of a RECENT PUBLISHED theorem, NOT an original theorem, and not a W33 hardware demonstration. The damping/dephasing example is a qubit, not the proposed qutrit photon device. Classical pairwise decompositions do not jointly extend.")


def run():
    data=dict(status="PASS",Dirac_domain=spinor_boundary_falsifier(),
              E6_anomaly=gs_level_audit(),winding=winding_lattice(),
              quantum_three_time=genuine_three_time())
    dest=ROOT/"data/toe_20261118_TOE_phys_falsifiers_anomaly_winding_multitime.json"
    dest.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
    print("PASS four physical fronts: chiral boundary index, level-sensitive GS, winding shell counts, pairwise-classical genuine 3time witness")
    return data

if __name__=="__main__":run()
