"""Local strong-CP completion tests, following (not rederiving) TOE39/11947.

11950: the theta determinant divisor constrains the gauge kinetic function.
11951: exact Nelson--Barr witness and a parity-compatible SM-level EFT.
Neither is an E6 compactification, radiatively complete model or TOE.
"""
from __future__ import annotations
import hashlib
import itertools
import json
from pathlib import Path
import sys
import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_20261010_toe39_theta_parity_fifth_order as prior_theta
import w33_pass11942_hypercharge_wilson_leptons as fits


def complex_pair(z):
    return [float(np.real(z)), float(np.imag(z))]


def theta_constant(omega, alpha, beta, cutoff=14):
    n = np.arange(-cutoff, cutoff + 1, dtype=float)
    x, y = np.meshgrid(n + alpha[0], n + alpha[1], indexing="ij")
    return np.exp(1j * np.pi * (omega[0, 0]*x*x + 2*omega[0, 1]*x*y
                              + omega[1, 1]*y*y)
                  + 2j*np.pi*(x*beta[0] + y*beta[1])).sum()


def chi10_product(omega, cutoff=14):
    """Product of squares of ten even half-characteristic theta constants.

    This differs from conventional chi10 by an irrelevant nonzero constant.
    It is evaluated on Omega, not the level-three matrix 3*Omega.
    """
    value = 1.0 + 0j
    count = 0
    for a in itertools.product((0, 1), repeat=2):
        for b in itertools.product((0, 1), repeat=2):
            if sum(x*y for x, y in zip(a, b)) % 2 == 0:
                value *= theta_constant(omega, np.array(a)/2, np.array(b)/2, cutoff)**2
                count += 1
    assert count == 10
    return value


def divisor_certificate():
    cases = []
    for name, values in fits.FITS.items():
        c = np.array(values[::2]) + 1j*np.array(values[1::2])
        tau, td, eu, ed, zd = c
        moment = prior_theta.moments(tau, N=18)
        leading = (6j*np.pi)**3 * np.linalg.det(moment)**2 / 2
        assert abs(leading) > 1e-5
        radius = 0.003
        phases = np.linspace(0, 2*np.pi, 193)
        determinants = [np.linalg.det(prior_theta.theta(tau, tau, radius*np.exp(1j*p), N=18))
                        for p in phases]
        winding = (np.unwrap(np.angle(determinants))[-1]
                   - np.unwrap(np.angle(determinants))[0])/(2*np.pi)
        assert abs(winding - 3) < 1e-9
        rows = []
        for eps in (0.01, 0.005, 0.0025, 0.00125):
            omega = np.array([[tau, eps], [eps, tau]])
            det = np.linalg.det(prior_theta.theta(tau, tau, eps, N=18))
            chi = chi10_product(omega)
            chi_alt = chi10_product(omega, cutoff=20)
            assert abs(chi/chi_alt - 1) < 1e-10
            rows.append(dict(epsilon=eps,
                             determinant_over_epsilon_cubed=complex_pair(det/eps**3),
                             leading_relative_error=float(abs(det/(leading*eps**3)-1)),
                             chi10_over_epsilon_squared=complex_pair(chi/eps**2),
                             squared_divisor_cancelled_ratio=complex_pair(det**2/chi**3)))
        assert rows[-1]["leading_relative_error"] < rows[0]["leading_relative_error"]/40
        first = complex(*rows[-2]["squared_divisor_cancelled_ratio"])
        last = complex(*rows[-1]["squared_divisor_cancelled_ratio"])
        assert abs(last/first-1) < 0.01
        # Product locus is at finite Siegel-metric distance for fixed factors.
        cases.append(dict(fit=name, tau=complex_pair(tau),
                          theta_leading_coefficient=complex_pair(leading),
                          determinant_winding=winding,
                          product_locus_metric=1/(2*tau.imag**2), samples=rows))
    return dict(status="PASS", cases=cases, determinant_order=3, chi10_order=2,
                physical_combination="A=exp(-8*pi^2*f3)*det(Yu)*det(Yd), theta_bar=arg A",
                local_regular_threshold_theorem=(
                    "In a fixed physical marking, with det Yd nonzero and finite holomorphic f3, "
                    "A has a zero of order3 at epsilon=0. A nonzero holomorphic function with "
                    "real positive values on a complex open set must be constant. Therefore "
                    "the declared theta family cannot have an identically zero theta_bar on "
                    "such an open set with a regular f3 across this separating divisor."),
                required_logarithm="f3=(3/(8*pi^2))*log(epsilon)+regular, if A is nonzero constant",
                required_gauge_factor_pole_order=3,
                required_f3_monodromy="3*i/(4*pi); theta3 shifts by -6*pi",
                Igusa_candidate="f3=(3/(16*pi^2))*log(chi10)+regular removes the local order3 divisor",
                squared_branch_free_test="(det Yu)^2/(chi10)^3 has a finite generically nonzero separating limit",
                limitation=(
                    "A pole-cancelling threshold is not derived from a colored spectrum. "
                    "Cancelling a local divisor does not make A globally constant or establish "
                    "modular covariance of an unmarked Yukawa determinant. Nonconstant regular "
                    "f3 pieces, CP-breaking dilaton/gluino/Higgs phases and SUSY-breaking loops "
                    "remain. No axion-quality conclusion is superseded."),
                priority=["analysis/2026-10-10_toe39_theta_parity_fifth_order.md",
                          "analysis/PASS11947_ENTANGLING_PHASE_AXIFLAVON.md",
                          "analysis/PASS11949_AXIFLAVON_QUALITY_FAILS.md"])


