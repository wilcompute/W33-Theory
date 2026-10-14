"""TOE71 full 80-site *site-dependent* Hartree and Hartree-Fock solver.

Local native density repulsion V*(n_i-.5)*(n_j-.5) on all 160 edges,
uniform pi pi pi hopping signs but WITHOUT uniform density assumptions.
An 80x80 self-consistent one-body approximation, not exact interacting
many-body ground state or an experimentally derived mass.
"""
from pathlib import Path
import json,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe69_five_fronts import graph

def model():
    edges,_=graph()
    H0=np.zeros((80,80))
    adjacency=np.zeros((80,80))
    for e,(a,b) in enumerate(edges):
        H0[a,b]=H0[b,a]=-(-1 if e in (59,93,139) else 1)
        adjacency[a,b]=adjacency[b,a]=1
    assert int(adjacency.sum())==320
    return edges,H0,adjacency

def unrestricted_solver(V,exchange,seed=.2,mix=.45,tolerance=1e-11):
    edges,H0,A=model()
    stagger=np.r_[np.ones(40),-np.ones(40)]
    eig,u=np.linalg.eigh(H0+np.diag(seed*stagger))
    rho=u[:,:40]@u[:,:40].T
    for step in range(700):
        d=np.diag(rho)-.5
        effective=H0+V*np.diag(A@d)
        if exchange:effective-=V*A*rho
        effective=(effective+effective.T)/2
        eig,u=np.linalg.eigh(effective)
        next_rho=u[:,:40]@u[:,:40].T
        residual=float(np.max(abs(next_rho-rho)))
        if residual<tolerance:
            rho=next_rho
            break
        rho=mix*next_rho+(1-mix)*rho
    assert residual<tolerance
    d=np.diag(rho)-.5
    energy=float(np.trace(H0@rho)+V*sum(
       d[a]*d[b]-(rho[a,b]**2 if exchange else 0) for a,b in edges))
    # Strict finite one-body gap at the CONVERGED HF solution.
    gap=float(eig[40]-eig[39])
    assert gap>0
    consistency=np.max(abs(rho@rho-rho))
    assert consistency<1e-9
    return {
      "V":V,"exchange_included":exchange,
      "initial_mass_sign":1 if seed>0 else -1,
      "iterations":step+1,"max_fixed_point_residual":residual,
      "projector_idempotency_error":float(consistency),
      "HF_trial_energy":energy,
      "quasiparticle_gap":gap,
      "mean_point_charge_minus_half":float(d[:40].mean()),
      "mean_line_charge_minus_half":float(d[40:].mean()),
      "point_density_std":float(d[:40].std()),
      "line_density_std":float(d[40:].std())
    }

def symmetric_trial(V,exchange):
    edges,H0,A=model()
    ev,u=np.linalg.eigh(H0)
    occ=(ev<-1e-9).astype(float)+.5*(abs(ev)<1e-9)
    rho=(u*occ)@u.T
    d=np.diag(rho)-.5
    assert max(abs(d))<1e-10
    return float(np.trace(H0@rho)+V*sum(
        d[a]*d[b]-(rho[a,b]**2 if exchange else 0) for a,b in edges))

def certificate():
    rows=[]
    for V in (.05,.2,.4,.8):
        for exchange in (False,True):
            plus=unrestricted_solver(V,exchange,seed=.2)
            minus=unrestricted_solver(V,exchange,seed=-.2)
            control=symmetric_trial(V,exchange)
            assert plus["mean_point_charge_minus_half"]<0
            assert minus["mean_point_charge_minus_half"]>0
            assert abs(plus["HF_trial_energy"]-minus["HF_trial_energy"])<1e-8
            assert plus["HF_trial_energy"]<control
            plus["symmetric_zero_mode_mixed_trial_energy"]=control
            plus["energy_gain_vs_symmetric_trial"]=control-plus["HF_trial_energy"]
            plus["symmetry_related_opposite_branch_gap"]=minus["quasiparticle_gap"]
            rows.append(plus)
    target=next(z for z in rows if z["V"]==.2 and z["exchange_included"])
    assert abs(target["quasiparticle_gap"]-.2404442056)<1e-7
    assert target["point_density_std"]>.039
    return {
      "status":"PASS_TOE71_UNRESTRICTED_LOCAL_SELF_CONSISTENT_HF",
      "native_sites":80,"native_edges":160,
      "interaction":"V*sum_edges(n_i-1/2)(n_j-1/2)",
      "Hartree_effective_onsite":"V*sum_neighbor(rho_jj-1/2)",
      "Fock_effective_offdiagonal":"-V*adjacency_ij*rho_ij",
      "runs":rows,
      "at_V_0p2_HF_quasiparticle_gap":target["quasiparticle_gap"],
      "at_V_0p2_HF_energy_gain":target["energy_gain_vs_symmetric_trial"],
      "scope":"Numerically converged self-consistent sitewise Hartree AND exchange-inclusive Hartree-Fock fixed points, with broken particle-hole symmetry pairs; not a proof of globally minimal HF energy, exact finite interacting Hamiltonian gap, thermodynamic spontaneous order, gauge-dynamical mass, physical hierarchy, or parameter-free observation."
    }

if __name__=="__main__":
    out=certificate()
    (ROOT/"data/w33_20261014_toe71_sitewise_hartree_fock.json").write_text(
      json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(out["status"],out["at_V_0p2_HF_quasiparticle_gap"])
