#!/usr/bin/env python3
"""W33 compact U1 gauge+free matter: full 81-chord variational vacuum.

Optimize ALL 81 independent Wilson coordinates for the *specified*
all-1620-octagon Wilson action plus free half-filled fermion determinant.
Includes analytical Jacobian, numerical finite-difference guard, global
grid controls, and flat-vacuum local Hessian/stability threshold. Multistart
local optimization DOES NOT prove any global vacuum or select physical κ.
"""
import json,sys,math
from pathlib import Path
import numpy as np
import networkx as nx
from scipy.optimize import minimize
from scipy.linalg import eigh
from w33_20261109_flux_dark_mode_fragility import build
from w33_20261109_octagon_gauge_matter_tradeoff import loops_length8
from w33_20261109_81_wilson_flux_decoder import decode

def model():
    B, edges, G=build()
    tree=nx.bfs_tree(G,0).to_undirected()
    chords=sorted({tuple(sorted((a,b))) for a,b in G.edges()} -
                  {tuple(sorted((a,b))) for a,b in tree.edges()})
    assert len(chords)==81
    pos={frozenset(e):j for j,e in enumerate(chords)}
    endpoints=[(u,v-40) if u<40 else (v,u-40) for u,v in chords]
    W=np.zeros((1620,81),dtype=np.float64)
    loops=loops_length8(G)
    assert len(loops)==1620
    for i,ring in enumerate(loops):
        for a,b in zip(ring,ring[1:]+ring[:1]):
            j=pos.get(frozenset((a,b)))
            if j is not None:W[i,j]+=1 if a<40 else -1
    return B,edges,G,chords,endpoints,W

def physics(x, ctx, kappa, beta=1.):
    B,edges,G,chords,endpoints,W=ctx
    T=B.astype(complex)
    rows=np.fromiter((p for p,l in endpoints),dtype=int)
    cols=np.fromiter((l for p,l in endpoints),dtype=int)
    z=np.exp(1j*x)
    T[rows,cols]=z
    U,s,Vh=np.linalg.svd(T,full_matrices=False)
    F=float(-(2/beta)*np.logaddexp(beta*s/2,-beta*s/2).sum())
    DD=(U*np.tanh(beta*s/2)[None,:])@Vh
    dF=-np.real(np.conj(DD[rows,cols])*(1j*z))
    phi=W@x
    mag=float(np.sum(1-np.cos(phi)))
    dM=W.T@np.sin(phi)
    return F+kappa*mag,dF+kappa*dM,F,mag,float(s[-1]),s

def gauge_of_edges(phi,ctx):
    B,edges,G,chords,endpoints,W=ctx
    _,r,_=decode(phi,G)
    return np.array([r[p,l] for p,l in endpoints])

def test_grad(ctx):
    rng=np.random.default_rng(20261109)
    x=rng.uniform(-.7,.7,81)
    for kappa in (0.,.0001,.01):
        fun,g,*_=physics(x,ctx,kappa)
        errs=[]
        for j in (0,6,15,27,41,65,80):
            h=1e-5
            a=x.copy();a[j]+=h
            b=x.copy();b[j]-=h
            df=(physics(a,ctx,kappa)[0]-physics(b,ctx,kappa)[0])/(2*h)
            errs.append(abs(df-g[j]))
        assert max(errs)<2e-8,(kappa,errs)

def local_critical(ctx,beta=1.):
    x=np.zeros(81)
    W=ctx[-1]
    # Hessian of all-octagon Wilson action is W^T W at flat flux.
    G=W.T@W
    assert np.linalg.eigvalsh(G)[0]>.001
    eps=1e-3
    H=np.column_stack([(physics(np.eye(81)[j]*eps,ctx,0,beta)[1]-
                        physics(-np.eye(81)[j]*eps,ctx,0,beta)[1])/(2*eps)
                       for j in range(81)])
    H=(H+H.T)/2
    vals=eigh(H,G,eigvals_only=True)
    crit=max(0.,float(-vals[0]))
    # Directly test crossing of full 81D Hessian matrix.
    for k in (crit*.9,crit*1.1):
        lowest=np.linalg.eigvalsh(H+k*G)[0]
        if k<crit:assert lowest<-1e-9,(k,crit,lowest)
        else:assert lowest>1e-9,(k,crit,lowest)
    return {"flat_Hferm_generalized_min_eig":float(vals[0]),
            "flat_Hferm_generalized_max_eig":float(vals[-1]),
            "flat_local_positive_Hessian_threshold_kappa":crit,
            "finite_difference_hessian_step":eps,
            "G_Wilson_eigen_min":float(np.linalg.eigvalsh(G)[0]),
            "G_Wilson_eigen_max":float(np.linalg.eigvalsh(G)[-1])}

