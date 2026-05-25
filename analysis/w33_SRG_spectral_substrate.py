"""W(3,3) SRG SPECTRAL SUBSTRATE IDENTITIES + PROJECTIVE PLANE CONNECTION.

The W(3,3) = SRG(40, 12, 2, 4) graph's adjacency spectrum and the
projective plane PG(2, F_3) over the ternary field yield clean
substrate identifications.

ADJACENCY SPECTRUM OF W(3,3):

  lambda_max = k = 12        (mult 1, Perron)
  lambda_+   = 2              (mult f = 24 = gauge_mult)
  lambda_-   = -mu = -4       (mult g_neg = 15 = chiral_mult)

SUBSTRATE SPECTRAL IDENTITIES:

  lambda_max - lambda_+ = Phi_4 = 10     (Laplacian gauge eigenvalue)
  lambda_max - lambda_- = 2^mu = 16      (Laplacian chiral eigenvalue)
  lambda_+ - lambda_-   = q!  = 6        (eigenvalue gap)

ADJACENCY DISCRIMINANT:

The SRG eigenvalue polynomial lambda^2 - (l - mu)lambda - (k - mu) = 0
becomes lambda^2 + 2*lambda - 8 = 0 at W(3,3).

Discriminant: D = (-2)^2 + 4*8 = 4 + 32 = 36 = (q!)^2.

So sqrt(D) = q! = 6 = eigenvalue gap = lambda_+ - lambda_-.

PROJECTIVE PLANE PG(2, F_3):

  Number of points         =  Phi_3 = 13
  Number of lines          =  Phi_3 = 13
  Points per line          =  mu = 4
  Lines per point          =  mu = 4
  Total flags (incidences) =  mu * Phi_3 = 52 = dim(F_4 exceptional Lie)
  Non-incidences           =  Phi_3^2 - mu * Phi_3 = 13^2 - 52 = 117 = q^2 * Phi_3

CONNECTIONS:

  dim(F_4)               =  mu * Phi_3 = PG(2,F_3) flag count = 52
  m_sterile / m_Pl       =  q^(-dim F_4) = q^(-52)  (BSM prediction)
  PG(2,F_3) flags        =  Fano-2 generalization (Fano = PG(2,F_2) with 21 flags)
                            (W(3,3)'s F_3 analog has 52 flags)

The substrate's "BSM ladder" exponent 52 for sterile neutrino mass is
exactly the PG(2,F_3) flag count, which is also the dimension of the
F_4 exceptional Lie algebra.
"""
from __future__ import annotations

import json
from pathlib import Path


Q = 3
MU = 4
QFACT = 6
K_CODEC = Q * MU
PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
F = 24
G_NEG = 15
V = 40


def srg_spectrum() -> dict:
    return {
        "lambda_max":         {"value": K_CODEC, "mult": 1,        "form": "k (Perron)"},
        "lambda_plus":        {"value": 2,         "mult": F,       "form": "r (gauge sector)"},
        "lambda_minus":       {"value": -MU,        "mult": G_NEG,   "form": "s = -mu (chiral sector)"},
        "trace_check":         K_CODEC + 2 * F + (-MU) * G_NEG,
    }


def spectral_substrate_identities() -> list[dict]:
    return [
        {"identity": "lambda_max - lambda_+ = Phi_4",  "lhs": K_CODEC - 2,   "rhs": PHI4,     "match": K_CODEC - 2 == PHI4},
        {"identity": "lambda_max - lambda_- = 2^mu",   "lhs": K_CODEC + MU,  "rhs": 2 ** MU,  "match": K_CODEC + MU == 2 ** MU},
        {"identity": "lambda_+ - lambda_- = q!",        "lhs": 2 + MU,        "rhs": QFACT,    "match": 2 + MU == QFACT},
        {"identity": "discriminant = (q!)^2",          "lhs": 36,             "rhs": QFACT ** 2, "match": 36 == QFACT ** 2},
        {"identity": "sum eigenvalues * multiplicity = 0 (trace)",
                          "lhs": K_CODEC + 2 * F + (-MU) * G_NEG, "rhs": 0,    "match": K_CODEC + 2 * F + (-MU) * G_NEG == 0},
    ]