def barr_realization(target):
    """Inverse construction at the decoupling limit; no optimization/fit.

    Every positive Hermitian 3x3 target H has Im H=a b^T-b a^T.
    Choose u=a+i b, S=H+u u^dagger real positive, m m^T=S.
    Then H=m(I-c c^dagger)m^T with c=m^-1 u and ||c||<1.
    B^dagger=c/sqrt(1-||c||^2), mu=1 gives the Barr Schur form.
    """
    target = np.asarray(target, complex)
    assert np.max(abs(target-target.conj().T)) < 1e-12
    assert np.linalg.eigvalsh(target)[0] > 0
    imag = target.imag
    i, j = max(itertools.combinations(range(3), 2), key=lambda pair: abs(imag[pair]))
    if abs(imag[i,j]) < 1e-15:
        return np.linalg.cholesky(target.real), np.zeros(3, complex), 1.0
    # Permute the chosen plane to positions 0/1, reducing small pivots.
    order = [i, j, next(k for k in range(3) if k not in (i,j))]
    inverse = np.argsort(order)
    h = target[np.ix_(order,order)]
    b12, b13, b23 = h.imag[0,1], h.imag[0,2], h.imag[1,2]
    scale = np.sqrt(abs(b12))
    a = scale*np.array([1., 0., -b23/b12])
    b = np.array([0., b12, b13])/scale
    u = (a+1j*b)[inverse]
    s = target + np.outer(u,u.conj())
    assert np.max(abs(s.imag)) < 1e-12
    m = np.linalg.cholesky(s.real)
    c = np.linalg.solve(m,u)
    gap = 1-float(np.vdot(c,c).real)
    assert gap > 0
    B = c.conj()/np.sqrt(gap)
    return m, B, 1.0


def light_hermitian(m, B, mu):
    u = m @ B.conj()
    return m @ m.T - np.outer(u,u.conj())/(mu**2+np.vdot(B,B).real)


def ckm_target():
    data = fits.DATA
    s13 = data["Vub"]; c13 = np.sqrt(1-s13**2)
    s12 = data["Vus"]/c13; c12=np.sqrt(1-s12**2)
    s23 = data["Vcb"]/c13; c23=np.sqrt(1-s23**2)
    delta = np.arcsin(data["J"]/(s12*s23*s13*c12*c23*c13**2))
    e = np.exp(1j*delta)
    v = np.array([[c12*c13,s12*c13,s13/e],
                  [-s12*c23-c12*s23*s13*e,c12*c23-s12*s23*s13*e,s23*c13],
                  [s12*s23-c12*c23*s13*e,-c12*s23-s12*c23*s13*e,c23*c13]])
    masses = np.array([data["md_ms"]*data["ms_mb"],data["ms_mb"],1.])
    return v, masses


