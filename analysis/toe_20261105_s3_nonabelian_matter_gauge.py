#!/usr/bin/env python3
"""Minimal D3=S3 two-loop non-Abelian gauge rotor with two color doublets.

One vertex, two oriented loop holonomies, and two distinguishable 2D
matter degrees of freedom transforming under the standard real irrep.
Gauge transformation simultaneously conjugates holonomies and rotates
matter. Exact group averaging yields a 27-dimensional physical sector.
This is a toy finite gauge theory, NOT an SU(2) or SM continuum theory.
"""
from __future__ import annotations
import itertools, json, math
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261105_s3_nonabelian_matter_gauge.json"
PERMS=list(itertools.permutations(range(3)))
INDEX={x:i for i,x in enumerate(PERMS)}
IDENT=(0,1,2)
TRANS=[p for p in PERMS if sum(p[i]!=i for i in range(3))==2]
assert len(TRANS)==3
def mul(p,q):return tuple(p[q[i]] for i in range(3))
def inv(p):return tuple(p.index(i) for i in range(3))
def irrep():
    basis=np.array([[1/math.sqrt(2),1/math.sqrt(6)],
                    [-1/math.sqrt(2),1/math.sqrt(6)],
                    [0,-2/math.sqrt(6)]])
    reps=[]
    for p in PERMS:
        x=np.zeros((3,3))
        for i in range(3):x[p[i],i]=1
        reps.append(basis.T@x@basis)
    for i,p in enumerate(PERMS):
        for j,q in enumerate(PERMS):
            assert np.max(np.abs(reps[INDEX[mul(p,q)]]-reps[i]@reps[j]))<2e-15
    return reps
def build():
    reps=irrep()
    n=6*6*4
    gauge=[]
    for h in PERMS:
        u=np.zeros((n,n))
        hin=inv(h)
        color=np.kron(reps[INDEX[h]],reps[INDEX[h]])
        for i,g in enumerate(PERMS):
            gi=INDEX[mul(mul(h,g),hin)]
            for j,k in enumerate(PERMS):
                kj=INDEX[mul(mul(h,k),hin)]
                u[4*(6*gi+kj):4*(6*gi+kj)+4,
                  4*(6*i+j):4*(6*i+j)+4]=color
        assert np.max(abs(u.T@u-np.eye(n)))<2e-14
        gauge.append(u)
    project=sum(gauge)/6
    assert np.max(abs(project-project.T))<3e-14
    assert np.max(abs(project@project-project))<3e-14
    traces=[float(np.trace(u)) for u in gauge]
    assert sorted(round(t) for t in traces)==[0,0,0,9,9,144]
    assert abs(np.trace(project)-27)<1e-12
    E=np.zeros((n,n)); M=np.zeros((n,n)); C=np.zeros((n,n))
    for i,g in enumerate(PERMS):
        for j,k in enumerate(PERMS):
            q=6*i+j; a=slice(4*q,4*q+4)
            for t in TRANS:
                ti=INDEX[mul(t,g)]
                tj=INDEX[mul(t,k)]
                E[a,slice(4*(6*ti+j),4*(6*ti+j)+4)]-=np.eye(4)/3
                E[a,slice(4*(6*i+tj),4*(6*i+tj)+4)]-=np.eye(4)/3
            comm=mul(mul(mul(g,k),inv(g)),inv(k))
            chi=float(np.trace(reps[INDEX[comm]]))
            M[a,a]=-(chi/2)*np.eye(4)
            color_g=(reps[i]+reps[i].T)/2
            color_k=(reps[j]+reps[j].T)/2
            C[a,a]=-0.5*(np.kron(color_g,np.eye(2))+
                          np.kron(np.eye(2),color_k))
    for name,op in (("electric",E),("magnetic",M),("matter",C)):
        assert np.max(abs(op-op.T))<1e-12,name
        for u in gauge:
            assert np.max(abs(op@u-u@op))<3e-13,(name,"not gauge invariant")
        assert np.max(abs(op@project-project@op))<3e-13,name
    em_norm=float(np.linalg.norm(E@M-M@E))
    ec_norm=float(np.linalg.norm(E@C-C@E))
    assert em_norm>10 and ec_norm>5
    w,b=np.linalg.eigh(project)
    physical=b[:,w>.5]
    assert physical.shape==(144,27)
    assert np.max(abs(physical.T@physical-np.eye(27)))<1e-12
    records=[]
    for J,K,g in ((1,0,0),(0.5,1,.3),(1,.4,.7),(.1,1,1)):
        H=J*E+K*M+g*C
        Hp=physical.T@H@physical
        levels,vec=np.linalg.eigh(Hp)
        psi=physical@vec[:,0]
        gauss_error=float(max(np.linalg.norm((u-np.eye(n))@psi) for u in gauge))
        assert gauss_error<3e-12
        records.append(dict(J=J,K=K,matter_g=g,
            lowest_four_eigenvalues=levels[:4].tolist(),
            ground_gap=float(levels[1]-levels[0]),
            ground_magnetic_expectation=float(psi@M@psi),
            ground_matter_expectation=float(psi@C@psi),
            max_Gauss_invariance_error=gauss_error))
    return dict(
        status="PASS_NONABELIAN_S3_TWO_LOOP_TWO_MATTER_GAUSS_INVARIANT_SPECTRAL_MODEL",
        group="D3 isomorphic S3",group_order=6,
        gauge_links=2,distinguishable_color_doublet_matter_fields=2,
        raw_hilbert_dimension=n,physical_gauge_invariant_dimension=27,
        pure_gauge_orbital_dimension=11,
        Burnside_trace_census={"identity":144,"each_transposition":0,
                                "each_three_cycle":9,"projected_rank":27},
        electric_magnetic_commutator_frobenius=em_norm,
        electric_matter_commutator_frobenius=ec_norm,
        exact_projector_and_Gauss_constraints=True,
        model_operator="H=J E + K M + g C with electric conjugacy-class shifts, magnetic commutator character and loop-matter symmetric color couplings",
        scans=records,
        nonidentification="The numerical dimension 27 coincides with the W33 affine history and three-qutrit Hilbert dimension but gives no canonical H27/W33 intertwiner, ray identification, relativistic gauge group, particle spectrum or continuum limit.",
        prior_art="Finite-group Hamiltonian lattice gauge theory and group projection are established. This 2-loop S3 color-doublet implementation and coincidence check are repo-local.")
def main():
    result=build()
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("PASS S3 non-Abelian Gauss rank",result["physical_gauge_invariant_dimension"])
    print("E-B commutator",result["electric_magnetic_commutator_frobenius"])
    print("CERTIFICATE",OUT)
    return result
if __name__=="__main__":main()
