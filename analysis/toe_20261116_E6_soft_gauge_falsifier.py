"""Gauge-invariant soft lifting of the cubic E6-trinification singlet modulus.

A=B=C=s I3, F=D=0 from preceding exact cubic certificate.
The illustrative, SU(3)^3-invariant EFT deformation uses
I=sum Tr(M_i^dagger M_i), V_soft=(m2/3)*I + kappa*I^3/(729*M^2).
Along the singlet branch this is 3*m2*|s|^2+kappa*|s|^6/M^2.
We compute the constrained stationary point and the complete gauge-vector
mass degeneracies; full off-branch scalar stability is NOT asserted.
"""
import importlib.util,math,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261116_E6_soft_gauge_falsifier.json"
sp=importlib.util.spec_from_file_location("e6",ROOT/"analysis"/"toe_20261116_e6_trinification_cubic_flat_branches.py")
cubic=importlib.util.module_from_spec(sp);sp.loader.exec_module(cubic)

def soft_branch(m2:float,kappa:float,M:float,gYM:float):
    if kappa<=0 or M<=0 or gYM<=0:raise ValueError("kappa,M,gYM>0 required")
    if m2>=0:
        return {"input":{"m2":m2,"kappa":kappa,"M":M,"gYM":gYM},
                "nonzero_singlet_stationary_point":False,
                "origin_stable_along_singlet":True}
    r=(-m2*M*M/kappa)**.25
    I=9*r*r
    V=(m2/3)*I+kappa*I**3/(729*M*M)
    predicted=3*m2*r*r+kappa*r**6/(M*M)
    assert abs(V-predicted)<1e-8*max(1,abs(V))
    assert abs(6*m2*r+6*kappa*r**5/(M*M))<1e-8
    # Equal gauge couplings; each bifundamental link gives
    # (gYM^2 |s|^2/2)*(A_i^a-A_j^a)^2 per generator.
    # Triangle graph Laplacian has eigenvalues 0,3,3.
    laplacian=((2,-1,-1),(-1,2,-1),(-1,-1,2))
    assert all(sum(row)==0 for row in laplacian)
    assert all(sum(laplacian[i][j]*x[j] for j in range(3))==3*x[i]
               for x in ((1,-1,0),(1,1,-2)) for i in range(3))
    mass2=3*gYM*gYM*r*r
    radial=-4*m2
    return {
       "input":{"m2":m2,"kappa":kappa,"M":M,"gYM":gYM},
       "nonzero_singlet_stationary_point":True,
       "VEV_abs_s":r,
       "VEV_fourth_power":r**4,
       "invariant_I":I,
       "soft_potential_at_VEV":V,
       "radial_canonical_mass2":radial,
       "phase_canonical_mass2":0,
       "gauge_vector_mass2_eigenvalues":[0,mass2,mass2],
       "gauge_multiplicities":{"massless_diagonal_SU3":8,"massive":16},
       "SU3_diagonal_rank":2,"Standard_Model_gauge_rank":4,
       "full_scalar_stability_proven":False,
       "scale_origin":"Inserted m2, kappa and suppression scale M: no first-principles prediction",
       "physical_limitation":"Global angular modulus remains; wrong unbroken gauge rank, and the full non-singlet Hessian has not been checked."
    }

def supersymmetric_gauge_loop_control(gYM:float,r:float):
    """Supertrace of the 16 massive 4D N=1 vector multiplets.

    In unbroken N=1 SUSY each massive vector multiplet comprises a
    massive vector (3 real polarizations), one real scalar (1), and
    one Dirac fermion (4); at common mass squared 3*gYM^2*r^2 the
    supertraces vanish. Computing gauge-vector loops ALONE would
    spuriously lift this F=D-flat branch.
    """
    m2=3*gYM*gYM*r*r
    str2=16*((3+1-4)*m2)
    str4=16*((3+1-4)*m2*m2)
    assert str2==0 and str4==0
    return {"mass_squared":m2,
            "massive_N1_vector_multiplets":16,
            "per_multiplet_real_bosonic_dof":4,
            "per_multiplet_real_fermionic_dof":4,
            "supertrace_mass2":str2,"supertrace_mass4":str4,
            "physics_caveat":"At exact unbroken SUSY, the F=D-flat vacuum energy remains zero perturbatively; explicit soft breaking, nonperturbative superpotentials and full spectrum may change this."}

def verify():
    assert cubic.scalar_triad(1,1,1)["F_norm_squared"]==0
    rows=[soft_branch(-1,1,1,1),soft_branch(-4,2,3,.7),soft_branch(1,1,1,1)]
    a=rows[0]
    assert a["VEV_abs_s"]==1
    assert a["radial_canonical_mass2"]==4
    assert a["gauge_vector_mass2_eigenvalues"]==[0,3,3]
    assert a["gauge_multiplicities"]["massive"]==16
    assert rows[2]["nonzero_singlet_stationary_point"] is False
    return {
      "status":"PASS_E6_SOFT_RADIAL_LIFT_AND_RESIDUAL_GAUGE_OBSTRUCTION",
      "strict_scope":"One gauge-invariant toy soft-EFT deformation evaluated only along the exact cubic F- and D-flat singlet locus",
      "triad_gauge_mass":"For each of 8 su(3) generators, triangle Laplacian has 0,3*gYM^2*|s|^2 twice",
      "weakness":"Soft terms explicitly introduce physical scales; no unique SM vacuum or complete 27+27bar spectrum.",
      "supersymmetric_one_loop_vector_multiplet_supertrace":supersymmetric_gauge_loop_control(1.,1.),
      "cases":rows}
if __name__=="__main__":
    v=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(v,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(v["status"],v["cases"][0]["gauge_vector_mass2_eigenvalues"])
