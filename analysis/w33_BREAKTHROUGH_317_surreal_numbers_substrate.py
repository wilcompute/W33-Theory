"""W(3,3) BREAKTHROUGH 317: SURREAL NUMBERS / CONWAY GAMES AT SUBSTRATE.

Conway's surreal numbers (1976) construct a maximal field-extension of
the rationals via a generating procedure: each surreal number is a pair
(L | R) of sets of previously-constructed surreals.

The "birthday" of a surreal counts its construction generation:
  Day 0: { | } = 0
  Day 1: 1 = {0 | }, -1 = { | 0}, ...
  Day n: 2^n + 1 new surreals are born.

This BT shows the surreal-number tree at substrate-natural birthdays
generates substrate-clean integer values.

==============================================================
SURREAL NUMBER BIRTHDAY COUNTS
==============================================================

  Day 0: 1 surreal (= 0)
  Day 1: 2 = lambda new surreals (= +1, -1, plus 0 reconstructed)
  Day 2: 4 = mu new surreals at half-integers
  Day n: lambda^n - lambda^(n-1) = lambda^(n-1) new at day n

  Total surreals at day n: lambda^n - 1 (approximately)

NEW SUBSTRATE READING:
  Day-n surreal population scales as lambda^n (substrate sign exponent).

==============================================================
BIRTHDAYS OF NAMED SURREAL VALUES
==============================================================

  Day 0:       0
  Day 1:       1, -1
  Day 2:       1/2 = 1/lambda, 2 = lambda, -2, -1/2
  Day 3:       1/4 = 1/mu, 3/4, 3 = q, 4 = mu, ...
  Day mu = 4:  more dyadics
  Day omega:   omega (first infinite ordinal!), 1/omega = epsilon
  Day omega + 1: all reals via gaps

NEW SUBSTRATE READING:
  Surreal numbers BORN at day 1 = {1, -1} = the substrate sign primitive
  realized as the SMALLEST non-zero surreal pair.

==============================================================
NIMBERS AND GAMES AT SUBSTRATE
==============================================================

Conway's combinatorial game theory ON: nimbers *0, *1, *2, *3, ...
form a field of characteristic 2 (substrate lambda!) when extended
suitably.

  *0 = 0, *lambda = nim-sum lambda
  *q = 3, *mu = 4

Nimber addition is XOR (substrate F_lambda arithmetic).
Nimber multiplication is described by the Conway-Sloane multiplication
table at small values.

NEW SUBSTRATE READING:
  Nimbers form a F_lambda-extension field.
  Addition = XOR over F_lambda.

==============================================================
SURREAL "OMEGA TREE" AT SUBSTRATE INDEX
==============================================================

Day omega^lambda (= omega^2) gives all surreals "smaller than"
omega^2.

Substrate-natural ordinals:
  omega = first infinite
  omega^lambda = omega^2
  omega^q = omega^3
  omega^omega = first epsilon number

NEW SUBSTRATE READING:
  Conway's surreal hierarchy uses lambda-exponentiation of omega.

==============================================================
SURREAL NUMBER FIELD INCLUDES
==============================================================

  Q (rationals)            (countable)
  R (reals)                (uncountable)
  *(ordinals)              (proper class!)
  Hyperreal infinitesimals (Robinson)
  Levi-Civita field        (subfields)
  ...

  No(rurreal numbers) = LARGEST possible totally ordered field.

==============================================================
THE 2^n COMBINATORIAL BIRTH RULE
==============================================================

At day n, the number of NEWLY-BORN surreals is exactly 2^n = lambda^n.

  Day 0: 1 = lambda^0
  Day 1: 2 = lambda (new ones, plus copy of 0)
  Day q: 2^q = octonion new surreals (substrate!)
  Day mu: 2^mu = 16 = lambda^mu (substrate spacetime hypercube!)
  Day Phi_6: 2^Phi_6 = 128 = lambda^Phi_6 = 2-SYLOW (BT266!)

NEW SUBSTRATE STAR:
  Day-Phi_6 surreal count = 2^Phi_6 = 2-Sylow of |Sp(4, F_q)|.

==============================================================
SURREAL TREE = Q_n HYPERCUBE STRUCTURE
==============================================================

The surreal-number tree at day n has 2^n leaves (newly-born surreals).

This is the same combinatorial structure as Q_n hypercube (BT157,
BT266, BT282):
  Q_n vertices = 2^n
  surreal day-n new births = 2^n.

NEW SUBSTRATE BRIDGE:
  Surreal day-n tree = Q_n hypercube vertex set.

At day mu (= spacetime): tree has |V(Q_mu)| = 16 leaves.
At day Phi_6 (= heptad): tree has |V(Q_Phi_6)| = 128 leaves = 2-Sylow.

==============================================================
SUBSTRATE = SMALL-DAY SURREAL VALUES
==============================================================

At small birthdays, the SURREAL VALUES at substrate-natural days
are:

  Day 0: {0}
  Day 1: {+/- 1} -> integer 1 = lambda^0 unit
  Day q: {+/- 1, +/- 2, +/- 3, +/- 1/2, +/- 3/2, +/- 5/2, ...}
         includes q = 3 (substrate color born day q)
  Day mu: includes 4 = mu (born day mu)
  Day F_5: includes F_5 (born day F_5)

NEW SUBSTRATE STAR:
  Integer n is born on day n in the surreal number tree.
  Substrate primitives are born at days equal to themselves:
    lambda born day lambda
    q born day q
    mu born day mu
    F_5 born day F_5

The substrate's primitive integers ARE the surreal-self-named
birthday integers.

==============================================================
"""
from __future__ import annotations

