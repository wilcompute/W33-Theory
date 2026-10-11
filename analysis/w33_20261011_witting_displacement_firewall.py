#!/usr/bin/env python3
"""2026-10-11: exact symmetry firewall for perturbing a Witting-ray vacuum.

A G32-invariant scalar cannot generate a projective tangent force at a Witting
ray.  The pointwise G25 subgroup already fixes the ray and has no invariant
covector in the transverse triplet.  This corrects the heuristic in Pass
11891 that the invariant degree-12 operator itself supplies a small displacement.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261011_witting_displacement_firewall.json"
sys.path.insert(0,str(ROOT/"analysis"))
import w33_pass1068_chevie_g25_g32_matrices as G

def sha(p):
    return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()

def transpose(A):
    return [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]

def fixed_dimension(gens,n,dual=False):
    I=G.ident(n); rows=[]
    for g in gens:
        A=transpose(g) if dual else g
        rows.extend(G.sub(A,I))
    return n-G.rank(rows)
def payload():
    dirs=[(0,0,-1,0),(1,1,1,0),(0,1,0,0),(1,-1,0,-1)]
    R4=[G.reflection(v) for v in dirs]
    R3=[G.block3(x) for x in R4[:3]]
    g25=G.group_mod7([G.tupmod(x) for x in R3],3)
    g32=G.group_mod7([G.tupmod(x) for x in R4],4)
    tangent_fixed=fixed_dimension(R3,3,False)
    cotangent_fixed=fixed_dimension(R3,3,True)
    assert len(g25)==648 and len(g32)==155520
    assert tangent_fixed==0 and cotangent_fixed==0
    old=json.loads((ROOT/"data/w33_pass11664_11671_kernel_dynamics.json").read_text())
    loop=json.loads((ROOT/"data/w33_pass11884_11886_one_loop_trinification.json").read_text())
    flav=json.loads((ROOT/"data/w33_pass11921_flavour_qutrits.json").read_text())
    p64=old["passes"]["11664"]
    assert p64["exact_group_order"]==648
    assert p64["transverse_odd_equals_even_mass_kernel"]
    assert p64["H27_relation"]=="ZX=omega XZ; center=omega I3"
    assert loop["checks"]["global_minimum_at_witting"] and loop["checks"]["strict_local_min"]
    assert loop["checks"]["phase_exactly_flat"]
    assert flav["checks"]["factorisation_all_pairs"] and flav["checks"]["up_top_space_exactly_three"]
    theorem=(
      "Let r be a Witting ray and T_r its three-complex-dimensional projective "
      "Cartan tangent. The pointwise stabilizer contains the exact G25 parabolic "
      "of order 648. Its action on T_r and on T_r^* has no trivial submodule. "
      "Hence for every differentiable G32-invariant scalar V, dV_r restricted "
      "to T_r is zero. In particular any scalar potential made only from the "
      "G32 invariant generators of degrees 12,18,24,30 keeps every Witting ray "
      "an exact stationary ray."
    )
    return {
      "schema":"w33.20261011.witting-displacement-firewall.v1",
      "status":"PASS_G32_INVARIANTS_CANNOT_PERTURBATIVELY_DISPLACE_A_WITTING_RAY",
      "exact_group_data":{
        "G25_order":len(g25),"G32_order":len(g32),
        "G25_tangent_fixed_dimension":tangent_fixed,
        "G25_cotangent_fixed_dimension":cotangent_fixed,
        "G25_degrees":[6,9,12],"G32_degrees":[12,18,24,30],
      },
      "repo_identification":{
        "actual_Witting_transverse_triplet_is_G25_H27":True,
        "H27_relation":p64["H27_relation"],
        "one_loop_Witting_is_strict_projective_minimum":True,
        "one_loop_common_phase_flat":True,
      },
      "theorem":theorem,
      "pass11891_correction":{
        "stands":"Im(Omega)~(3/pi)log(1/delta) and the theta hierarchy epsilon is linear in an externally supplied projective displacement delta.",
        "withdraw":"A G32-invariant degree-12 scalar operator by itself generically produces delta~(v/Lambda)^8.",
        "reason":"The invariant has zero projective tangent differential at every Witting ray. It can lift the common phase or change tangent Hessian/stability, but cannot supply a linear displacement force.",
        "allowed_alternatives":[
          "an explicit G32-breaking spurion in the transverse G25 triplet",
          "a bifurcation after an invariant correction changes a tangent Hessian sign",
          "a cross-sector coupling whose background breaks the Witting stabilizer"
        ],
      },
      "flavour_weld":{
        "pass11921_flux_factorises_W33_into_two_qutrits":True,
        "pass11921_up_Higgs_top_space_dimension":3,
        "transverse_Witting_module_dimension":3,
        "representation_target":"The exact Witting tangent is already the G25/H27 qutrit triplet of Pass11664. Pass11921 independently produces a three-dimensional up-Higgs flavour qutrit. Therefore the minimal symmetry-breaking spurion needed to move the Witting vacuum has exactly the representation type required by the flavour sector.",
        "firewall":"No phase-resolved intertwiner between the Pass11921 theta-function Higgs basis and the Pass11664 transverse basis is constructed here. Representation compatibility is not a derived physical coupling.",
      },
      "physics_consequence":"A realistic hierarchy cannot be attributed to a fully G32-symmetric higher-dimensional correction if it relies on moving off the radiative Witting ray. The displacement source must break the Witting-ray little group (or arise after a stability bifurcation).",
      "sources":{
        p:sha(p) for p in [
          "analysis/w33_pass1068_chevie_g25_g32_matrices.py",
          "data/w33_pass11664_11671_kernel_dynamics.json",
          "data/w33_pass11884_11886_one_loop_trinification.json",
          "data/w33_pass11921_flavour_qutrits.json",
        ]
      },
      "checks":{
        "orders_648_155520":True,
        "no_G25_fixed_tangent":True,
        "no_G25_fixed_cotangent":True,
        "actual_repo_transverse_triplet_matches_G25_H27":True,
        "radiative_Witting_ray_projectively_strict":True,
        "flavour_qutrit_is_three_dimensional":True,
      }
    }

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--check",action="store_true")
    a=ap.parse_args();p=payload();txt=json.dumps(p,indent=2,sort_keys=True)+"\n"
    if a.check:
        if not OUT.exists() or OUT.read_text()!=txt: raise SystemExit("certificate drift")
    else:
        OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(txt)
    print(json.dumps({"status":p["status"],"fixed":[p["exact_group_data"]["G25_tangent_fixed_dimension"],p["exact_group_data"]["G25_cotangent_fixed_dimension"]]}))
if __name__=="__main__":raise SystemExit(main())
