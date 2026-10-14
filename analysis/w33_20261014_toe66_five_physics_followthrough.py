"""TOE66: five independent finite-model physics fronts, with explicit caveats."""
from __future__ import annotations
from pathlib import Path
import json, math, sys
import numpy as np
from scipy.optimize import brentq
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261013_toe65_edge_product_adversary import ED,V,C,W,SGN
HIGH_EDGES=(30,31,49,51,59,62,63,82,83,93,95,118,119,138,139,142,143)
Q=(0,-1,1)

def native_adversary():
    bits=np.zeros(160,dtype=np.int64);bits[list(HIGH_EDGES)]=1
    counts=(C@bits).astype(int);q=np.asarray(Q,dtype=int)
    coeff=[sum(int(SGN[i])*int(W[i]@q)**2 for i,h in enumerate(counts) if h==k)
           for k in range(9)]
    assert coeff==[0,0,72,46,34,0,0,0,-12]
    def rat(n,d):
        return sum(int(coeff[k])*(d+n)**k*(d-n)**(8-k) for k in range(9))
    assert rat(244615,1000000)>0
    negative=rat(244616,1000000)
    assert negative<0
    root=float(brentq(lambda x:sum(coeff[k]*(1+x)**k*(1-x)**(8-k)
                            for k in range(9)),.24,.25,xtol=5e-16))
    old=json.loads((ROOT/"data/w33_20261013_toe65_exact_edge_disorder_bracket.json").read_text())
    assert old["native_winding_octagons"]==len(W)==238
    assert len(HIGH_EDGES)<sum(old["edge_high_bits"])
    assert root<.245
    return {"status":"CERTIFIED","high_edge_indices":list(HIGH_EDGES),
       "phase_ray":list(Q),"ray_polynomial_coefficients":coeff,
       "polynomial_root_numeric":root,
       "new_counterexample_epsilon":"244616/1000000",
       "exact_negative_integer":str(negative),
       "preceding_exact_positive_integer":str(rat(244615,1000000)),
       "TOE64_proven_lower":(11**(1/8)-1)/(11**(1/8)+1),
       "scope":"Native 160-edge product leading beta^7 Hessian counterexample, not a global minimax threshold."}

def fermi_energy(theta,beta,amplitudes):
    ph=amplitudes*np.exp(1j*(V@np.asarray(theta)))
    H=np.zeros((80,80),complex)
    H[ED[:,0],ED[:,1]]=-ph
    H[ED[:,1],ED[:,0]]=-np.conj(ph)
    en=np.linalg.eigvalsh(H)
    if beta is None:return float(-sum(abs(en))/2)
    return float(-sum(np.logaddexp(beta*en/2,-beta*en/2))/beta)

def thermal_front():
    bits=np.zeros(160,dtype=bool);bits[list(HIGH_EDGES)]=True
    amp=np.where(bits,1.3,.7)
    pi=np.ones(3)*np.pi
    u=np.asarray(Q,dtype=float);u/=np.linalg.norm(u)
    h=.05;cases=[]
    for beta in (.4,.8,1.,1.5,2.,2.5,4.,8.,None):
        f0=fermi_energy(pi,beta,amp)
        fp=fermi_energy(pi+h*u,beta,amp)
        fm=fermi_energy(pi-h*u,beta,amp)
        assert abs(fp-fm)<1e-9
        cases.append({"beta":"infinity" if beta is None else beta,
            "directional_second_difference":(fp+fm-2*f0)/h**2})
    assert cases[1]["directional_second_difference"]<-1e-5
    assert cases[5]["directional_second_difference"]>1e-3
    def curve(beta,step=.05):
        return (fermi_energy(pi+step*u,beta,amp)
               +fermi_energy(pi-step*u,beta,amp)
               -2*fermi_energy(pi,beta,amp))/step**2
    crossing=float(brentq(curve,1.5,2.5))
    return {"status":"EXACT_STATIONARITY_NUMERICAL_CROSSOVER",
        "stationarity_proof":"H(-phi)=conjugate(H(phi)) for real edge weights. Since -pi=pi modulo 2pi, every differentiable spectral free energy is stationary at three-pi for all beta, but need not minimize.",
        "weighted_deviation":.30,"direction":u.tolist(),"step":h,
        "curvature_cases":cases,"numerical_crossover_beta":crossing,
        "half_step_curvature_at_crossing":float(curve(crossing,.025)),
        "small_beta_nonuniform_counterexample":"The exact negative eighth moment phase Hessian gives nonminimality at sufficiently small positive beta by analytic log-cosh series.",
        "scope":"One-dimensional directional curvature scan, not a certified critical temperature or thermodynamic transition; no global all-beta U1 selection theorem."}