def main(path=None):
    ctx=model()
    test_grad(ctx)
    B,edges,G,chords,endpoints,W=ctx
    root=Path(__file__).resolve().parents[1]
    prior=json.loads((root/"data/w33_20261109_minimal_15_flux_lift.json").read_text())
    opt=json.loads((root/"data/w33_20261109_flux_mass_gap_design.json").read_text())
    oldmask=np.zeros((40,40));bestmask=oldmask.copy()
    for e in prior["constructed_phase_only_pi_flip_links"]:
        oldmask[e["point"],e["line"]]=np.pi
    for e in opt["best_15_edges"]:
        bestmask[e["point"],e["line"]]=np.pi
    fixed={"flat":np.zeros(81),
        "fifteen_original":gauge_of_edges(oldmask,ctx),
        "fifteen_best_gap":gauge_of_edges(bestmask,ctx)}
    for name,x in fixed.items():
        val,grad,f,mag,minsv,s=physics(x,ctx,0)
        if name=="flat":assert abs(f+87.59344827068617)<1e-8
        if name=="fifteen_original":assert abs(f+87.68795102768237)<1e-8
        if name=="fifteen_best_gap":assert abs(f+87.68573187830089)<1e-8
    critical=local_critical(ctx)
    rng=np.random.default_rng(2026110902)
    curves=[]
    for k in (0.,.00001,.00005,.0001,.001,.01):
        seeds=list(fixed.items())
        seeds.extend([("random_"+str(i),rng.uniform(-np.pi,np.pi,81))
                      for i in range(2)])
        best=None;solutions=[]
        for name,x in seeds:
            fun=lambda q:physics(q,ctx,k)
            result=minimize(lambda q: fun(q)[0],x,
                   jac=lambda q:fun(q)[1],method="L-BFGS-B",
                   bounds=[(-np.pi,np.pi)]*81,
                   options={"maxiter":130,"gtol":2e-7,"ftol":3e-13})
            z=result.x
            val,g,f,mag,sg,s=physics(z,ctx,k)
            row={"seed":name,"objective":float(val),"fermion_free_energy":float(f),
                 "all_octagon_magnetic_penalty_unweighted":float(mag),
                 "gradient_sup":float(max(abs(g))),
                 "minimum_singular_value":sg,
                 "phase_chord_number_nonzero_gt_1e_3":int(sum(abs(z)>1e-3)),
                 "iterations":int(result.nit),
                 "converged":bool(result.success)}
            solutions.append(row)
            if best is None or val<best["objective"]:
                best={**row,"chord_phases":[float(w) for w in z]}
        reference={name:float(physics(x,ctx,k)[0]) for name,x in fixed.items()}
        assert best["objective"]<=min(reference.values())+2e-6
        curves.append({"gauge_penalty_kappa":k,
                "best_multistart_local":best,
                "all_start_controls":solutions,
                "fixed_sector_reference_objectives":reference})
        print("FULL_U1_81D",k,"best",round(best["objective"],8),
              "vsflat",round(best["objective"]-reference["flat"],7),
              "mag",round(best["all_octagon_magnetic_penalty_unweighted"],5),
              "grad",round(best["gradient_sup"],6),flush=True)
    out={"status":"PASS_W33_81_GAUGE_FERMION_VARIATIONAL_VACUUM_AND_LOCAL_STABILITY",
      "exact_81_chord_unimodular_certificate_prior":"data/w33_20261109_full_octagon_integer_gauge_basis.json",
      "octagon_count":1620,"chord_number":81,
      "free_fermion_inverse_temperature_beta":1,
      "objective_definition":"J_kappa(x)=-2 sum_s log(2 cosh(singular(B(x))/2)) + kappa sum_{1620 octagons}(1-cos(Wx)), with one fixed gauge tree and U1 edge phases on all81 chords",
      "gradient_method":"analytical SVD spectral derivative -Re(conj(U diag tanh(s/2) V†)_edge * i exp(i x_edge)) + κ W.T sin(Wx)",
      "gradient_finite_difference_checks_passed":True,
      "flat_vacuum_local_Hessian":critical,
      "multistart_local_variational_results":curves,
      "proven_global_bound":"Each best is an explicit upper bound on the unknown global minimum (a trial state); no upper bound on all possible configurations' energy gap is proved.",
      "limits":"Numerical multistart L-BFGS-B with 81 gauge coordinates, not global exact minimization. Hessian threshold is local and numerical, not spontaneous flux proof or fundamental coupling. The all-1620 octagon model imposes winding-loop penalties unlike TOE38's 1382 local plaquettes. No photonic hardware or SM chirality derived.",
      "references":["https://doi.org/10.1103/PhysRevLett.73.2158",
                    "https://doi.org/10.1007/s10955-026-03617-y"]}
    if path:Path(path).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print("U1_RESULT",json.dumps({"Hcrit":critical["flat_local_positive_Hessian_threshold_kappa"],
        "best_at_k0":curves[0]["best_multistart_local"]["objective"],
        "best_at_k001":curves[-1]["best_multistart_local"]["objective"]}))
    return out
if __name__=="__main__":main(sys.argv[1] if len(sys.argv)>1 else None)
