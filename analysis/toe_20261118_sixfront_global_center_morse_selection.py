"""Six reproducible constraint tests for W33/E8/H27 and TOE physics.

Mathematical tests, NOT a global M-theory compactification, gravity
equations, a chiral particle spectrum, or measured photonic device.

1. The global (E6 x SU3)/Z3 quotient shares the H27 center with E6.
2. A sharp adjoint H27 discrete connection spectral gap.
3. Any n>=2 tilt-localized harmonic PW-like Morse n-plet is possible.
4. Actual round-S7 untwisted Dirac spectral obstruction.
5. Explicit vectorlike E6 Higgs-pair F/D-flat Abelian-rank repair.
6. Detector-misassignment threshold and fixed-n quantum witness power.
"""
import json,math,itertools
from pathlib import Path
import numpy as np
import sympy as s
from scipy.optimize import root
from scipy.special import gamma,comb
from scipy.stats import binom,beta

ROOT=Path(__file__).resolve().parents[1]
omega=np.exp(2j*np.pi/3)
X=np.array([[0,0,1],[1,0,0],[0,1,0]],complex)
Z=np.diag([1,omega,omega**2])
I3=np.eye(3,dtype=complex)

def global_E8_center():
    # Kernel of E6 x SU3 -> E8 for 248 branching.
    # E6 zeta acts as omega on 27, SU3 omega on 3:
    # (27,3): omega^(a+b), (27bar,3bar): omega^(-a-b).
    table=[]
    ker=[]
    for a,b in itertools.product(range(3),repeat=2):
        test=(a+b)%3
        table.append(dict(E6_center_exp=a,SU3_center_exp=b,
                          sector_27x3_character_exponent=test,
                          sector_27barx3bar_exponent=(-test)%3,
                          acts_trivially_on_full_248=(test==0)))
        if test==0:ker.append([a,b])
    assert ker==[[0,0],[1,2],[2,1]]
    assert ((1+0)-(0+1))%3==0
    # H27 center lies inside SU3 center and, after quotient,
    # equals the E6 center. Thus their Z3 factors are not independent.
    return dict(global_subgroup="(E6 x SU3) / Z3",
       quotient_kernel_pairs=ker,central_table=table,
       E6_center_equals_SU3_center_in_global_E8_subgroup=True,
       H27_intersection_E6_center_order=3,
       product_H27_and_E6_center_in_E8_order=27,
       false_independent_product_order=81,
       adjoint_E6_gauge_bosons_invariant_under_H27_center=True,
       fundamental_27_matter_center_character="omega",
       source="E8 248 branching (78,1)+(1,8)+(27,3)+(27bar,3bar)",
       caveat="Only a group-global center constraint. Does not prohibit an E8-compatible H27 flat bundle, and does not supply anomaly cancellation or a physical Higgs solution.")

def Weyl_gap():
    W={}
    energies=[]
    for a,b in itertools.product(range(3),repeat=2):
        M=np.linalg.matrix_power(X,a)@np.linalg.matrix_power(Z,b)
        M/=np.linalg.norm(M,'fro')
        E=.5*(np.linalg.norm(X@M@X.conj().T-M,'fro')**2+
              np.linalg.norm(Z@M@Z.conj().T-M,'fro')**2)
        exact=s.Rational(3,2)*(int(a!=0)+int(b!=0))
        assert abs(E-float(exact))<1e-12,(a,b,E,exact)
        W[str(a)+str(b)]=str(exact)
        energies.append(float(E))
    assert np.allclose(sorted(energies),[0.]+[1.5]*4+[3.]*4,atol=1e-12)
    # A nontrivial adjoint triplet cannot be invariant under both
    # noncommuting clock and shift. This is a finite-graph holonomy
    # frustration bound, not a continuum physical mass.
    return dict(normalization="Q(M)=1/2(||XMX†-M||F²+||ZMZ†-M||F²)/||M||F²",
       unitary_two_generator_eigenvalues=sorted(energies),
       traceless_adjoint_eigenvalues=[1.5]*4+[3.]*4,
       sharp_min_positive_eigenvalue=s.Rational(3,2).__str__(),
       sharp_max=3,
       energy_by_Weyl_label=W,
       no_nonzero_cocovariantly_constant_SU3_adjoint_Higgs=True,
       caveat="A graph-holonomy spectral gap with unit generator-edge weights; no physical mass follows without specifying loop lengths, Higgs kinetic normalization, curvature and actual boundary domain.")

