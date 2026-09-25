#!/usr/bin/env python3
from __future__ import annotations
import itertools, json, math, sys
from collections import Counter
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
OUT=ROOT/"data/w33_20260924_tetracode_spectral_mu12_clock.json"

from analysis.w33_affine_tetracode_e8_glue_bridge import (
    STANDARD_TETRACODE_GENERATORS,
)
from analysis.w33_20260924_null_hesse_4a2_s4_intertwiner import NULLS
from analysis.w33_20260924_null_history_spectral_clock import (
    adjacency, fourier_eigenvalue, sym2_rep, inv3,
)
from analysis.w33_20260924_temporal_maslov_mu12 import (
    weil_phase, root12_exponent,
)

W=np.exp(2j*np.pi/3)
TOL=3e-10
V=list(itertools.product(range(3),repeat=3))
VID={v:i for i,v in enumerate(V)}
def span(gens):
    out=set()
    for coeff in itertools.product(range(3),repeat=len(gens)):
        v=np.zeros(len(gens[0]),dtype=int)
        for a,g in zip(coeff,gens):
            v=(v+a*np.array(g,dtype=int))%3
        out.add(tuple(map(int,v)))
    return sorted(out)

def dual_action(M,k):
    return tuple(map(int,(inv3(M).T@np.array(k,dtype=int))%3))

def orbit(seed,M):
    out=[]
    y=seed
    while y not in out:
        out.append(y)
        y=dual_action(M,y)
    return out

def spectral_phase(leval):
    z=np.exp(-1j*(2*math.pi/9)*leval)
    if abs(z-1)<TOL: return "1"
    if abs(z-W)<TOL: return "omega"
    if abs(z-W**2)<TOL: return "omega^2"
    raise AssertionError(z)

def mu12_generated(exponents):
    return sorted({sum(c*e for c,e in zip(cs,exponents))%12
                   for cs in itertools.product(range(12),repeat=len(exponents))})
