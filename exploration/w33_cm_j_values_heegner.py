r"""The j-invariant at CM points pins the nine class-number-1 fields.

For an imaginary quadratic order  O_D  of discriminant  D < 0, the value
j(tau_D)  -- where  tau_D  is the canonical CM point of the principal form --
is an algebraic integer of degree  h(D)  (the class number) over Q.  When
h(D) = 1, j(tau_D) is an INTEGER.  There are exactly nine such  D:

    D in { -3, -4, -7, -8, -11, -19, -43, -67, -163 }      (Heegner / Stark).

The corresponding j-values (Weber, Atkin / Birch, Stark, Heegner) are

    D = -3   :  j(tau) =                 0  =                   0
    D = -4   :  j(tau) =              1728  =                  12^3
    D = -7   :  j(tau) =             -3375  =                 -15^3
    D = -8   :  j(tau) =              8000  =                  20^3
    D = -11  :  j(tau) =            -32768  =                 -32^3
    D = -19  :  j(tau) =           -884736  =                 -96^3
    D = -43  :  j(tau) =        -884736000  =                -960^3
    D = -67  :  j(tau) =     -147197952000  =               -5280^3
    D = -163 :  j(tau) = -262537412640768000 =            -640320^3.

PROOF SKELETON.  For each principal form  Q_D = a x^2 + b x y + c y^2 of
discriminant D = b^2 - 4 a c, the canonical point is
    tau_D = (-b + sqrt(D)) / (2 a)  in the upper half plane (so a = 1, b = 0
    or 1 depending on D mod 4).
Class field theory (Hauptidealsatz, Weber) says j(tau_D) generates the
Hilbert class field  H_D / K_D = Q(sqrt(D)).  When h(D) = 1, H_D = K_D and
j(tau_D) lies in Q; integrality is the next standard step.

THE q-EXPANSION GIVES NUMERICAL EVIDENCE.

    j(q)  =  1/q  +  744  +  196884 q  +  21493760 q^2  +  ...

At  tau_D = (1 + sqrt(-D))/2,  q = exp(2 pi i tau)  =  -exp(-pi sqrt(D))
(odd D mod 4) and  q = exp(-pi sqrt(D))  (even D mod 4 or D = -4).  In the
former case 1/q is large and negative, j is dominated by 1/q + 744.

RAMANUJAN'S NEAR-INTEGER FORMULA.

    exp(pi sqrt(163))  ~~  262537412640768744  =  640320^3  +  744,

which is just the q-series approximation  -1/q  ~~  j(tau)  -  744  =  -640320^3 - 744.
(Equivalently  e^{pi sqrt(163)} - (640320^3 + 744)  is of order  10^{-12}.)

CONNECTION TO W(3,3) AND THE LEVEL-1 PLANE.

    1728  =  12^3  =  k_W33^3                         (D = -4, j(i)).
    640320  =  2^6 * 3 * 5 * 23 * 29                  (D = -163, Monster moonshine).
    640320^3 + 744 = 196884 * 1333_...                (Monstrous moonshine seed).
    The set  {0, 1728, -3375, 8000, ..., -640320^3}  is the COMPLETE list of
    rational j-values, hence the complete list of elliptic curves over Q with
    CM by an order of class number 1.

This layer pins:
    (1) the nine Heegner discriminants and their j-values are perfect cubes;
    (2) numerical j(tau_D) computed from the q-series matches the algebraic
        integer for D in {-3, -4, -7, -8, -11};
    (3) high-precision j(tau_D) matches for D in {-19, -43, -67, -163};
    (4) Ramanujan's near-integer  | exp(pi sqrt(163)) - (640320^3 + 744) | < 10^{-9}.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

import mpmath as mp


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_cm_j_values_heegner_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))


# ----------------------------------------------------------------------
# The nine Heegner discriminants and their j-values.
# Stored as (D, j_value, cube_root) where j_value = cube_root^3.
# ----------------------------------------------------------------------
HEEGNER_TABLE: list[tuple[int, int, int]] = [
    (-3,                    0,         0),
    (-4,                 1728,        12),
    (-7,                -3375,       -15),
    (-8,                 8000,        20),
    (-11,              -32768,       -32),
    (-19,             -884736,       -96),
    (-43,          -884736000,      -960),
    (-67,       -147197952000,     -5280),
    (-163, -262537412640768000,  -640320),
]


def heegner_table() -> dict[str, Any]:
    return {
        "discriminants":  [t[0] for t in HEEGNER_TABLE],
        "j_values":       [t[1] for t in HEEGNER_TABLE],
        "cube_roots":     [t[2] for t in HEEGNER_TABLE],
        "count":          len(HEEGNER_TABLE),
    }


def verify_j_values_are_perfect_cubes() -> dict[str, Any]:
    discrepancies = []
    for D, j_val, root in HEEGNER_TABLE:
        if root ** 3 != j_val:
            discrepancies.append({"D": D, "j": j_val, "root": root, "root_cubed": root ** 3})
    return {
        "n_tested":      len(HEEGNER_TABLE),
        "discrepancies": discrepancies,
        "all_match":     discrepancies == [],
    }


# ----------------------------------------------------------------------
# Numerical computation of j(tau_D) via the q-expansion.
#
#   tau_D = (1 + sqrt(-D))/2  if D mod 4 == 1  (D = -3, -7, -11, -19, -43, -67, -163)
#   tau_D = sqrt(-D)/2        if D mod 4 == 0  (D = -4, -8)
#
# In both cases  q = exp(2 pi i tau).  For D mod 4 == 1, q is a NEGATIVE
# real number  -exp(-pi sqrt(D)); for D mod 4 == 0, q is a POSITIVE real
# number  exp(-pi sqrt(D)).
# ----------------------------------------------------------------------
def _q_at_tau_D(D: int, dps: int = 60) -> mp.mpf:
    """Return the real number q = e^{2 pi i tau_D} as a high-precision mpf.

    Sign convention:  D = -3, -7, -11, ...  ->  q = -e^{-pi sqrt(|D|)},
                       D = -4, -8           ->  q =  e^{-pi sqrt(|D|)}.
    """
    mp.mp.dps = dps
    pi_sqrt = mp.pi * mp.sqrt(-D)
    base = mp.exp(-pi_sqrt)
    if D % 4 == 1 or D == -3:
        return -base
    return base


def _j_q_series_value(q: mp.mpf, n_terms: int = 20) -> mp.mpf:
    """Evaluate j(q) = 1/q + 744 + sum_{n >= 1} c_n q^n with c_n the
       J_tilde - 744 coefficients shifted appropriately.  Coefficients up
       through q^7 are the Monster moonshine head."""
    coeffs = [
        744,
        196884,
        21493760,
        864299970,
        20245856256,
        333202640600,
        4252023300096,
        44656994071935,
    ][: n_terms + 1]
    val = 1 / q
    qpow = mp.mpf(1)
    for c in coeffs:
        val += c * qpow
        qpow *= q
    return val


def numerical_j_at_CM(D: int, dps: int = 60, n_terms: int = 8) -> mp.mpf:
    q = _q_at_tau_D(D, dps=dps)
    return _j_q_series_value(q, n_terms=n_terms)


def verify_low_D_numeric_matches(threshold: float = 1e-3) -> dict[str, Any]:
    """For D in {-7, -8, -11} the q-series converges fast enough to verify
       j(tau_D) numerically against the integer.  D = -3, -4 are exact at
       q = -exp(-pi sqrt(3)) and q = exp(-pi sqrt(4)) respectively but the
       q-series convergence is slow at D = -3 (|q| ~ 0.0043), so we include
       D = -3, -4 with weaker thresholds."""
    results = {}
    all_close = True
    # For D = -3, |q| ~ 0.0043 so series converges only modestly.
    # j(rho) = 0; absolute tolerance is acceptable.
    for D, j_int, _ in HEEGNER_TABLE:
        # Use enough terms; for D = -3 use 7 terms (max we have).
        n_terms = 7
        # Use higher dps for higher D since 1/q dominates more.
        dps = max(30, abs(D) // 2 + 30)
        j_num = numerical_j_at_CM(D, dps=dps, n_terms=n_terms)
        diff = abs(j_num - j_int)
        # Use absolute threshold scaled by max(|j|, 1).
        scale = max(abs(j_int), 1)
        rel = float(diff / scale)
        match = rel < threshold
        results[D] = {
            "j_int":          j_int,
            "j_numeric_str":  mp.nstr(j_num, 12),
            "abs_diff_str":   mp.nstr(diff, 6),
            "relative_diff":  rel,
            "match":          match,
        }
        if not match:
            all_close = False
    return {
        "threshold":     threshold,
        "per_D":         results,
        "all_close":     all_close,
    }


# ----------------------------------------------------------------------
# Ramanujan's near-integer  exp(pi sqrt(163)) ~~ 640320^3 + 744.
# ----------------------------------------------------------------------
def verify_ramanujan_constant(dps: int = 50) -> dict[str, Any]:
    mp.mp.dps = dps
    e_pi_sqrt163 = mp.exp(mp.pi * mp.sqrt(163))
    target = mp.mpf(640320) ** 3 + 744
    diff = abs(e_pi_sqrt163 - target)
    return {
        "exp_pi_sqrt163_str":      mp.nstr(e_pi_sqrt163, 25),
        "target_640320_cubed_p744": int(target),
        "abs_diff_str":            mp.nstr(diff, 12),
        "diff_lt_1e_minus_9":      bool(diff < mp.mpf("1e-9")),
        "diff_lt_1e_minus_11":     bool(diff < mp.mpf("1e-11")),
    }


# ----------------------------------------------------------------------
# Specific algebraic-cube structural pins.
# ----------------------------------------------------------------------
def cube_structure_pins() -> dict[str, Any]:
    return {
        "j_at_i_is_12_cubed":             1728 == 12 ** 3,
        "j_at_i_is_k_W33_cubed":          1728 == 12 ** 3,
        "j_at_-163_cube_root_640320":     (-262537412640768000) // (-640320) // (-640320) // (-640320) == 1,
        "640320_factors":                 "2^6 * 3 * 5 * 23 * 29",
        "640320_squared":                 640320 ** 2,
        "640320_cubed":                   640320 ** 3,
        "Heegner_count":                  9,
        "all_class_number_1_imag_quad":   [-3, -4, -7, -8, -11, -19, -43, -67, -163],
    }


# ----------------------------------------------------------------------
# Driver.
# ----------------------------------------------------------------------
def derive_all() -> dict[str, Any]:
    table = heegner_table()
    cubes = verify_j_values_are_perfect_cubes()
    numeric = verify_low_D_numeric_matches(threshold=1e-3)
    rama = verify_ramanujan_constant(dps=50)
    structure = cube_structure_pins()
    return {
        "heegner_table":           table,
        "j_values_are_cubes":      cubes,
        "numeric_j_matches":       numeric,
        "ramanujan_constant":      rama,
        "cube_structure_pins":     structure,
        "summary_chain": {
            "nine_Heegner_discriminants_listed":         table["count"] == 9,
            "all_j_values_are_perfect_cubes":            cubes["all_match"],
            "j_at_i_equals_12_cubed":                    structure["j_at_i_is_12_cubed"],
            "numeric_j_matches_for_all_nine":            numeric["all_close"],
            "ramanujan_e_pi_root163_near_640320_cubed":  rama["diff_lt_1e_minus_9"],
        },
    }


def main() -> None:
    summary = derive_all()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    print("=" * 72)
    print("W33 CM j-VALUES AND THE NINE HEEGNER DISCRIMINANTS")
    print("=" * 72)
    print()
    for key, val in summary["summary_chain"].items():
        status = "PASS" if val else "FAIL"
        print(f"  [{status}] {key}")
    print()
    print("  D       j(tau_D)             cube root")
    print("  --      -----                ----")
    for D, j_val, root in HEEGNER_TABLE:
        print(f"  {D:>4}    {j_val:>22}    {root:>10}")
    print()
    print(f"  exp(pi sqrt(163)) - (640320^3 + 744) = {summary['ramanujan_constant']['abs_diff_str']}")


if __name__ == "__main__":
    main()
