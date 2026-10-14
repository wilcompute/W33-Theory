"""TOE77: W33-specific completion of the native 11-site theta interferometer.

THEOREM (rank obstacle): W33 Levi 40x40 incidence has rank 25,
from singular spectrum 4^1, sqrt(6)^24, 0^15. Adding arbitrary
phases to only two already-existing entries changes its rank by <=2,
so the full 80x80 hopping A=[[0,T],[T*,0]] has at least 26 exact
zero modes, whatever the two theta holonomies. No 4D chirality claim.

THEOREM (girth): any phase-dependent closed walk of length <=8 in
native W33 Levi is an oriented 8-cycle; exactly 16 traversals per
undirected 8-cycle enter tr H^8. Thus the phase-dependent part of
tr H^8 equals 16 sum_C prod_e(w_e) cos(n_C.phi), with 1620 native
octagons and explicitly derived two-chord winding coefficients.

NUMERICAL: restore the other 69 vertices with hopping t, then compare
the full 40-fermion static ground energy against the isolated 5-fermion
theta optimum 120 degrees, and optimize continuous holonomies.
"""
from __future__ import annotations
import collections,itertools,json,math,sys
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe69_five_fronts import graph,octagons
from w33_20261014_toe69_two_octagon_covariance import patch
from w33_20261014_toe75_exact_120_flux import theoretical_energy

def build():
    edges,adj,cycles=octagons()
    p=patch()
    assert len(edges)==160 and len(p["nodes"])==11
    chosen=[int(p["support"][q]) for q in p["chords"]]
    assert len(set(chosen))==2
    assert len(set(p["support"]))==12
    actual={i for i,(a,b) in enumerate(edges) if a in p["nodes"] and b in p["nodes"]}
    assert actual==set(p["support"]), "11-site motif must be induced"
    return edges,cycles,p,chosen

def cycle_key(edges,cycle,chosen):
    sub=collections.defaultdict(list)
    for e in cycle:
        v,w=edges[e]
        sub[v].append((w,e,1))
        sub[w].append((v,e,-1))
    pos=min(sub);prev=None
    winding=[0,0]
    for k in range(8):
        nxt,e,orient=next(t for t in sub[pos] if t[0]!=prev)
        if e in chosen:winding[chosen.index(e)]+=orient
        prev,pos=pos,nxt
    assert pos==min(sub)
    tup=tuple(winding)
    return min(tup,tuple(-x for x in tup))

def hamiltonian(edges,p,chosen,phi,t):
    # 80 vertex native Levi hopping, ONLY 12 motif edges held at 1.
    # Other 148 edges have amplitude t. 2 motif chords have phases.
    H=np.zeros((80,80),dtype=complex)
    patch_ids=set(p["support"])
    for eid,(a,b) in enumerate(edges):
        weight=1. if eid in patch_ids else t
        phase=float(phi[chosen.index(eid)]) if eid in chosen else 0.
        H[a,b]=-weight*np.exp(1j*phase)
        H[b,a]=np.conj(H[a,b])
    return H

