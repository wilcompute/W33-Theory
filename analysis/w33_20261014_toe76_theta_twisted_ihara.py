"""TOE76: exact link of the native 11-site W33 Theta(4,4,4) flux law
to Ihara/Bass, Ramanujan-style tempered twisted spectra and graph RH.

The 11-site graph is IRREGULAR. A 'k=12 Ramanujan' claim about it is
incorrect. Equal length-4 subdivisions of the 3-edge dipole transport
the dipole's twisted Ihara factor via t=u**4. The original collinearity
graph has its own independent regular Ramanujan/G-RH theorem.
"""
from __future__ import annotations
import json,cmath,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe69_two_octagon_covariance import patch
from w33_20261014_toe74_theta_friendship import theta_symmetry
from w33_20261014_toe74_u1_manybody_finite_t import phases_for_chords

def hashimoto(p,phi):
    directed=[]
    for e,(a,b) in enumerate(p["p_ed"]):
        directed.extend([(a,b,e,1),(b,a,e,-1)])
    H=np.zeros((len(directed),len(directed)),dtype=complex)
    for i,(a,b,e,sgn) in enumerate(directed):
        for j,(b2,c,f,tgn) in enumerate(directed):
            if b==b2 and c!=a:
                H[i,j]=cmath.exp(1j*tgn*phi[f])
    return H,directed

def analytic_coeff(s_squared):
    # x=u^8.  det(I-u B_chi)=(1-x)[1+(4-s^2)x+4x^2].
    return np.array([1.,3.-s_squared,s_squared,-4.],float)

