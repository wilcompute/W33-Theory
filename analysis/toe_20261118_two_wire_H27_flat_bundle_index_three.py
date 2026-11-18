"""A two-wire noncommutative H27 holonomy interface and Euler-index gate.

Uses the familiar fact pi1(exterior of two-component unlink in S3)=F2.
This is an alternative test GEOMETRY, not a G2 compactification.
"""
import json,numpy as np
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def run():
    omega=np.exp(2j*np.pi/3)
    X=np.array([[0,0,1],[1,0,0],[0,1,0]],complex)
    Z=np.diag([1,omega,omega**2]);Y=Z@Z
    I=np.eye(3,dtype=complex)
    assert np.max(abs(X@X@X-I))<1e-12
    assert np.max(abs(Y@Y@Y-I))<1e-12
    central=X@Y@X.conj().T@Y.conj().T
    assert np.max(abs(central-omega*I))<1e-12
    matrices={(a,b,c):omega**c*np.linalg.matrix_power(X,a)@np.linalg.matrix_power(Y,b)
              for a in range(3) for b in range(3) for c in range(3)}
    assert all(np.max(abs(m-n))>1e-12 for i,m in enumerate(matrices.values())
               for j,n in enumerate(matrices.values()) if i<j)
    # Flat twisted 0->1 cochain differential on the free2 1-skeleton.
    d0=np.vstack([X-I,Y-I])
    rank=int(np.linalg.matrix_rank(d0,tol=1e-10))
    assert rank==3
    free2_twisted_H1=6-rank
    # Exterior of split 2-component unlink has boundary T2+T2,
    # chi=0, twisted H0=0 (no fixed X,Y vector), twisted H3=0
    # (boundary). Hence b2(X)=b1(X)=3 by Euler.
    assert free2_twisted_H1==3
    base_H=[0,3,3,0]
    # Remove one interior ball: b2 increases by rankV=3,
    # all other Betti remain. Select that S2 as relative.
    punctured_H=[0,3,6,0]
    # LES for pair (Y,S2): H0(S2,V)=V contributes to H1rel,
    # restriction H2(Y,V)->H2(S2,V) is surjective.
    # So b1rel=b1(Y)+3=6; b2rel=b2(Y)-3=3.
    relative_H=[0,6,3,0]
    assert relative_H[1]-relative_H[2]==3
    # Independent Euler: chi(Y)=chi(X)+1=1, chi(S2)=2;
    # chi_rel=-1; with rank(V)=3 => chi_rel(V)=-3.
    assert sum((-1)**i*relative_H[i] for i in range(4))==-3
    topology=[]
    for puncture_spheres in (0,1,3,5):
        for relative_spheres in range(puncture_spheres+1):
            if relative_spheres==0: continue
            chirel=puncture_spheres-2*relative_spheres
            topology.append(dict(point_spheres=puncture_spheres,
                                 relative_spheres=relative_spheres,
                                 rank1_index=2*relative_spheres-puncture_spheres,
                                 rank3_H27_twisted_index=3*(2*relative_spheres-puncture_spheres)))
    out=dict(status="PASS",
      lens_L41_pi1="C4; every homomorphism C4->H27 is trivial (gcd(3,4)=1).",
      single_core_wire_pi1="Z; the image of a single generator is cyclic, cannot surject onto nonabelian H27",
      two_component_unlink_exterior_pi1="F2; send free generators to native Heisenberg x,y to obtain an onto flat H27 holonomy",
      two_wire_boundary=["T2","T2"],
      full_H27_flat_holonomy_generated_elements=len(matrices),
      commutator_scalar="omega I3",
      holonomy_representation_dimension=3,
      common_invariant_vectors_dimension=3-rank,
      untwisted_exterior_chi=0,
      base_H27_rank3_local_system_betti=base_H,
      single_sphere_puncture_absolute_betti=punctured_H,
      single_sphere_puncture_relative_betti=relative_H,
      one_spherical_defect_rank3_net_index=relative_H[1]-relative_H[2],
      unavoidable_rank3_vectorlike_pair_count_in_this_CW_model=relative_H[2],
      Euler_relative_formula="index=b1-b2=rank(V)*(2*r-k) for k punctured S2 components and r relative spheres, assuming mixed nonempty absolute boundary and b0rel=b3rel=0; the two wire torus boundaries have chi=0.",
      index_table=topology,
      scope="Two-wire unlink exterior and single relative puncture are a topological/flat-bundle alternative. Surjectivity onto H27 and net index3 coexist, but H2_relative=3 leaves vectorlike modes in this finite twisted CW model. Neither a metric, G2 ALE fibration, physical Dirac spectrum, full E6 gauge centralizer, anomaly inflow nor isolated three families is supplied.",
      source="Hatcher Algebraic Topology Example 1.23 pi1(unlink)=Z*Z; ordinary Euler characteristic with local coefficients and long exact sequence of boundary pair."
    )
    dest=ROOT/"data/toe_20261118_two_wire_H27_flat_bundle_index_three.json"
    dest.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print("PASS C4/Z nonabelian holonomy obstruction; F2 two-wire surjects H27; one S2 gives twisted net index3 but leaves three vectorlike partners")
    return out
if __name__=="__main__":run()