def main():
    T=span(STANDARD_TETRACODE_GENERATORS)
    Amap=np.array(NULLS,dtype=int).T%3
    P=sorted({
        tuple(map(int,(Amap@np.array(v,dtype=int))%3))
        for v in T
    })
    assert len(P)==9
    assert set(P)=={(0,b,c) for b in range(3) for c in range(3)}

    # Primal support audit: the nine basis states are not an invariant subspace.
    A=adjacency()
    pids=[VID[x] for x in P]
    outside=[i for i in range(27) if i not in pids]
    induced=A[np.ix_(pids,pids)]
    cross=A[np.ix_(pids,outside)]
    assert set(map(int,induced.sum(axis=1)))=={2}
    assert int(induced.sum()//2)==9
    assert set(map(int,cross.sum(axis=1)))=={6}
    assert int(cross.sum())==54

    # Functions constant on P-cosets form the canonical 3D quotient.
    Pperp=sorted([
        k for k in V
        if all(sum(k[i]*p[i] for i in range(3))%3==0 for p in P)
    ])
    assert Pperp==[(0,0,0),(1,0,0),(2,0,0)]
    fixed_rows=[]
    for k in Pperp:
        leval=8-fourier_eigenvalue(k)
        ph,rank,det=weil_phase(k)
        fixed_rows.append({
          "k":list(k),"L_eigenvalue":leval,
          "spectral_phase":spectral_phase(leval),
          "maslov_mu12_exponent":root12_exponent(ph),
          "rank":rank,"determinant":det,
        })
    assert all(r["spectral_phase"]=="1" for r in fixed_rows)
    assert sorted(r["maslov_mu12_exponent"] for r in fixed_rows)==[0,3,9]
    # Tetracode C3 in the common P1(F3) action; use contragredient action on Fourier labels.
    G=np.array([[1,0],[1,1]],dtype=int)
    R=sym2_rep(G)
    assert np.array_equal(np.linalg.matrix_power(R,3)%3,np.eye(3,dtype=int)%3)
    assert all(dual_action(R,k)==k for k in Pperp)

    primal_dual_images={dual_action(R,k) for k in P}
    primal_dual_preserved=primal_dual_images==set(P)
    assert not primal_dual_preserved

    # Enumerate C3 orbits in dual space and choose a smallest omega orbit.
    seen=set()
    orbits=[]
    for k in V:
        if k in seen: continue
        O=orbit(k,R)
        seen.update(O)
        levals={8-fourier_eigenvalue(x) for x in O}
        phases={spectral_phase(v) for v in levals}
        maslov={root12_exponent(weil_phase(x)[0]) for x in O}
        orbits.append({
          "points":O,"size":len(O),
          "L_eigenvalues":sorted(levals),
          "spectral_phases":sorted(phases),
          "maslov_exponents":sorted(maslov),
        })
    omega_orbits=[o for o in orbits if o["spectral_phases"]==["omega"]]
    assert omega_orbits and min(o["size"] for o in omega_orbits)==3
    chosen=min((o for o in omega_orbits if o["size"]==3),
               key=lambda o:o["points"])
    extension=Pperp+chosen["points"]
    assert len(set(extension))==6
    phase_hist=Counter()
    maslov_hist=Counter()
    for k in extension:
        leval=8-fourier_eigenvalue(k)
        phase_hist[spectral_phase(leval)]+=1
        maslov_hist[root12_exponent(weil_phase(k)[0])]+=1
    assert phase_hist==Counter({"1":3,"omega":3})
    assert mu12_generated([4,3])==list(range(12))

    out={
      "schema":"w33.20260924.tetracode_spectral_mu12_clock.v2",
      "status":"PASS_TETRACODE_CLOCK_DUALITY_FIXED3_WITH_MINIMAL_C3_MU12_EXTENSION",
      "primal_tetracode_plane":{
        "description":"P={(0,b,c): b,c in F3}",
        "states":len(P),
        "induced_null_graph":"3 disjoint triangles",
        "internal_degree":2,
        "internal_edges":9,
        "external_degree_each":6,
        "cross_edges":54,
        "basis_support_subspace_dynamically_invariant":False,
      },
      "canonical_fourier_quotient":{
        "construction":"functions constant on cosets of P; Fourier support P^perp",
        "dimension":len(Pperp),
        "P_perp":[list(x) for x in Pperp],
        "spectral_clock_action":"identity at t*=2*pi/9",
        "rows":fixed_rows,
        "maslov_exponents":[r["maslov_mu12_exponent"] for r in fixed_rows],
        "phase_group_inside_fixed_sector":"mu_4 generated by i",
      },
      "C3":{
        "history_matrix":R.astype(int).tolist(),
        "dual_action":"k -> R^{-T} k",
        "fixes_P_perp_pointwise":True,
        "primal_plane_not_preserved_by_dual_action":True,
        "dual_orbits":orbits,
      },
      "minimal_mu12_extension":{
        "dimension":6,
        "added_C3_orbit":[list(x) for x in chosen["points"]],
        "added_orbit_size":chosen["size"],
        "added_L_eigenvalue":chosen["L_eigenvalues"][0],
        "added_spectral_phase":"omega",
        "phase_dimensions":{
          "1":phase_hist["1"],
          "omega":phase_hist["omega"],
          "omega^2":phase_hist["omega^2"],
        },
        "maslov_histogram":{str(k):v for k,v in sorted(maslov_hist.items())},
        "generators_mu12_indices":{"omega":4,"i":3},
        "generated_mu12_indices":mu12_generated([4,3]),
        "minimality":"outside the 3 fixed modes every nontrivial C3 orbit has size 3",
      },
      "theorem":(
        "The nine tetracode history addresses form a primal translation subgroup P, "
        "but their delta-function basis span is not invariant under the null-history "
        "Laplacian. The canonical spectral object is instead the 3D coset-constant "
        "quotient with Fourier support P^perp. The order-three clock fixes P^perp "
        "pointwise at t*=2*pi/9, and its Maslov phases are 1,+i,-i. The tetracode "
        "C3 fixes these three dual modes pointwise. Adding one smallest nontrivial "
        "C3 orbit with Laplacian eigenvalue 6 contributes three omega modes, giving "
        "a minimal 6D C3-invariant sector containing both i and omega and hence all "
        "of mu_12."
      ),
      "boundary":(
        "This is a finite Fourier/module statement. The primal nine-history plane "
        "must not be conflated with an identically labelled Fourier-mode plane, and "
        "the 6D extension is a control/spectral sector rather than a new physical "
        "spacetime dimension."
      ),
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
      "status":out["status"],
      "fixed":out["canonical_fourier_quotient"]["P_perp"],
      "added":out["minimal_mu12_extension"]["added_C3_orbit"],
      "phase_dimensions":out["minimal_mu12_extension"]["phase_dimensions"],
    },indent=2,sort_keys=True))

if __name__=="__main__":
    main()