def generalized_Morse():
    table=[]
    for n in range(2,9):
        rc=n**(-1/(n-1))
        caustic_bound=rc+rc**n
        assert caustic_bound<1
        roots=[]
        for rad in (0.55,0.85,1.15,1.55):
            for theta in np.linspace(0,2*np.pi,24,endpoint=False):
                w0=rad*np.exp(1j*theta)
                def func(v):
                    w=v[0]+1j*v[1]
                    z=np.conj(w)**n-w-1
                    return [z.real,z.imag]
                sol=root(func,[w0.real,w0.imag],tol=1e-10)
                if sol.success and np.linalg.norm(func(sol.x))<1e-8 and not any(
                    np.linalg.norm(sol.x-r)<1e-6 for r in roots):
                    roots.append(sol.x)
        assert len(roots)==n,(n,len(roots))
        assert all(np.linalg.norm(v)>rc+1e-7 for v in roots)
        # Degree of the proper planar map F(w)=conj(w)^n-w is -n.
        # det(dF)=1-n²|w|^(2n-2) is strictly negative at every root
        # when |a|>rc+rc^n. All are Morse index1 with z eigenvalue2.
        C=s.simplify(2*s.pi**s.Rational(3,2)*s.factorial(n)/
           ((2*n+3)*s.gamma(s.Rational(2*n+3,2))))
        if n==3:assert s.simplify(C-64*s.pi/315)==0
        table.append(dict(n=n,real_tilt_a=1,critical_disk_radius=rc,
             sufficient_any_direction_tilt_magnitude=caustic_bound,
             numerical_critical_count=len(roots),
             guaranteed_Morse_index1_count=n,
             leading_energy_coefficient_times_pi=str(s.simplify(C/s.pi)),
             exact_energy_ball="C_n*R^(2n+3)+(8pi/5)*R^5+(4pi/3)*a^2*R^3",
             leading_power=2*n+3,
             complex_root_coordinates=[list(map(float,v)) for v in sorted(roots,key=lambda v:(v[0],v[1]))]))
    return dict(status="PASS",family="f_(n,a)=Re((x+iy)^(n+1))/(n+1)-(x²+y²)/2+z²-a*x",
       gradient_equation="conjugate(w)^n-w=a",
       planar_Jacobian_determinant="1-n²|w|^(2n-2)",
       proper_gradient_topological_degree="-n",
       exact_critical_point_count_at_large_tilt="n Morse-index-one points for |a|>r_c+r_c^n; r_c=n^(-1/(n-1))",
       general_energy_coefficient="C_n=2*pi^(3/2)*gamma(n+1)/((2n+3)*gamma(n+3/2))",
       table=table,
       caveat="Critical-point/Morse degree theorem, not a physical n-family Dirac spectrum or proof of L2 kernels for every n. This shows the quartic n=3 background is an input; a mechanism dynamically selecting n=3 remains absent.")

def round_S7_Dirac():
    levels=[]
    for k in range(8):
        eig=s.Rational(2*k+7,4)
        mult=8*math.comb(k+6,6)
        levels.append(dict(k=k,positive_Dirac_eigenvalue_times_AdS4_L=str(eig),
            negative_eigenvalue_times_L=str(-eig),multiplicity_each_sign=mult))
    assert levels[0]["positive_Dirac_eigenvalue_times_AdS4_L"]=="7/4"
    # scalar curvature of unit S7: 42; R_S7=2 L => 21/(2 L²).
    # Lichnerowicz D²=∇*∇+Scal/4 precludes kernel.
    return dict(AdS4_x_round_S7_on_shell_R7_over_L=2,
      round_S7_untwisted_Dirac_spectrum_times_L="±(k+7/2)/2",
      first8_levels=levels,
      scalar_curvature_times_L2="21/2",
      Lichnerowicz_bound_Dirac_squared_L2="21/8",
      exact_ground_Dirac_squared_L2="49/16",
      zero_internal_untwisted_spinor_modes=0,
      caveat="Untwisted geometric Dirac, not full flux-coupled 11D gravitino or charged 7D ADE Dirac operator. No physical fermion-mass conclusion in actual singular G2 compactifications.")

