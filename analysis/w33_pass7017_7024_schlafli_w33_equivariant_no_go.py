#!/usr/bin/env python3
"""Passes 7017--7024: full-PSp(4,3) degree-27/degree-40 equivariant no-go.

The repo already certifies both relevant PSp(4,3) actions as transitive rank-3
permutation actions:
  * W(3,3) points: SRG(40,12,2,4), subdegrees 1,12,27;
  * Schlaefli carrier: SRG(27,16,10,8), subdegrees 1,10,16.

For a transitive rank-3 action, the complex permutation module is
multiplicity-free with three constituents.  The two nontrivial constituent
dimensions are the multiplicities of the two nontrivial SRG eigenvalues.
This script computes those dimensions exactly and then the common-constituent
count, hence dim Hom_G(C^27,C^40).
"""
from __future__ import annotations

from fractions import Fraction
import json
from math import isqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_W33_PASS7017_7024_SCHLAFLI_W33_EQUIVARIANT_NO_GO.json"


def srg_spectrum(v:int,k:int,lam:int,mu:int):
    # nontrivial eigenvalues solve x^2-(lam-mu)x-(k-mu)=0
    b = lam - mu
    disc = b*b + 4*(k-mu)
    d = isqrt(disc)
    assert d*d == disc
    r = Fraction(b+d,2)
    s = Fraction(b-d,2)
    # f+g=v-1, k+fr+gs=0
    f = Fraction(-k-(v-1)*s, r-s)
    g = Fraction(v-1)-f
    assert f.denominator == g.denominator == 1
    return [(Fraction(k),1),(r,int(f)),(s,int(g))]


def main():
    w = srg_spectrum(40,12,2,4)
    s = srg_spectrum(27,16,10,8)
    assert w == [(Fraction(12),1),(Fraction(2),24),(Fraction(-4),15)]
    assert s == [(Fraction(16),1),(Fraction(4),6),(Fraction(-2),20)]

    w_dims = [1,24,15]
    s_dims = [1,6,20]
    common = sorted(set(w_dims) & set(s_dims))
    assert common == [1]
    hom_dim = len(common)
    assert hom_dim == 1

    report = {
      "passes": list(range(7017,7025)),
      "group": "PSp(4,3), order 25920",
      "w33_action": {
        "degree":40,"rank":3,"subdegrees":[1,12,27],
        "srg":[40,12,2,4],"spectrum":{"12":1,"2":24,"-4":15},
        "permutation_module_dimensions":[1,24,15]
      },
      "schlafli_action": {
        "degree":27,"rank":3,"subdegrees":[1,10,16],
        "srg":[27,16,10,8],"spectrum":{"16":1,"4":6,"-2":20},
        "permutation_module_dimensions":[1,6,20]
      },
      "common_irreducible_dimensions":[1],
      "hom_dimension_over_C":1,
      "hom_dimension_over_Q":1,
      "theorem":"Every full-PSp(4,3)-equivariant linear map C^27 -> C^40 (and conversely) is a scalar multiple of the constant all-ones channel. There is no nonconstant full-group linear transport between the Schlaefli 27-carrier and W33 40 points.",
      "escape_routes":["restrict to a proper subgroup","use a nonlinear map","use a larger/intermediate carrier","change coefficient characteristic, which requires a separate modular analysis"],
      "boundary":"Characteristic-zero full-group linear statement only; it does not rule out subgroup-equivariant, nonlinear, or modular constructions."
    }
    OUT.write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps(report,indent=2))
    return report

if __name__ == "__main__":
    main()