def projective_plane_PG_2_F3() -> dict:
    return {
        "n_points":         PHI3,
        "n_lines":          PHI3,
        "points_per_line":  MU,
        "lines_per_point":  MU,
        "flag_count":        MU * PHI3,
        "n_non_incidences":  PHI3 ** 2 - MU * PHI3,
        "substrate_form":   "n_points = lines = Phi_3 = 13; flags = mu * Phi_3 = 52",
        "comparison_Fano": {
            "Fano_PG_2_F2": "7 points, 7 lines, 3 points per line, 21 flags",
            "PG_2_F_3":     "13 points, 13 lines, 4 points per line, 52 flags",
        },
    }


def connections_to_physics() -> dict:
    return {
        "dim_F_4_Lie_algebra": MU * PHI3,
        "BSM_sterile_exponent": MU * PHI3,
        "claim": "dim(F_4) = mu * Phi_3 = PG(2,F_3) flag count = 52",
        "m_sterile_substrate": "m_sterile / m_Pl = q^(-dim F_4) = q^(-52)",
    }


def build_payload() -> dict:
    return {
        "header": {
            "substrate_constants": {
                "q": Q, "mu": MU, "q!": QFACT, "k": K_CODEC,
                "Phi_3": PHI3, "Phi_4": PHI4, "Phi_6": PHI6,
                "f": F, "g_neg": G_NEG, "v": V,
            },
        },
        "srg_spectrum":               srg_spectrum(),
        "spectral_substrate_identities": spectral_substrate_identities(),
        "projective_plane_PG_2_F3":     projective_plane_PG_2_F3(),
        "connections_to_physics":      connections_to_physics(),
        "headline": (
            "W(3,3) SRG spectrum {12, 2, -4} with discriminant (q!)^2 = 36.\n"
            "PG(2,F_3) has 13 = Phi_3 points and 52 = mu*Phi_3 = dim(F_4) flags.\n"
            "Substrate BSM exponent for sterile neutrino: q^(-52) = q^(-dim F_4)\n"
            "                                            = q^(-PG(2,F_3) flags)."
        ),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_SRG_spectral_substrate.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("=" * 78)
    print("W(3,3) SRG SPECTRAL + PG(2, F_3) SUBSTRATE")
    print("=" * 78)

    s = payload["srg_spectrum"]
    print(f"\nW(3,3) Adjacency spectrum:")
    for k, v in s.items():
        if isinstance(v, dict):
            print(f"  {k:>15s}: value={v['value']:>3d}, mult={v['mult']:>2d}  ({v['form']})")
    print(f"  trace check: {s['trace_check']} (should be 0)")

    print(f"\nSpectral substrate identities:")
    for i in payload["spectral_substrate_identities"]:
        print(f"  {i['identity']:>45s}: lhs={i['lhs']}, rhs={i['rhs']}, match={i['match']}")

    p = payload["projective_plane_PG_2_F3"]
    print(f"\nPG(2, F_3) projective plane:")
    print(f"  points = lines = {p['n_points']} = Phi_3")
    print(f"  points/line = {p['points_per_line']} = mu")
    print(f"  flag count = {p['flag_count']} = mu * Phi_3")
    print(f"  Comparison with Fano (PG(2,F_2)):")
    for k, v in p["comparison_Fano"].items():
        print(f"    {k:>15s}: {v}")

    c = payload["connections_to_physics"]
    print(f"\nPhysics connection: {c['claim']}")
    print(f"  BSM sterile neutrino: {c['m_sterile_substrate']}")

    print(f"\nHEADLINE:")
    print(payload["headline"])

    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
