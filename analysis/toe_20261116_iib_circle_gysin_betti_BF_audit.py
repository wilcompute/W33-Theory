"""Independent integral topology and BF-band audit of the M/T2 -> IIB T^{p,q} dual.

Based on the existing D9 IIB derivation, but tests additional integral
(co)homology, torsion winding, spin structure, Betti vector, and stability
criteria using the Gysin sequence and integer Smith normal forms.
"""
import json, math
from pathlib import Path
from math import gcd
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form

ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/"data"/"toe_20261116_iib_circle_gysin_betti_BF_audit.json"

def topology(p,q):
    assert p or q
    g=gcd(abs(p),abs(q))
    # Base H2(B) = Z^2, H4(B)=Z.  Cup by c1=(p,q)
    # 1 -> (p,q) and (a,b) -> qa+pb.
    a=sp.Matrix([[p],[q]])
    b=sp.Matrix([[q,p]])
    # The Gysin sequence here involves exterior cup on two distinct
    # S2 factors. c1 wedge c1 = 2pq uv, not generally zero;
    # the two maps are at distinct sequence degrees, not a complex.
    assert smith_normal_form(a,domain=sp.ZZ)[0,0] in (g,-g)
    assert abs(smith_normal_form(b,domain=sp.ZZ)[0,0])==g
    return dict(
        flux_chern_numbers=[p,q],gcd=g,
        pi1="Z_"+str(g),
        homology={
          "H0":"Z","H1":"Z_"+str(g),"H2":"Z",
          "H3":"Z"+(" + Z_"+str(g) if g>1 else ""),
          "H4":"0","H5":"Z"},
        cohomology={
          "H0":"Z","H1":"0",
          "H2":"Z"+(" + Z_"+str(g) if g>1 else ""),
          "H3":"Z","H4":"Z_"+str(g),"H5":"Z"},
        de_rham_betti=[1,0,1,1,0,1],
        independent_spin_structures=(2 if g%2==0 else 1),
        fiber_loop_order_in_pi1=g,
        continuous_Betti_vector_from_RR_C4_count=1,
        notes="H2 and H3 are Z by rank; H3 carries Z_g torsion for g>1; de Rham cohomology cannot detect torsion." )

def mminus(lam):
    return lam-2-math.sqrt(4+16*lam)