def ribbon_front():
    adj=[[] for _ in range(80)]
    for i,(a,b) in enumerate(ED):
        adj[int(a)].append((i,0));adj[int(b)].append((i,1))
    assert [len(v) for v in adj]==[4]*80
    sigma={}
    for row in adj:
        row.sort()
        for i,d in enumerate(row):sigma[d]=row[(i+1)%4]
    perm={d:sigma[(d[0],1-d[1])] for d in sigma}
    remaining=set(perm);lengths=[]
    while remaining:
        d=min(remaining);start=d;length=0
        while d in remaining:
            remaining.remove(d);length+=1;d=perm[d]
        assert d==start
        lengths.append(length)
    lengths.sort()
    b=len(lengths)
    assert (2-b-(80-160))%2==0
    h=(2-b-(80-160))//2
    g=2*h+b-1
    assert (h,b,g)==(39,4,81)
    assert lengths==[12,14,106,188]
    return {"status":"CERTIFIED_RIBBON_DOUBLE",
        "original_vertices":80,"original_edges":160,
        "rotation":"cyclic order of incident Levi edges by sorted edge index",
        "ribbon_boundary_lengths":lengths,"ribbon_genus":h,
        "ribbon_boundary_components":b,"doubled_closed_genus":g,
        "doubled_surface_euler":2-2*g,
        "scope":"Constructed genuine orientable closed surface; rotation/doubling noncanonical. Not original clique two-skeleton or a derived physical spacetime."}

def four_dim_front(ribbon):
    g=ribbon["doubled_closed_genus"];n=2*g
    J=np.zeros((n,n),dtype=int)
    for i in range(g):
        J[2*i,2*i+1]=1;J[2*i+1,2*i]=-1
    JT=np.array([[0,1],[-1,0]],dtype=int)
    Qmat=np.zeros((2+2*n,2+2*n),dtype=int)
    Qmat[0,1]=Qmat[1,0]=1
    Qmat[2:,2:]=-np.kron(J,JT)
    assert Qmat.shape==(326,326)
    assert np.array_equal(Qmat,Qmat.T)
    assert np.array_equal(Qmat@Qmat,np.eye(326,dtype=int))
    assert int(np.trace(Qmat))==0
    c=np.zeros(326,dtype=int);c[:2]=1
    assert int(c@Qmat@c)==2
    return {"status":"CERTIFIED_CONTINUUM_INDEX_ON_DERIVED_MANIFOLD",
        "M4":"Double(W33 Levi ribbon) times T2",
        "betti":[1,164,326,164,1],
        "intersection_signature":[163,163],"hyperbolic_planes":163,
        "spin":True,"selected_c1_square":2,"twisted_spin_Dirac_index":1,
        "index_formula":"ind D_L = integral (c1(L)^2/2 - p1/24) = 1 for signature zero",
        "scope":"True continuum index on noncanonical W33-derived closed spin 4-manifold with added T2 and chosen U1 line bundle; not a native overlap lattice index, Standard Model Weyl spectrum or unique TOE geometry."}

def cutoff_front():
    old=json.loads((ROOT/"data/w33_20261013_toe65_three_loop_cutoff_grid.json").read_text())
    p=old["native_patch"]
    assert (p["sites"],p["links"],p["fermions"],p["contained_Wilson_rows"])==(14,16,6,6)
    rows=old["new_runs"]+old["baseline_runs_from_TOE62"]
    by={(z["depth"],z["L"]):z for z in rows}
    assert len(by)==7
    cases=[]
    for (depth,L),z in sorted(by.items()):
        for sector in ("neutral","charged"):
            x=z["sectors"][sector]
            residual=11.2*math.sqrt(x["Fock_boundary_weight"])+3.75*math.sqrt(x["electric_flux_boundary_weight"])+x["eigensolver_residual"]
            cases.append({"depth":depth,"L":L,"sector":sector,
               "Ritz_energy":x["ground"],"boundary_spectral_residual_upper":residual,
               "Fock_boundary_probability":x["Fock_boundary_weight"],
               "flux_boundary_probability":x["electric_flux_boundary_weight"]})
    assert len(cases)==14
    E=lambda d,l:by[d,l]["sectors"]["neutral"]["ground"]
    assert E(2,3)<E(2,2) and E(3,2)<E(3,1)
    return {"status":"RIGOROUS_BUT_LOOSE_SPECTRAL_DISTANCE_BOUND",
        "Fock_operator_prefactor":11.2,"flux_operator_prefactor":3.75,
        "derived_bound":"||QH psi|| <= 16*kappa*sqrt(P_Fock shell)+6*(beta/g^2)*sqrt(P_flux shell), plus numerical eigensolver residual. Simple octagon chord changes <=1. Distance from Ritz energy to SOME full patch spectral point is at most this norm; not ground-state error.",
        "d2_L2_to_L3_neutral_shift":E(2,3)-E(2,2),
        "d3_L1_to_L2_neutral_shift":E(3,2)-E(3,1),
        "full_patch_ground_lower_from_TOE65":-13.0,
        "cases":cases,
        "scope":"Reanalysis of published TOE62/TOE65 native 14-site interacting patch data, no new eigensolves; bounds too loose for convergence or rigorous charge gap. Not full 80-site theory."}

def certificate():
    a=native_adversary()
    b=thermal_front()
    c=ribbon_front()
    d=four_dim_front(c)
    e=cutoff_front()
    return {"status":"PASS_TOE66_FIVE_FRONTS",
      "front1":a,"front2":b,"front3":c,"front4":d,"front5":e,
      "physics_scope":"Mathematical and finite-model results. Physical TOE, emergent Lorentz gravity, unique spacetime selection, overlap lattice index and anomaly-free SM remain open."}

if __name__=="__main__":
    out=certificate()
    path=ROOT/"data/w33_20261014_toe66_five_physics_followthrough.json"
    path.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(out["status"],out["front1"]["new_counterexample_epsilon"],
          out["front3"]["doubled_closed_genus"],out["front4"]["twisted_spin_Dirac_index"])