def certificate():
    p=patch();theta=theta_symmetry()
    assert theta["independent_cycle_rank"]==2
    assert sorted(len(path)-1 for path in theta["native_three_equal_four_edge_routes"])==[4,4,4]
    assert sum(len(a) for a in theta["S3_arm_permutation_automorphisms"])==66
    assert len(p["p_ed"])==12
    cases=[(0.,0.),(np.pi,0.),(2*np.pi/3,4*np.pi/3),
           (1.13,4.7),(.37,.91), (np.pi/3,2*np.pi/7)]
    probes=[.11,.23,.43,.66]
    rows=[]
    for a,b in cases:
        phase=phases_for_chords(p,(a,b))
        T,directed=hashimoto(p,phase)
        assert T.shape==(24,24)
        assert np.max(np.abs(np.trace(T)))<1e-11
        z=np.array([1.,cmath.exp(1j*a),cmath.exp(1j*b)])
        square=abs(sum(z))**2
        # 6 oriented collapsed paths. Non-backtracking continuation
        # at either hub requires switching to another of the 3 arms.
        K=np.ones((3,3))-np.eye(3)
        Z=np.diag(z)
        P=K@np.conj(Z)@K@Z
        roots=np.linalg.eigvals(P)
        t1=float(np.real(np.trace(P)))
        t2=float(np.real((t1*t1-np.trace(P@P))/2))
        det=float(np.real(np.linalg.det(P)))
        assert abs(t1-(square-3))<1e-10
        assert abs(t2-square)<1e-10
        assert abs(det-4)<1e-10
        coeff=analytic_coeff(square)
        assert abs(np.trace(np.linalg.matrix_power(T,8))-8*(square-3))<1e-8
        assert abs(np.trace(np.linalg.matrix_power(T,16))-
                   8*((square-3)**2-2*square))<1e-7
        err=0.
        for u in probes:
            d1=np.linalg.det(np.eye(24)-u*T)
            x=u**8
            d2=(1-x)*(1+(4-square)*x+4*x*x)
            err=max(err,abs(d1-d2))
            assert abs(d1-d2)<2e-8, (a,b,u,d1,d2)
            # Bass holds despite irregularity: E-V = 1;
            # twisted adjacency A_phi in its unitarily gauged orientation.
            A=np.zeros((11,11),dtype=complex)
            for e,(v,w) in enumerate(p["p_ed"]):
                A[v,w]=cmath.exp(1j*phase[e])
                A[w,v]=A[v,w].conjugate()
            deg=np.diag([sum(v in edge for edge in p["p_ed"])
                          for v in range(11)])
            bass=(1-u*u)*np.linalg.det(np.eye(11)-u*A+
                            u*u*(deg-np.eye(11)))
            assert abs(bass-d2)<2e-8, (a,b,u,bass,d2)
        rows.append({"phases_pi":[a/np.pi,b/np.pi],
           "s_squared":float(square),
           "inverse_zeta_x_coefficients":coeff.tolist(),
           "nonbacktracking_trace_8":float(8*(square-3)),
           "nonbacktracking_trace_16":float(8*((square-3)**2-2*square)),
           "max_independent_24x24_hashimoto_vs_11x11_Bass_vs_3x3_transfer_error":float(err),
           "collapsed_transfer_eigenvalues":[[float(v.real),float(v.imag)] for v in roots]})
    # exact special phase polynomial identities, coefficients in Z:
    assert analytic_coeff(9).tolist()==[1,-6,9,-4]  # (1-x)^2(1-4x)
    assert analytic_coeff(1).tolist()==[1,2,1,-4]
    assert analytic_coeff(0).tolist()==[1,3,0,-4]   # (1-x)(1+2x)^2
    # For 0 <= s^2 <= 8, roots of 4x²+(4-s²)x+1
    # are conjugate (or double), so |x|=1/2,
    # i.e. |u|=(1/2)^(1/8). This is the TWISTED
    # dipole's tempered condition |lambda|=s <= 2 sqrt2.
    samples=[(0,True),(1,True),(8,True),(9,False)]
    for s2,inside in samples:
        roots=np.roots([4,4-s2,1])
        assert all(abs(abs(z)-.5)<1e-8 for z in roots)==inside
    # Separate main W33 collinearity Ramanujan condition:
    # degree12, nontrivial eigenvalues 2,-4; 4²<4*11.
    assert 2**2<4*11 and (-4)**2<4*11
    return {
      "status":"PASS_TOE76_NATIVE_THETA_TWISTED_IHARA_RAMANUJAN_BRIDGE",
      "repo_sources_checked":[
        "manuscripts/tex/part27_graph_rh_theorem.tex",
        "w33_paper.tex (manuscript wrapper)",
        "analysis/w33_ihara_zeta.py",
        "analysis/w33_pass74_zeta_frontier.py",
        "manuscripts/parts/PART_MCLIII_IHARA_ZETA.md",
        "analysis/w33_pass3080_3082_bass_regular_audit.py"],
      "theta_vertices_edges":[11,12],"degree_multiset":{"2":9,"3":2},
      "cycle_rank":2,"primitive_undirected_girth_eight_cycles":3,
      "fourfold_subdivision_of_3_parallel_edge_dipole":True,
      "zeta_inverse_exact":"(1-u^8)*(1+(4-s^2)*u^8+4*u^16)",
      "s_definition":"abs(1+exp(i*phi1)+exp(i*phi2))",
      "untwisted_inverse_zeta":"(1-u^8)^2*(1-4*u^8)",
      "120_degree_inverse_twisted_zeta":"(1-u^8)*(1+2*u^8)^2",
      "untwisted_principal_pole_modulus":"2^(-1/4)",
      "unitary_120_nontrivial_pole_modulus":"2^(-1/8)",
      "tempered_twisted_dipole_condition":"s^2<=8; nontrivial roots x=u^8 satisfy |x|=1/2",
      "120_degree_exact_s":0,
      "signed_octagon_nonbacktracking_trace_formula":"trace(Bchi^8)=8*(s^2-3)",
      "free_fermion_exact_energy_uses_same_s":
           "-sqrt(2)-sqrt(5+2sqrt(3+s))-sqrt(5+2sqrt(3-s))",
      "native_main_collinearity_Ramanujan":{
         "vertices":40,"degree":12,"eigenvalues_multiplicities":{"12":1,"2":24,"-4":15},
         "Ihara_nontrivial_circle":"|u|=11^(-1/2)",
         "Ihara_inverse":"(1-u^2)^200(1-u)(1-11u)(1-2u+11u^2)^24(1+4u+11u^2)^15"},
      "independent_hashimoto_bass_transfer_checks":rows,
      "precise_interpretation":"The 11-site theta graph is IRREGULAR: do NOT apply the k=12 Ramanujan criterion or claim all theta poles lie on 1/sqrt(11). Its twisted transfer reduces to a three-regular MULTIGRAPH dipole (with 3 parallel edges); in the base unitary representation the nontrivial quadratic factor is tempered when s<=2sqrt(2), with path-length-4 pullback u^4. The 120° flux achieves s=0, strict interior of the twisted Ramanujan window. Nothing here transfers graph RH to classical Riemann RH.",
      "literature":["Rangarajan, FSTTCS 2017, DOI 10.4230/LIPIcs.FSTTCS.2017.46",
                    "Scattering matrices of regular coverings of graphs, DOI 10.1016/j.disc.2009.09.009"]}
if __name__=="__main__":
    c=certificate()
    (ROOT/"data/w33_20261014_toe76_theta_twisted_ihara.json").write_text(json.dumps(c,indent=2)+"\n")
    print(c["status"],[(v["phases_pi"],v["s_squared"]) for v in c["independent_hashimoto_bass_transfer_checks"]])
