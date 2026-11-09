#!/usr/bin/env python3
"""No-go: balanced gapped chiral incidence Dirac family has zero 2D Chern.

For a periodic invertible B(theta,phi), H=[[0,B],[B†,0]],
the -energy occupied bundle admits global smooth periodic orthonormal
frame ( -polar(B) v, v )/sqrt(2). Its first Chern class is zero.
The demonstration is W33-specific for graph construction; the theorem
is standard class AIII topology, not an original 3+1D chiral no-go.
"""
import json,math,sys
from pathlib import Path
import numpy as np
from w33_20261109_five_fronts import geometry

def incidence():
    _,lines,rows=geometry()
    B=np.zeros((40,40),complex)
    for i,neighbors in enumerate(rows):
        for j in neighbors:B[i,j]=1
    assert (B!=0).sum()==160
    return B

def polarframe(C):
    U,s,Vh=np.linalg.svd(C,full_matrices=False)
    unitary=U@Vh
    frame=np.vstack([-unitary,np.eye(40)])/np.sqrt(2)
    assert np.max(abs(frame.conj().T@frame-np.eye(40)))<1e-11
    return frame,float(min(s))

def eigband_test(C):
    V,gap=polarframe(C)
    H=np.block([[np.zeros((40,40)),C],[C.conj().T,np.zeros((40,40))]])
    neg=np.linalg.eigh(H)[0][:40]
    assert max(neg)<-gap+1e-9
    chiral=np.diag(np.r_[np.ones(40),-np.ones(40)])
    assert np.max(abs(H@chiral+chiral@H))<1e-14
    return gap

def torus_test(n=13):
    rng=np.random.default_rng(20261109248)
    B=incidence()
    theta=rng.uniform(-np.pi,np.pi,(40,40))
    B0=np.where(abs(B)>0,np.exp(1j*theta),0)
    edges=np.argwhere(abs(B0)>0)
    i,j=edges[0];p,q=edges[19]
    assert (i,j)!=(p,q)
    # Make the two externally selected hopping amplitudes weak but
    # keep all hoppings pure U(1) phase-twisted at fixed modulus.
    base=B0.copy()
    base[i,j]=0
    base[p,q]=0
    s0=min(np.linalg.svd(base,compute_uv=False))
    assert s0>1e-5
    delta=s0/16
    def C(x,y):
        Z=base.copy()
        Z[i,j]=delta*np.exp(1j*x)
        Z[p,q]=delta*np.exp(1j*y)
        return Z
    frames={}
    gaps=[]
    for t in range(n):
        for s in range(n):
            V,gap=polarframe(C(2*np.pi*t/n,2*np.pi*s/n))
            frames[t,s]=V
            gaps.append(gap)
    assert min(gaps)>=s0-2*delta-1e-10
    # Fukui-Hatsugai-Suzuki lattice Chern number: unitary part of
    # determinant overlap of global occupied frames.
    links={}
    for t in range(n):
        for s in range(n):
            F=frames[t,s]
            phases=[]
            for t2,s2 in (((t+1)%n,s),(t,(s+1)%n)):
                O=F.conj().T@frames[t2,s2]
                sign,logdet=np.linalg.slogdet(O)
                assert abs(sign)>1-1e-10
                phases.append(sign)
            links[t,s]=phases
    flux=[]
    for t in range(n):
        for s in range(n):
            ux,uy=links[t,s]
            uyx=links[(t+1)%n,s][1]
            uxy=links[t,(s+1)%n][0]
            flux.append(np.angle(ux*uyx/(uxy*uy)))
    chern=sum(flux)/(2*np.pi)
    assert abs(chern)<1e-9
    eigband_test(C(0.,0.))
    result={
      "status":"PASS_W33_CHIRAL_AIII_GAPPED_TWO_TWIST_CHERN_ZERO",
      "native_W33_incidence_vertices":80,
      "bipartite_incidence_rows":40,
      "bipartite_incidence_cols":40,
      "nonzero_graph_edges":160,
      "two_torus_grid_shape":[n,n],
      "random_phase_seed":20261109248,
      "two_twisted_graph_edges":[[int(i),int(j)],[int(p),int(q)]],
      "full_rank_base_with_two_weak_edges_removed_min_singular":float(s0),
      "phase_twists_fixed_hopping_modulus":True,
      "twist_amplitude":float(delta),
      "analytical_gap_lower":float(s0-2*delta),
      "sampled_min_gap":float(min(gaps)),
      "berry_curvature_max_plaquette_abs":float(max(abs(x) for x in flux)),
      "sampled_first_chern_number":float(chern),
      "exact_chiral_anticommutator_zero_for_all_twists":True,
      "global_negative_energy_occupied_frame":"1/sqrt(2) * vstack([-polar(B(theta,phi)),I_40])",
      "topological_proof":"For any continuous periodic invertible square B(theta,phi), polar(B) is continuous and periodic, giving a global frame of all occupied negative-energy states; the first Chern class on the 2-torus vanishes identically. This is a standard class-AIII even-dimensional obstruction.",
      "scope":"Only balanced, gapped, bipartite offdiagonal Dirac models. Does not exclude chiral 3D topological AIII winding, modified gauge theories, mass-breaking class-A Chern systems, overlap fermions, or an actual 3+1D emergent chiral continuum. The two twist parameters themselves are externally imposed.",
      "not_TOE":True}
    return result

def main(path=None):
    data=torus_test()
    if path:Path(path).write_text(json.dumps(data,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("PASS W33 AIII chiral Chern",json.dumps({
       "chern":data["sampled_first_chern_number"],
       "min_gap":data["sampled_min_gap"],
       "gap_bound":data["analytical_gap_lower"]}))
    return data
if __name__=="__main__":
    main(sys.argv[1] if len(sys.argv)>1 else None)
