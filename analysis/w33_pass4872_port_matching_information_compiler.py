#!/usr/bin/env python3
"""Pass4872 — exact information/control cost of the 45 local S3 port matchings.

Pass4861 proved that a bijection between three sheet cells and three line ports
at each of 45 recovered GQ points is the minimal datum that kills S3^45.
This verifier compiles each S3 selector as AGL(1,3):

    i |-> (-1)^b i + r  (mod 3),   r in F3, b in F2,

so each local selector is exactly one trit plus one bit.
"""
from __future__ import annotations
import itertools,json,math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/PART_W33_PASS4872_PORT_MATCHING_INFORMATION_COMPILER.json"

def perm(r,b):
    return tuple((((-1 if b else 1)*i+r)%3) for i in range(3))

def main()->int:
    affine={(r,b):perm(r,b) for r in range(3) for b in range(2)}
    assert len(set(affine.values()))==6
    assert set(affine.values())==set(itertools.permutations(range(3)))
    for r,b in affine:
        for s,c in affine:
            lhs=tuple(affine[(r,b)][affine[(s,c)][i]] for i in range(3))
            rhs=affine[((r+(-1 if b else 1)*s)%3,(b+c)%2)]
            assert lhs==rhs

    n=45;states=6**n;entropy=n*math.log2(6);binary=math.ceil(entropy)
    local_bits=n*3
    chir_states=2*states;chir_entropy=entropy+1;chir_binary=math.ceil(chir_entropy)
    assert 2**(binary-1)<states<=2**binary
    assert 2**(chir_binary-1)<chir_states<=2**chir_binary

    out={
      "pass":4872,
      "local_selector":{"group":"S3 ~= AGL(1,3) ~= F3 : F2","affine_rule":"i -> (-1)^b i + r mod 3",
        "native_state":"one trit r plus one bit b","states":6},
      "45_point_table":{"state_count":states,"entropy_bits":entropy,"optimal_global_fixed_binary_bits":binary,
        "independent_local_binary_bits":local_bits,"independent_local_binary_overhead_bits":local_bits-binary,
        "native_mixed_radix":"45 trits + 45 bits"},
      "with_global_chirality":{"state_count":chir_states,"entropy_bits":chir_entropy,
        "optimal_global_fixed_binary_bits":chir_binary,"native_mixed_radix":"45 trits + 46 bits"},
      "landauer_symbolic":{"port_table_reset_minimum":"45 k_B T ln 6","plus_chirality":"k_B T (45 ln 6 + ln 2)",
        "boundary":"Thermodynamic lower bound applies only to logically irreversible reset/erasure, not to reversible routing itself."},
      "compiler":{"decode":"two-stage affine port map: optional reflection i->-i followed by trit rotation i->i+r",
        "table_free_option":"If hardware supplies a deterministic coordinate-derived matching rule, the 6^45 table need not be stored; that rule is extra physical/placement structure and is not supplied by the intrinsic code.",
        "capability":"removes all local representative ambiguity while preserving the diagonal PGSp action certified in Pass4861"},
      "theorem":"The minimal S3-breaking port datum has an exact qutrit-native compiler: every local three-port matching is the affine map i->(-1)^b i+r over F3, so the 45-point selector table is exactly 45 trits plus 45 bits. An arbitrary global table has 6^45 states, Shannon information 45 log2(6)=116.323... bits, and therefore needs at least 117 fixed binary bits globally (or 135 bits if each point is encoded independently in 3 bits). Adding the global chirality bit raises the optimum to 118 bits.",
      "boundary":"Information/control accounting theorem. It does not assert a particular FPGA/photonic implementation realizes the entropy bound, and Landauer cost is not incurred by reversible routing unless information is erased."
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=="__main__":raise SystemExit(main())