def certificate():
    edges,cycles,p,chosen=build()
    # 40x40 native point/line incidence rank = 25.
    H0=hamiltonian(edges,p,chosen,(0.,0.),1.)
    singular=np.linalg.svd(H0[:40,40:],compute_uv=False)
    assert sum(singular>1e-9)==25
    assert abs(singular[0]-4)<1e-10
    assert sum(abs(singular-math.sqrt(6))<1e-9)==24
    assert sum(singular<1e-9)==15
    # ALL 1620 octagons -> exact winding/weight polynomials;
    # each coefficient records t^d, where d = outside motif edges.
    coeff=collections.defaultdict(lambda:[0]*9)
    for cycle in cycles:
        key=cycle_key(edges,cycle,chosen)
        d=sum(e not in set(p["support"]) for e in cycle)
        coeff[key][d]+=1
    assert sum(sum(poly) for poly in coeff.values())==1620
    assert coeff[(0,0)][0]==0
    assert sum(poly[0] for poly in coeff.values())==3
    nonzero={key:poly for key,poly in coeff.items() if key!=(0,0)}
    assert nonzero
    probes=[(0.,0.),(math.pi,math.pi),(2*math.pi/3,4*math.pi/3),(.4,2.1)]
    trace_checks=[]
    for t in (0.,.4,1.):
        base=hamiltonian(edges,p,chosen,(0.,0.),t)
        ev0=np.linalg.eigvalsh(base)
        tr0=float(sum(ev0**8))
        for phi in probes[1:]:
            ev=np.linalg.eigvalsh(hamiltonian(edges,p,chosen,phi,t))
            delta=float(sum(ev**8)-tr0)
            rhs=16*sum((sum(c*t**j for j,c in enumerate(poly)))*
                 (math.cos(key[0]*phi[0]+key[1]*phi[1])-1)
                 for key,poly in nonzero.items())
            assert abs(delta-rhs)<5e-6,(t,phi,delta,rhs)
            trace_checks.append({"outside_weight":t,"phases_pi":[v/math.pi for v in phi],
                "direct_tr_H8_difference":delta,"octagon_Fourier_prediction":rhs,
                "absolute_error":abs(delta-rhs)})
    # Realized half-filled 80-site free-fermion energy is sum of
    # lowest 40 one-body eigenvalues, even if N=40 many-body ground
    # state is degenerate due to exact flat bands.
    cases=[]
    for t in (0.,.25,.5,1.):
        cache={}
        calls=[0]
        def energy(z):
            phase=tuple(float(x%(2*math.pi)) for x in z)
            key=tuple(round(x,11) for x in phase)
            if key in cache:return cache[key]
            calls[0]+=1
            H=hamiltonian(edges,p,chosen,phase,t)
            ev=np.linalg.eigvalsh(H)
            e=float(sum(ev[:40]))
            cache[key]=e
            return e
        corners={k:energy(v) for k,v in {
          "zero":(0.,0.),"pi_pi":(math.pi,math.pi),
          "pi_0":(math.pi,0.),"0_pi":(0.,math.pi),
          "120":(2*math.pi/3,4*math.pi/3),
          "240":(4*math.pi/3,2*math.pi/3)}.items()}
        sols=[]
        for start in ((2*math.pi/3,4*math.pi/3),
                     (4*math.pi/3,2*math.pi/3),
                     (math.pi,math.pi),(math.pi,0.)):
            fit=minimize(energy,np.array(start),method="Nelder-Mead",
                    options={"xatol":1e-7,"fatol":1e-10,"maxiter":160})
            sols.append({"phase_pi":[float(x%(2*math.pi)/math.pi) for x in fit.x],
                "energy":float(fit.fun),"success":bool(fit.success)})
        best=min(sols,key=lambda x:x["energy"])
        if t==0:
            assert abs(corners["120"]-theoretical_energy(0))<1e-8
            assert abs(corners["120"]-corners["240"])<1e-9
        if t==1.:
            for phi in ((0,0),(math.pi,math.pi),
                        (2*math.pi/3,4*math.pi/3),(.43,1.4)):
                H=hamiltonian(edges,p,chosen,phi,1.)
                singular=np.linalg.svd(H[:40,40:],compute_uv=False)
                assert np.count_nonzero(singular<1e-9)>=13
        cases.append({"outside_edge_amplitude":t,
            "corner_and_120_ground_energies":corners,
            "best_multistart":best,"local_optimizer_runs":sols,
            "E120_minus_E_pi_pi":corners["120"]-corners["pi_pi"],
            "evaluated_matrix_count":calls[0]})
    return {
      "status":"PASS_TOE77_W33_EMBEDDED_THETA_EXTERIOR_FLUX",
      "W33_Levi_vertices_edges":[80,160],
      "native_theta_vertices_edges":[11,12],
      "complement_vertices":69,"external_links":148,
      "two_phase_chord_global_edge_ids":chosen,
      "full_incidence_rank_without_phases":25,
      "full_incidence_rank_max_with_two_phases":27,
      "full_80_vertex_exact_zero_mode_lower_bound":26,
      "rank_proof":"W33 Levi bipartite incidence 40x40 has exactly rank25, from squared singular eigenvalues 16^1,6^24,0^15. Two magnetic chord entries perturb its rank by <=2, so >=13 zero modes on each bipartite half, >=26 of the Hermitian 80x80 hopping Hamiltonian.",
      "native_1620_octagon_2chord_Fourier_multiplicity_by_outside_edges":{
         str(key):poly for key,poly in sorted(coeff.items())},
      "nonzero_winding_octagon_count":sum(sum(v) for v in nonzero.values()),
      "trace_H8_flux_dependence_formula":"Delta tr H(phi,t)^8 = 16 sum_C t^(number_edges_outside_patch) [cos(w_C.phi)-1], exact by Levi girth8",
      "trace_H8_independent_spectral_cross_checks":trace_checks,
      "outside_hopping_flux_scan":cases,
      "scientific_boundary":"At t=1 this is a bona-fide 80-site native W33 Levi free fermion model with two chosen magnetic chord phases, 40 fermions and 148 exterior links reinstated. The ground energy is a sum of lowest one-body eigenvalues, NOT a dynamical gauge action, 4D overlap-Dirac index or physical TOE. Local phase minima from Nelder-Mead are not rigorously global."}
if __name__=="__main__":
    c=certificate()
    out=ROOT/"data/w33_20261014_toe77_embedded_theta_exterior_flux.json"
    out.write_text(json.dumps(c,indent=2)+"\n")
    print(c["status"],"windings",c["nonzero_winding_octagon_count"])
    for z in c["outside_hopping_flux_scan"]:
        print("EMBED",z["outside_edge_amplitude"],
             "E120-Epi",z["E120_minus_E_pi_pi"],
             "best",z["best_multistart"])