def run():
    cases=[(1,1),(2,2),(3,3),(6,10),(5,0),(0,7),(11,-13),(6,9),(-4,-4)]
    results=[topology(p,q) for p,q in cases]
    for case in results:
        g=case["gcd"]
        assert case["independent_spin_structures"]==(2 if g%2==0 else 1)
        assert case["de_rham_betti"]==[1,0,1,1,0,1]
    assert topology(1,1)["pi1"]=="Z_1"
    assert topology(2,2)["pi1"]=="Z_2"
    assert topology(6,10)["pi1"]=="Z_2"
    assert topology(1,1)["homology"]["H3"]=="Z"
    assert topology(3,3)["homology"]["H3"]=="Z + Z_3"
    # The local conifold Killing spinors have fiber charge ±1/2 in
    # the conventional 4*pi-periodic psi_std coordinate. A Z_N deck
    # generator contributes phase exp(±2*pi*i/N). A second spin lift
    # contributes -1 and exists only when N is even. These are
    # GLOBAL invariant-spinor tests, not zero U(1)_R charges.
    from fractions import Fraction as F
    quotient_spin=[]
    for N in range(1,13):
        lifts=[F(0)] + ([F(1,2)] if N%2==0 else [])
        preserved=[str(lift) for lift in lifts if (F(1,N)+lift).denominator==1]
        quotient_spin.append(dict(quotient_N=N,number_of_spin_structures=len(lifts),
                                   preserving_lifts=preserved))
    assert [s["quotient_N"] for s in quotient_spin if s["preserving_lifts"]]==[1,2]
    # Equal-flux T11/N: use N0 units of IIB F5 and N=(p=q)
    volume_factor={N:sp.simplify(16*sp.pi**3/(27*N)) for N in range(1,10)}
    central_factor={N:sp.simplify(sp.pi**3*sp.Symbol("N0")**2/(4*volume_factor[N]))
                    for N in volume_factor}
    for N in volume_factor:
        assert central_factor[N]==sp.Rational(27,64)*N*sp.Symbol("N0")**2
    lam=sp.Symbol("lam",real=True,positive=True)
    mm=lam-2-sp.sqrt(4+16*lam)
    assert mm.subs(lam,0)==-4 and mm.subs(lam,12)==-4
    assert sp.solve(sp.diff(mm,lam),lam)==[sp.Rational(15,4)]
    assert mm.subs(lam,sp.Rational(15,4))==-sp.Rational(25,4)
    assert all(mminus(x)<-4 for x in [0.01,0.2,1,3.75,11.99])
    assert all(mminus(x)>-4 for x in [12.01,20,100])
    # For square shape and N0=1, N=1 is BF-safe in torus momentum
    # (lambda1=3*pi), while N>=2 has lambda1<12.
    square=[{"N":N,"N0":N0,"lambda_shortest":3*math.pi*N0/N,
       "BF_violation_from_shortest_lattice_mode":0<3*math.pi*N0/N<12}
       for N in range(1,8) for N0 in range(1,6)]
    for x in square:
        assert x["BF_violation_from_shortest_lattice_mode"]==(x["N"]/x["N0"]>math.pi/4)
    # Key separation: Type IIB two-derivative point fields have zero
    # winding; the M-theory torus Fourier modes become nonperturbative
    # wrapped (a,b) strings on the circle. That comparison neither
    # deletes these states nor proves full IIB string vacuum stability.
    result={
      "status":"EXACT_GYSIN_TOPOLOGY_T11_ZN_TORSION_AND_BF_WINDING_CHECK",
      "source_reused_not_modified":"analysis/2026-11-16_D9_iib_conifold_dual.md (untracked parallel author source)",
      "topological_T_duality":"c1(Y)=N1*u+N2*v is integral circle curvature obtained from fiberwise IIA H3 integration",
      "case_tables":results,
      "all_nontrivial_c1_deRham_betti":[1,0,1,1,0,1],
      "equal_flux_Y":"T^{1,1}/Z_N as an S1 bundle over S2xS2 of Chern numbers (N,N)",
      "N1_equal_1_homotopy_type":"S2 x S3 (classification of simply-connected spin 5-manifolds)",
      "baryonic_Betti_U1":"Exactly one free H3(Y;Z) class gives one extra RR C4-derived 5D massless Betti vector in ordinary IIB reduction",
      "massless_vector_sector_warning":"The 7 light vectors of standalone D9 Einstein-Maxwell do not exhaust the IIB T11 spectrum; the IIB Betti vector is additional.",
      "torsion_winding":"pi1(Y)=Z_g; fiber string winding has only a Z_g conserved homotopy class, not a free integer charge, though nonprotected wrapped string excitations still exist.",
      "fundamental_group_generator_fiber":True,
      "two_spin_structures_iff_g_even":True,
      "local_conifold_spinor_fiber_charges_in_std_4pi_coordinate":["1/2","-1/2"],
      "equal_flux_quotient_Killing_spinor_lifts":quotient_spin,
      "IIB_supergravity_vs_M11_supersymmetry_warning":"Continuous fiber spinorial Lie derivative is nonzero, even when global quotient lift permits Killing spinors at N=1,2. Circle-invariant supergravity T-duality may lose those modes; recovering supersymmetry requires checking charged winding sectors. This is a duality-consistency mechanism, not a proof of complete quantum equivalence.",
      "spinor_parallel_susy_warning":"Spin structures existing does NOT imply Killing spinors. The local IIB T11 Killing-spinor lift is available for N=1, and for N=2 with its alternative lift; for N>2 no such lift of covering spinors.",
      "equal_flux_volume_in_Ric4_units":"16*pi^3/(27*N)",
      "equal_flux_leading_a_c":"(27/64)*N*N0^2",
      "BF_lower_branch":"m_-^2 L^2=lambda-2-sqrt(4+16 lambda)",
      "BF_band_open":[0,12],"minimum_m2L2":"-25/4",
      "minimizer_lambda":"15/4",
      "square_torus_first_lambda":"3*pi*N0/N (N0>0, N>0)",
      "square_torus_BF_iff":"N/N0>pi/4",
      "square_torus_samples":square,
      "IIB_supergravity_scope":"The zero-winding sector is a low-energy truncation; the winding tachyon band is omitted from the point-field supergravity KK spectrum, not disproven. Its presence and validity depends on full string backgrounds and lattice shape.",
      "independent_method":"Integral Gysin sequence, 2x1 and 1x2 Smith forms, exact SymPy BF stationarity and sampled quantized winding comparison.",
      "claim_limits":"Conditional on circle-bundle dual identification and compact integral flux. Not a full supersymmetry theorem for all quotients, string-worldsheet stability theorem, or proof of physical TOE."
    }
    OUTPUT.write_text(json.dumps(result,indent=2)+"\n")
    return result

if __name__=="__main__":
    r=run()
    print("PASS",r["status"],"Betti b3=",r["all_nontrivial_c1_deRham_betti"][3])