def vectorlike_certificate():
    i=sp.I
    m=sp.Matrix([[1,1,0],[0,2,1],[1,0,3]])
    B=sp.Matrix([[1+i,2-i,1+2*i]])
    mu=sp.Integer(2)
    full=m.row_join(sp.zeros(3,1)).col_join(B.row_join(sp.Matrix([[mu]])))
    denom=sp.simplify(mu**2+(B*B.conjugate().T)[0])
    u=m*B.conjugate().T
    h=(m*m.T-u*u.conjugate().T/denom).applyfunc(sp.simplify)
    cp=sp.simplify(sp.im(h[0,1]*h[1,2]*h[2,0]))
    assert full.det()==14 and cp==sp.Rational(119,64)
    v, masses=ckm_target();target=(v*masses**2)@v.conj().T
    real_m, row_b, real_mu=barr_realization(target)
    regenerated=light_hermitian(real_m,row_b,real_mu)
    assert np.max(abs(regenerated-target)) < 1e-12
    ev, U=np.linalg.eigh(regenerated)
    J=float(np.imag(U[0,0]*U[1,1]*U[0,1].conj()*U[1,0].conj()))
    assert abs(abs(J)/fits.DATA["J"]-1) < 1e-6
    finite=[]
    for heavy_scale in (100.,1000.,10000.):
        mass=np.zeros((4,4),complex);mass[:3,:3]=real_m
        mass[3,:3]=heavy_scale*row_b;mass[3,3]=heavy_scale*real_mu
        left, singulars, _=np.linalg.svd(mass)
        sorted_s=singulars[-1:0:-1]
        finite.append(dict(heavy_scale=heavy_scale,
                           max_light_mass_relative_error=float(max(abs(sorted_s/masses-1))),
                           determinant_phase=float(np.angle(np.linalg.det(mass))),
                           weak_unitarity_defect=float(np.linalg.norm(
                               left[:3,1:]@left[:3,1:].conj().T-np.eye(3)))))
    assert finite[-1]["max_light_mass_relative_error"] < 1e-5
    qpsi=json.loads((ROOT/"data/w33_qpsi_matter_parity_e8_d8_bridge.json").read_text())
    assert qpsi["E6_27"]["branching"]=="27 = 16_1 + 10_-2 + 1_4"
    assert [p["count"] for p in qpsi["E6_cubic"]["patterns"]]==[40,5]
    # Chiral-superfield anomalies: multiplicity, Y, X for the new fields.
    inventory=[(3,sp.Rational(-1,3),1),(3,sp.Rational(1,3),-1),
               (1,0,-1),(1,0,-1),(1,0,1),(1,0,1)]
    anomalies={"SU3_squared_X":sp.Rational(1,2)*(1-1),
               "Y_squared_X":sum(n*y*y*x for n,y,x in inventory),
               "Y_X_squared":sum(n*y*x*x for n,y,x in inventory),
               "gravity_X":sum(n*x for n,y,x in inventory),
               "X_cubed":sum(n*x**3 for n,y,x in inventory)}
    assert all(z==0 for z in anomalies.values())
    x1,y1,x2,y2=sp.symbols("x1 y1 x2 y2",real=True)
    r1=x1*x1+y1*y1;r2=x2*x2+y2*y2
    align=(r1+r2-2)**2+(r1-r2)**2+(x1*x2+y1*y2)**2
    at={x1:1,y1:0,x2:0,y2:1}
    assert all(sp.diff(align,z).subs(at)==0 for z in (x1,y1,x2,y2))
    hessian=sp.hessian(align,(x1,y1,x2,y2)).subs(at)
    spectrum={str(k):int(v) for k,v in hessian.eigenvals().items()}
    assert sum(spectrum.values())==4 and spectrum["0"]==1
    return dict(status="PASS", exact_example=dict(
        real_light_mass=[[int(z) for z in row] for row in m.tolist()], complex_B=[str(z) for z in B], mu=2,
        full_determinant="14", light_CP_invariant="119/64",
        inverse_upper_block_sensitivity=[str(sp.simplify(z)) for z in B*m.inv()/mu]),
        inverse_construction=dict(real_m=real_m.tolist(),B=[complex_pair(z) for z in row_b],mu=real_mu,
                                  target_light_masses=masses.tolist(),J=J,
                                  matrix_reconstruction_error=float(np.max(abs(regenerated-target))),
                                  finite_heavy_checks=finite,
                                  perturbative_common_rescale=1/64,
                                  largest_rescaled_B_component=float(max(abs(row_b))/64),
                                  rescaled_mu=1/64),
        formula="M=[[m,0],[B,mu]], det M=mu det m; H_light=m m^T-m B^dagger B m^T/(mu^2+|B|^2)",
        E6_parity_obstruction=(
            "For the certified standard (-1)^Qpsi, d^c in16 is odd while D in10 is even. "
            "D d^c is odd; every product of parity-even condensates leaves it forbidden. "
            "The 27^3 mixing needs an odd16 background. Thus native10 exotics cannot carry "
            "the Barr mixing block in an unbroken standard-matter-parity vacuum, at any order. "
            "This does not apply to alternative parity assignments or vectorlike16 additions."),
        parity_compatible_SM_EFT=dict(
            X_charges={"Q":0,"d_c":0,"H_d":0,"D":1,"D_c":-1,"S1":-1,"S2":-1,"T1":1,"T2":1},
            matter_parities={"Q":-1,"d_c":-1,"H_d":1,"D":-1,"D_c":-1,"S1":1,"S2":1,"T1":1,"T2":1},
            declared_SM_fields="D=(3,1,-1/3), Dc=(bar3,1,+1/3); S,T gauge singlets",
            superpotential="Q*m*d_c*H_d+mu*D*D_c+sum_ij lambda_ij*S_i*D*d_c_j+sum c_ijkl*S_i*S_j*T_k*T_l/Lambda",
            all_order_holomorphic_zero="Q*H_d*Dc has X=-1; dressing by any nonnegative S1,S2 powers cannot neutralize it when T1=T2=0",
            anomaly_sums={k:str(z) for k,z in anomalies.items()},
            D_flat_background="xi=2, S1=1,S2=i, T1=T2=0: D_X=xi-|S1|^2-|S2|^2=0",
            declared_CP_invariant_alignment_potential="lambda_r*(|S1|^2+|S2|^2-2)^2+lambda_a*(|S1|^2-|S2|^2)^2+kappa*(Re(S1bar*S2))^2, all coefficients positive",
            alignment="S2=+/-i*S1, |S1|=|S2|=1; supplies physical relative CP phase, while the common phase is gauged",
            alignment_hessian_eigenvalues_unit_coefficients=spectrum,
            FI_boundary="Constant xi is a rigid EFT input; no gauge-invariant supergravity/string FI realization supplied",
            supersymmetric_part_boundary="D-flat background and holomorphic zero do not derive the additional alignment potential or actual SUSY breaking"),
        scope=(
            "Standard Nelson--Barr construction and inverse reconstruction, not new general mechanisms. "
            "The repo-specific connection is its compatibility gate against the stored E6 parity. "
            "The explicit anomaly-free SM-level EFT adds fields and a U1, not a certified E6/string "
            "embedding. Quark input is reconstructed, not predicted. Radiative theta, gluino phases, "
            "spectator dynamics, proton operators, leptons, neutrinos and gravity remain uncomputed."))


def certificate():
    paths=["analysis/w33_20261010_toe39_theta_parity_fifth_order.py",
           "analysis/w33_pass11942_hypercharge_wilson_leptons.py",
           "data/w33_qpsi_matter_parity_e8_d8_bridge.json"]
    return dict(schema="w33.pass11950_11951.strong_cp.v1", status="PASS",
                input_normalized_sha256={p:hashlib.sha256((ROOT/p).read_bytes().replace(b"\r\n",b"\n")).hexdigest() for p in paths},
                pass11950=divisor_certificate(),pass11951=vectorlike_certificate())


if __name__=="__main__":
    result=certificate()
    out=ROOT/"data/w33_pass11950_11951_strong_cp_divisor_and_vectorlike.json"
    out.write_text(json.dumps(result,indent=2,default=str)+"\n")
    print(json.dumps({"status":result["status"],"determinant_order":3,
                      "chi10_order":2,"exact_CP_invariant":"119/64",
                      "inverse_J":result["pass11951"]["inverse_construction"]["J"]}))
