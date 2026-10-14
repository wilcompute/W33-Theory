"""TOE74 static U(1)^2 two-loop 11-site native interacting finite-T census.

Whole 462-state canonical 5-fermion space with exact Jordan-Wigner signs.
Ground energies use converged complex sparse eigensolver; partition
functions use full dense 462 eigenvalue spectra at four phase corners.
This is NOT dynamic Gauss-constrained matter or global three-deck W33.
"""
from __future__ import annotations
import itertools,json,sys,math
from pathlib import Path
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import eigsh
from scipy.special import logsumexp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe69_two_octagon_covariance import patch
from w33_20261014_toe73_eleven_site_ed import make_hamiltonian as old_Z2

def H_phi(p,phases,V):
    edges=p["p_ed"];chords=p["chords"];N=len(p["nodes"])
    states=[bits for bits in range(1<<N) if bits.bit_count()==5]
    idx={bits:i for i,bits in enumerate(states)}
    occ=np.asarray([[(b>>j)&1 for j in range(N)] for b in states],int)
    interactions=np.asarray([sum((o[a]-.5)*(o[b]-.5) for a,b in edges)
                             for o in occ])
    rows=list(range(len(states)));cols=list(range(len(states)))
    data=list(np.asarray(V*interactions,dtype=complex))
    for i,bits in enumerate(states):
        o=occ[i]
        for e,(a,b) in enumerate(edges):
            if o[a]==o[b]:continue
            dest=bits^(1<<a)^(1<<b)
            angle=phases[e]
            direction=1 if o[a] else -1
            jw=(-1)**sum((bits>>j)&1 for j in range(min(a,b)+1,max(a,b)))
            rows.append(i);cols.append(idx[dest])
            data.append(-jw*np.exp(1j*direction*angle))
    H=coo_matrix((data,(rows,cols)),shape=(len(states),len(states))).tocsr()
    herm=H-H.getH()
    assert herm.nnz==0 or max(abs(herm.data))<1e-12
    return H

def phases_for_chords(p,values):
    result=[0.0]*len(p["p_ed"])
    for e,phi in zip(p["chords"],values):result[e]=float(phi)
    return result

def small_eigs(H):
    val,vec=eigsh(H,k=2,which="SA",tol=1e-10,maxiter=15000)
    o=np.argsort(val)
    resid=max(float(np.linalg.norm(H@vec[:,i]-val[i]*vec[:,i])) for i in o)
    assert resid<1e-7
    return float(val[o[0]]),float(val[o[1]]-val[o[0]]),resid

def certificate():
    p=patch()
    corners=list(itertools.product((0.,np.pi),repeat=2))
    vals=(0.,.2,1.,4.)
    grid=[0,np.pi/4,np.pi/2,3*np.pi/4,np.pi]
    data=[]
    for V in vals:
        grid_rows=[]
        for a in grid:
            for b in grid:
                h=H_phi(p,phases_for_chords(p,(a,b)),V)
                ground,gap,res=small_eigs(h)
                grid_rows.append({"phase_pi_units":[float(a/np.pi),float(b/np.pi)],
                    "energy":ground,"gap":gap,"ritz_residual":res})
        winner=min(grid_rows,key=lambda r:r["energy"])
        corners_table=[]
        for a,b in corners:
            H=H_phi(p,phases_for_chords(p,(a,b)),V)
            exact_Z2,_o,_i=old_Z2(p,(int(round(a/np.pi)),int(round(b/np.pi))),V)
            assert float(abs((H-exact_Z2).data).max())<1e-12 if (H-exact_Z2).nnz else True
            # Complete finite-temperature trace, not thermal sampling.
            full=np.linalg.eigvalsh(H.toarray())
            assert len(full)==462 and np.max(abs(np.imag(full)))==0
            free={str(beta):float(-logsumexp(-beta*full)/beta)
                  for beta in (.5,1.,2.,8.)}
            corners_table.append({"phase_pi_units":[int(round(a/np.pi)),int(round(b/np.pi))],
               "ground":float(full[0]),"canonical_log_partition_free_energy":free,
               "same_N_gap":float(full[1]-full[0])})
        corner_best=min(corners_table,key=lambda r:r["ground"])
        assert winner["energy"]<=corner_best["ground"]+1e-7
        data.append({"V":V,"grid_5x5":grid_rows,
             "min_grid_holonomy":winner,
             "full_spectrum_four_corner_free_energies":corners_table,
             "best_Z2_corner":corner_best["phase_pi_units"]})
    # Gauge invariance under site-dependent phase redefinitions:
    # edge angle phi_ab -> phi_ab+theta_b-theta_a.
    test_p=phases_for_chords(p,(np.pi/3,2*np.pi/5))
    theta=np.array([.07*j+.03*(j*j)%1 for j in range(len(p["nodes"]))])
    rotated=[ang+theta[b]-theta[a] for ang,(a,b) in zip(test_p,p["p_ed"])]
    original=H_phi(p,test_p,V=1.)
    gauged=H_phi(p,rotated,V=1.)
    # A deterministic unitary change of Fock basis gives identical spectra.
    e0,g0,_=small_eigs(original);e1,g1,_=small_eigs(gauged)
    assert abs(e0-e1)<1e-8 and abs(g0-g1)<1e-8
    # Time reversal: H(-phi)=complex conjugate of H(phi), spectra identical.
    em,gm,_=small_eigs(H_phi(p,[-z for z in test_p],V=1.))
    assert abs(em-e0)<1e-8 and abs(gm-g0)<1e-8
    return {"status":"PASS_TOE74_NATIVE_U1_INTERACTING_FINITE_T",
      "native_sites_links":[11,12],
      "fermions":5,"Fock_dim":462,
      "flux_chords":list(p["chords"]),
      "finite_phase_grid_pi_units":[0,.25,.5,.75,1.],
      "V_scans":data,
      "finite_temperature_inverse_beta":[.5,1,2,8],
      "gauge_rephasing_spectrum_invariance":True,
      "time_reversal_spectrum_invariance":True,
      "comparison":"Static U1^2 chord holonomy with spinless density repulsion; finite canonical 462-state exact-sector matrix, numerical eigsh for 5x5 grids and full eigenvalue trace for corners.",
      "limitation":"Grid minima need not be continuous global minima. Canonical free energies are finite-size static-gauge matter quantities, NOT a dynamical Gauss-constrained gauge partition function, 80-site phase diagram, or physical TOE."}

if __name__=="__main__":
    out=certificate()
    (ROOT/"data/w33_20261014_toe74_u1_manybody_finite_t.json").write_text(
        json.dumps(out,indent=2)+"\n")
    print(out["status"],[(x["V"],x["min_grid_holonomy"]["phase_pi_units"],x["best_Z2_corner"]) for x in out["V_scans"]])