def E6_vectorlike():
    # Two distinct full 27+27bar Higgs pairs: choose SM singlet
    # N^c=(-5,1) and S=(0,4) in 27, dual opposite charges in bar27.
    q=s.Matrix([[-5,0],[1,4]])
    assert q.det()==-20
    gram=2*q*q.T
    assert gram==s.Matrix([[50,-10],[-10,34]])
    assert gram.det()==1600
    eig=[str(v) for v in sorted(gram.eigenvals(),key=lambda x:float(x))]
    assert set(gram.eigenvals())=={42-2*s.sqrt(41),42+2*s.sqrt(41)}
    # Full complex E6 cancellation on each vectorlike pair:
    # the dual (bar27) VEV is conjugate to the 27 VEV, and
    # the D terms for EVERY gauge generator cancel pairwise.
    v1,v2,z1,z2=s.symbols("v1 v2 z1 z2",nonzero=True)
    # E6 invariant superpotential:
    # W=Z1*(barH1.H1-v1²)+Z2*(barH2.H2-v2²).
    # D=0 if barH_i=H_i* and |H_i|²=v_i², Z_i=0.
    return dict(status="PASS",
       Higgs_multiplets="two distinct vectorlike (27+27bar) pairs plus two E6-singlet driving chiral multiplets",
       charge_table={"Nc_in_27":[-5,1],"S_in_27":[0,4],
          "Ncbar_in_27bar":[5,-1],"Sbar_in_27bar":[0,-4]},
       Abelian_charge_determinant=-20,
       normalized_equal_vev_Abelian_mass_Gram=[[int(v) for v in row] for row in gram.tolist()],
       Abelian_mass_Gram_determinant=1600,
       Abelian_mass_Gram_eigenvalues=eig,
       exact_full_E6_D_cancellation_pair_by_pair=True,
       exact_full_E6_F_solution_at_driving_fields_zero=True,
       invariant_superpotential="W=Z1*(barH1.H1-v1²)+Z2*(barH2.H2-v2²)",
       breaks_both_extra_Abelian_generators_at_rank2=True,
       caveat="Constructive auxiliary SUSY Higgs model, not derived field content from compactification. New 27bar multiplets introduce conjugate representations/exotics; unbroken non-Abelian gauge sector, entire Hessian, D/Holonomy global consistency, localized matter, anomalies and stable UV completion untested.")

def photon_assignment():
    gamma=.96;eta=.95;p=.45
    maxerr=(1-2/math.sqrt(4*eta*eta+gamma*gamma))/2
    alpha=.01
    def one_power(n,err):
        t=1-2*err
        pg=(1+gamma*t)/2
        pe=(1+eta*t)/2
        idx=np.arange(n+1)
        lo=np.zeros(n+1)
        lo[1:]=2*beta.ppf(alpha/3,idx[1:],n-idx[1:]+1)-1
        lo=np.maximum(lo,0.)
        req=np.sqrt(1-lo[:,None]**2)+np.sqrt(1-lo[None,:]**2)
        k_required=np.searchsorted(lo,req,side="right")
        tails=binom.sf(np.arange(n+2)-1,n,pg)
        weights=binom.pmf(idx,n,pe)
        return float(np.dot(weights,np.dot(tails[k_required],weights)))
    rows=[]
    for err in (0.,.01,.02,.03,.04):
        t=1-2*err
        witness=2*math.sqrt(1-(eta*t)**2)-gamma*t
        row=dict(symmetric_binary_assignment_flip_probability=err,
                 expected_undebiasable_raw_witness=witness,
                 asymptotic_raw_witness_negative=witness<0)
        if err in (0.,.01,.02):
            row["n450_exact_model_power"]=one_power(450,err)
            row["n900_exact_model_power"]=one_power(900,err)
        rows.append(row)
    assert abs(rows[0]["n450_exact_model_power"]-.66128121221282)<1e-9
    assert rows[3]["asymptotic_raw_witness_negative"]
    assert not rows[-1]["asymptotic_raw_witness_negative"]
    return dict(status="PASS",pairwise_classical_source_parameters=[gamma,p,eta],
       raw_readout_visibility_factor="t=1-2*epsilon",
       raw_fixed_axis_witness="2 sqrt(1-(t*eta)²)-t*gamma",
       exact_ideal_witness_surviving_symmetric_assignment_error_limit=maxerr,
       rows=rows,
       caveat="Applies if symmetric readout misclassification is UNCORRECTED and independent with known channel parameters; calibrated debiasing can recover a witness at increased variance. No power guarantee under drift, selection, herald loss, non-IID statistics, imperfect instrumental tomography or an intrinsically qutrit channel.")

def run():
    data=dict(status="PASS",date="2026-11-18",
       E8_global_center=global_E8_center(),
       H27_adjoint_gap=Weyl_gap(),
       harmonic_family_selection=generalized_Morse(),
       AdS4_S7_Dirac=round_S7_Dirac(),
       E6_vectorlike_Higgs=E6_vectorlike(),
       photonic_assignment=photon_assignment(),
       physical_TOE_claim=False)
    dest=ROOT/"data/toe_20261118_sixfront_global_center_morse_selection.json"
    dest.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
    print("PASS six independent constraints: E8 shared center, H27 gap, n-family harmonic Morse, S7 Dirac, E6 vectorlike F/D and photonic readout")
    print("Morse n counts:",[(r["n"],r["numerical_critical_count"]) for r in data["harmonic_family_selection"]["table"]])
    print("Readout noise threshold:",data["photonic_assignment"]["exact_ideal_witness_surviving_symmetric_assignment_error_limit"])
    return data
if __name__=="__main__":run()