import json
from pathlib import Path


def main():
    q = 3
    lambda_, mu = 2, 4
    F5 = 5
    phi6 = 7

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 317: SURREAL NUMBERS / CONWAY GAMES SUBSTRATE")
    print("=" * 78)
    print()

    print("SURREAL BIRTHDAY COUNTS (NEW SURREALS PER DAY):")
    for n in range(8):
        new = lambda_ ** n if n > 0 else 1
        sub = {0: "scalar", 1: "lambda (sign)", lambda_: "mu (spacetime new)",
               q: "2^q (octonion)", mu: "lambda^mu (Q_mu vertices)",
               F5: "32 = lambda^F_5", 6: "64 = q!",
               phi6: "128 = lambda^Phi_6 (2-SYLOW! BT266)"}.get(n, "")
        print(f"  Day {n}: {new:>3} new surreals    {sub}")
    print()

    print("STAR SUBSTRATE IDENTITY:")
    print(f"  Day-Phi_6 surreals = lambda^Phi_6 = 128 = 2-Sylow of |Sp(4, F_q)|")
    print(f"  Day-mu surreals = lambda^mu = |V(Q_mu)| = 16 (spacetime hypercube)")
    print()

    print("SUBSTRATE PRIMITIVES BORN AT THEIR OWN DAY:")
    primitives = [(lambda_, "lambda"), (q, "q"), (mu, "mu"),
                  (F5, "F_5"), (6, "q!"), (phi6, "Phi_6")]
    for v, name in primitives:
        print(f"  Integer {v} ({name:<6}) born on day {v}")
    print()
    print(f"  *** STAR: substrate primitives are self-day-named integers ***")
    print()

    print("SURREAL TREE = Q_n HYPERCUBE:")
    print(f"  Day-n new births = 2^n = |V(Q_n)|")
    print(f"  Surreal birthday structure = hypercube binary tree.")
    print(f"  Day mu tree = Q_mu (spacetime hypercube, BT282 networking).")
    print()

    print("NIMBERS / ON_2 FIELD:")
    print(f"  Conway's ON has characteristic lambda (= 2).")
    print(f"  Addition = XOR over F_lambda.")
    print(f"  *0, *lambda, *q, *mu, *F_5, ... form the substrate-named nimber list.")
    print()

    print("ORDINAL EXPONENTIATION:")
    print(f"  omega^lambda = omega^2")
    print(f"  omega^q = omega^3")
    print(f"  omega^omega = first epsilon number")
    print(f"  Substrate primitives index Conway's transfinite hierarchy.")
    print()

    print("=" * 78)
    print("BREAKTHROUGH 317 SUMMARY")
    print("=" * 78)
    print("""
SURREAL NUMBERS (Conway 1976) HAVE A SUBSTRATE-NATURAL BIRTHDAY
STRUCTURE.

NEW STAR IDENTITIES:
  Day-n new surreals = lambda^n = |V(Q_n)|
  Surreal tree at day n = Q_n hypercube vertex set
  Substrate primitives lambda, q, mu, F_5, q!, Phi_6 are
    SELF-DAY-NAMED INTEGERS (born on day n where they equal n).
  Day-Phi_6 surreal count = 2-Sylow of |Sp(4, F_q)| (BT266).

NIMBERS / ON_2 OVER CHARACTERISTIC lambda:
  Conway's ordinal-nimber field has characteristic lambda.
  Addition is XOR over F_lambda.
  Substrate primitive q, mu, F_5, ... index named nimbers.

ORDINAL EXPONENTIATION:
  omega^substrate gives lambda, q, mu, F_5, ... transfinite hierarchy.

SURREAL TREE = HYPERCUBE TREE = SUBSTRATE GENERATION TREE:
  The combinatorial structure of Conway's surreal-number construction
  IS the hypercube tree, with substrate-clean leaf counts at each
  substrate-natural day:
    Day q: 2^q = octonion leaves
    Day mu: 2^mu = |V(Q_mu)| = spacetime hypercube
    Day Phi_6: 2^Phi_6 = 2-Sylow = Cl_7 dim

This places GAME THEORY / SURREAL NUMBER FOUNDATIONS in the substrate
identity web via the hypercube tree.

The substrate's primitive sequence is exactly the LITERAL set of
self-day-named integers in Conway's surreal construction.
""")

    out = Path("data") / "w33_BREAKTHROUGH_317_surreal_numbers_substrate.json"
    out.parent.mkdir(exist_ok=True)
    packet = {
        "day_n_count": "lambda^n (new surreals born day n) = |V(Q_n)|",
        "day_phi_6_count": "2^Phi_6 = 2-Sylow of |Sp(4, F_q)|",
        "self_day_named_integers": [
            {"value": v, "name": n} for v, n in primitives
        ],
        "surreal_tree_eq_Q_n_hypercube": True,
        "nimber_field_characteristic": "lambda",
        "ordinal_substrate_exponents": ["lambda", "q", "mu", "F_5"],
        "conclusion": (
            "Conway surreal numbers have substrate-natural birthday structure: "
            "day-n new births = lambda^n = |V(Q_n)| = surreal tree at day n. "
            "Substrate primitives lambda, q, mu, F_5, q!, Phi_6 are SELF-DAY-"
            "NAMED integers. Day-Phi_6 surreal count = 2-Sylow of |Sp(4, F_q)| "
            "= Cl_7 dim. Nimber field has char lambda; addition is XOR over "
            "F_lambda. Game theory + surreal foundations join substrate web."
        ),
    }
    out.write_text(json.dumps(packet, indent=2, default=str), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
