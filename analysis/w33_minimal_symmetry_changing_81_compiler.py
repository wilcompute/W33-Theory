#!/usr/bin/env python3
"""Construct a minimal symmetry-changing 81-state compiler in K-Fourier coordinates.

Source:
  Reg(K), K = H27 x C3_external.

Target:
  9 V_omega tensor Reg(C3_external).

The exact K-equivariant rank ceiling is 27, so any invertible 81-state compiler
must change representation type on at least 54 coordinates.

In the source group-Fourier basis use coordinates
  S1(t,r,i): V_omega at external character t, regular multiplicity r, component i;
  S2(t,r,i): V_omega^2 at external character t;
  L(u,v,t): the 27 one-dimensional characters.

In the target operator basis use coordinates
  O(t,m,i), t in F3_external, m in {0,...,8} multiplicity, i in F3_internal.

The deterministic compiler is:
  S1(t,r,i) -> O(t,r,i)                 for r=0,1,2        (27 equivariant coords)
  S2(t,r,i) -> O(t,3+r,i)               for r=0,1,2        (27 retyped coords)
  L(u,v,t)  -> O(t,6+u,v)                                      (27 retyped coords)

This is a permutation matrix in Fourier coordinates, hence unitary. Exactly 54
coordinates change irrep type, saturating the lower bound 81-27=54.

Boundary: this is an explicit Fourier-coordinate compiler. It does not claim
that the root hybrid basis itself equals the K-Fourier basis without the
separate Fourier analysis transform, nor that the 54 retyped coordinates arise
from a physical interaction.
"""
from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_minimal_symmetry_changing_81_compiler.json"

def canonical(x):
    return json.dumps(x,sort_keys=True,separators=(",",":"))

def main(write=True):
    budget=json.loads((ROOT/"data/w33_hybrid81_operator_equivariance_budget.json").read_text())
    assert budget["equivariant_map_budget"]["maximum_ranks"]["full81_to_operator81"]==27
    assert budget["equivariant_map_budget"]["full_equivariance_deficit"]==54

    records=[]
    targets=set()
    sources=set()

    for t in range(3):
        for r in range(3):
            for i in range(3):
                source=["S1",t,r,i]
                target=[t,r,i]
                records.append({"source":source,"target":target,"mode":"equivariant"})
                sources.add(tuple(source));targets.add(tuple(target))
        for r in range(3):
            for i in range(3):
                source=["S2",t,r,i]
                target=[t,3+r,i]
                records.append({"source":source,"target":target,"mode":"retyped_central"})
                sources.add(tuple(source));targets.add(tuple(target))
        for u in range(3):
            for v in range(3):
                source=["L",u,v,t]
                target=[t,6+u,v]
                records.append({"source":source,"target":target,"mode":"retyped_abelian"})
                sources.add(tuple(source));targets.add(tuple(target))

    assert len(records)==len(sources)==len(targets)==81
    mode_counts={}
    for row in records:mode_counts[row["mode"]]=mode_counts.get(row["mode"],0)+1
    assert mode_counts=={"equivariant":27,"retyped_central":27,"retyped_abelian":27}

    changed=mode_counts["retyped_central"]+mode_counts["retyped_abelian"]
    lower_bound=81-budget["equivariant_map_budget"]["maximum_ranks"]["full81_to_operator81"]
    assert changed==lower_bound==54

    digest="sha256:"+hashlib.sha256(canonical(records).encode()).hexdigest()
    assert digest=="sha256:cb577548c5a894a996a1416d7eda1059bf817a31a0d7f513dd945cd799663aad"

    out={
      "schema":"w33.minimal_symmetry_changing_81_compiler.v1",
      "status":"PASS_EXPLICIT_FOURIER_COORDINATE_COMPILER_REACHES_THE_54D_SYMMETRY_CHANGE_LOWER_BOUND",
      "headline":"An explicit 81-state address-to-operator compiler exists in K-Fourier coordinates as a permutation matrix. It carries the 27 operator-compatible S1 coordinates identically into the first three multiplicity slots and deterministically retypes the 27 conjugate-Schrodinger plus 27 one-dimensional coordinates into the remaining six multiplicity slots. Exactly 54 coordinates change representation type, which is minimal because every K-equivariant map has rank at most 27.",
      "source_basis":{
        "group":"K=H27 x C3_external",
        "module":"Reg(K)",
        "coordinates":{"S1":27,"S2":27,"L":27},
        "dimension":81
      },
      "target_basis":{
        "module":"9 V_omega tensor Reg(C3_external)",
        "coordinate":"O(t,m,i), t in F3, m=0..8, i in F3",
        "dimension":81
      },
      "compiler":{
        "formula":[
          "S1(t,r,i) -> O(t,r,i), r=0,1,2",
          "S2(t,r,i) -> O(t,3+r,i), r=0,1,2",
          "L(u,v,t) -> O(t,6+u,v)"
        ],
        "matrix_type":"81x81 permutation/monomial matrix in Fourier coordinates",
        "unitary":True,
        "bijective":True,
        "mode_counts":mode_counts,
        "symmetry_preserving_coordinates":27,
        "symmetry_changing_coordinates":54,
        "symmetry_change_lower_bound":54,
        "lower_bound_saturated":True,
        "mapping_digest":digest
      },
      "interpretation":"Linear completeness and representation conversion are now separated cleanly. The group Fourier transform resolves the address module into irreducible coordinates; this minimal monomial compiler then performs exactly the 54 irreducible retypings that no K-equivariant basis change can avoid.",
      "boundary":"This solves the finite Fourier-coordinate conversion problem, not a microscopic Hamiltonian. The next physics problem is to realize the 54 retypings through a permitted interaction while preserving unitarity/coherence and the frozen FI orientation.",
      "parents":[
        "data/w33_hybrid81_operator_equivariance_budget.json",
        "data/w33_e8_matter81_hybrid_cubic_dark_basis.json",
        "data/w33_address_operator_h27_roles.json"
      ],
      "checks":{
        "81_source_coordinates_unique":True,
        "81_target_coordinates_unique":True,
        "permutation_unitary":True,
        "27_equivariant_coordinates":True,
        "54_retyped_coordinates":True,
        "54_lower_bound_reproduced":True,
        "lower_bound_saturated":True
      }
    }
    if write:OUT.write_text(json.dumps(out,indent=2)+"\n")
    return out

if __name__=="__main__":
    print(json.dumps(main(True),indent=2))
