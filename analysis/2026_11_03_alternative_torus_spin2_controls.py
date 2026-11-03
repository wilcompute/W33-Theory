#!/usr/bin/env python3
"""Independent finite 4D lattice Lorentz/TT positive controls and dimension no-go.

A four-dimensional torus spatial+Euclidean-time product exhibits a controlled
intermediate heat spectral dimension; its four axes were GIVEN, not generated.
On 3D spatial Fourier modes, TT projector has rank 2; it is IMPOSED rather
than derived by a graph Hessian.
"""
from pathlib import Path
import numpy as np,math,json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"2026_11_03_torus_lorentz_tt_controls.json"
pairs=[(0,0),(1,1),(2,2),(0,1),(0,2),(1,2)]
def makeh(v):
    H=np.zeros((3,3))
    for a,(i,j) in enumerate(pairs):H[i,j]=H[j,i]=v[a]
    return H
def tomode(H):return np.array([H[i,j] for i,j in pairs])
def tt(h,k):
    n=k/np.linalg.norm(k)
    P=np.eye(3)-np.outer(n,n)
    return P@h@P-np.trace(P@h@P)*P/2
def run():
    checks=[]
    for L in (8,16,32,64,128):
        e=2-2*np.cos(2*np.pi*np.arange(L)/L)
        for D in (2,3,4):
            for t in (2.,8.,12.):
                E=np.exp(-t*e)
                ds=2*D*t*np.dot(e,E)/sum(E)
                checks.append({"side":L,"input_dimension":D,
                   "diffusion_time_lattice_units":t,"spectral_dimension":float(ds)})
    # A 4D lattice can show a scaling window near 4, but the dimension
    # was selected in the number of Cartesian factors from the outset.
    mid=next(x for x in checks if x["side"]==128 and x["input_dimension"]==4 and x["diffusion_time_lattice_units"]==12.)
    assert 3.99<mid["spectral_dimension"]<4.2,mid
    # Spatial 3D wave: central differences yield omega(k)=2c/a sqrt(sum sin²(k_i a/2)).
    dispersion=[]
    for L in (8,16,32,64,128):
        a=2*np.pi/L
        w=[]
        for k in ((3,0,0),(2,2,1)):
            omega=2/a*np.sqrt(sum(np.sin(np.array(k)*a/2)**2))
            w.append(float(omega))
        dispersion.append({"side":L,"a":a,"omega_axis":w[0],
          "omega_oblique_same_continuum_k":w[1],
          "relative_directional_dispersion_anisotropy":abs(w[0]-w[1])/3,
          "relative_axis_error_vs_omega_eq_c_abs_k":abs(w[0]-3)/3})
    assert all(dispersion[i+1]["relative_directional_dispersion_anisotropy"]<
               dispersion[i]["relative_directional_dispersion_anisotropy"] for i in range(4))
    ttchecks=[]
    for k in (np.array([1.,0,0]),np.array([1.,2,3]),np.array([2.,2.,1.])):
        Q=np.column_stack([tomode(tt(makeh(np.eye(6)[j]),k)) for j in range(6)])
        assert np.max(abs(Q@Q-Q))<1e-10
        assert np.linalg.matrix_rank(Q,tol=1e-9)==2
        assert np.linalg.norm(tomode(tt(np.eye(3),k)))<1e-12
        for j in range(3):
            xi=np.eye(3)[j]
            gauge=np.outer(k,xi)+np.outer(xi,k)
            assert np.linalg.norm(tt(gauge,k))<1e-12
        ttchecks.append({"k":k.tolist(),"symmetric_tensor_dim":6,
           "transverse_traceless_rank":2,
           "projector_idempotence_max":float(np.max(abs(Q@Q-Q))),
           "imposed_projector_not_dynamical":True})
    # A fixed-N hypercubic refinement graph cost lambda E gives
    # E/N=D. For lambda != 0, the cost strictly monotone in D.
    costs={str(D):D for D in range(1,7)}
    out={"status":"PASS_SUPPLIED_4D_TORUS_CONTINUUM_AND_TWO_HELICITY_CONSTRAINT_TESTS",
       "heat_spectral_dimension":checks,
       "mid_heat_regime":mid,
       "central_difference_wave_dispersion":dispersion,
       "tensor_tt_constraints":ttchecks,
       "graph_selection_linear_edge_cost":{"energy_per_site_if_single_edge_weight":costs,
          "no_go":"A free energy depending solely on positive constant times edge count N*D selects lowest D; with negative coefficient selects highest D. No interior 3-space/4-spacetime dimensionality can be selected by this single term without extra competing dynamics or boundary restrictions."},
       "interpretation":"A 4D Cartesian torus supplies the intended approximate Euclidean spectral dimension; independent temporal wave equation and 3D spatial differences supply a causal cone approximation and two-helicity TT projector only after extra structures are supplied.",
       "negative_controls":"D=2,3 heat traces; axis versus oblique lattice dispersion; rank-six symmetric tensor before projection versus rank-two TT after projection.",
       "scope":"No dynamical graph-growth action, Einstein gravity, nonlinear diffeomorphism constraints, universality of matter coupling, derivation of dimension/time, Lorentzian signature from graph alone, or physical graviton established.",
       "references":["https://doi.org/10.1103/PhysRev.135.B1049","https://link.springer.com/article/10.1007/s41114-026-00064-9"]}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print("4D HEAT",mid["spectral_dimension"],"TT",ttchecks,"ANISO",dispersion[-1]["relative_directional_dispersion_anisotropy"])
    return out
if __name__=="__main__":run()
