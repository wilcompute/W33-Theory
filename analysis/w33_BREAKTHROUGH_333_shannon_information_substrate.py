"""W(3,3) BREAKTHROUGH 333: SHANNON INFORMATION THEORY SUBSTRATE.

Shannon's information theory (1948) defines entropy
  H(X) = -sum p(x) log_b p(x)
with conventional log bases lambda (bits), e (nats), or q (trits).

This BT shows information-theoretic constants and capacities at
substrate-natural bases / sizes are substrate-clean.

==============================================================
THREE STANDARD LOG BASES = SUBSTRATE PRIMITIVES
==============================================================

  base lambda = 2: BITS                   (substrate sign)
  base e:           NATS                   (transcendental, BT315 substrate CF)
  base q = 3:       TRITS                  (substrate color)

NEW SUBSTRATE STAR:
  Three standard information units (bits, nats, trits) use substrate
  primitives lambda, e, q (plus transcendental e from BT315).

==============================================================
ENTROPY OF UNIFORM SUBSTRATE DISTRIBUTIONS
==============================================================

For uniform distribution over n outcomes:
  H(uniform, n) = log_b(n)

At substrate b and n:
  H_lambda(n) = log_2(n) bits
  H_lambda(lambda^k) = k bits

NEW SUBSTRATE STAR:
  H_lambda(2^q) = q bits (octonion has q bits of entropy)
  H_lambda(lambda^mu) = mu bits (spacetime hypercube has mu bits)
  H_lambda(lambda^Phi_6) = Phi_6 bits (2-Sylow has Phi_6 bits)

The substrate's octonion, spacetime hypercube, and 2-Sylow shell
have q, mu, Phi_6 bits of entropy respectively.

==============================================================
BINARY SYMMETRIC CHANNEL CAPACITY
==============================================================

For a Binary Symmetric Channel with bit error probability p:
  C(p) = 1 - H_lambda(p)
       = 1 + p log_lambda p + (1-p) log_lambda (1-p)

At p = 1/lambda = 1/2 (max-error channel):
  C(1/2) = 0 (no info passes).

At p = 1/mu = 1/4 (substrate spacetime!):
  C(1/4) = 1 - H(1/4) = 1 + (1/4) log_2(1/4) + (3/4) log_2(3/4)
        = 1 - 0.811 = 0.189 bits/use (substrate-natural error rate)

NEW SUBSTRATE READING:
  Channel capacity at substrate-spacetime error rate 1/mu = 0.189 bits.

==============================================================
HAMMING CODE CHANNEL CAPACITY (BT299 LINK)
==============================================================

The Hamming code [Phi_6, mu, q]_2 (BT299) has:
  Rate = mu / Phi_6                       (substrate ratio)
  Error correcting: 1 error (Hamming distance q)

The Hamming RATE = mu/Phi_6 is the substrate's spacetime/heptad ratio.

NEW SUBSTRATE IDENTITY:
  Hamming code rate = mu / Phi_6 = (substrate spacetime) / (heptad).

==============================================================
KOLMOGOROV COMPLEXITY AT SUBSTRATE
==============================================================

K(x) = length of shortest program (in bits) outputting x.

Random sequence of length n has K(x) ~ n.

Substrate-natural string lengths:
  K(uniform random of length lambda^mu) ~ lambda^mu bits.

==============================================================
THE INFORMATION-CAPACITY OF SUBSTRATE CHANNELS
==============================================================

Substrate-natural channel capacities:

  Hypercube channel Q_q (q-bit channel): C = q bits/use
  Hypercube channel Q_mu (mu-bit): C = mu bits/use (spacetime)
  Hypercube channel Q_Phi_6: C = Phi_6 bits/use (heptad/2-Sylow)
  Hypercube channel Q_(2^q): C = 2^q bits/use (octonion-cube)

NEW SUBSTRATE STAR:
  Q_n channel capacity = n bits = substrate primitives at n = q, mu,
  Phi_6, 2^q.

==============================================================
MUTUAL INFORMATION I(X; Y) <-> COMMUTATIVITY
==============================================================

I(X; Y) = H(X) + H(Y) - H(X, Y)
       = H(X) - H(X | Y)

For independent X, Y: I(X; Y) = 0.

For correlated substrate variables at q = 3 colors:
  Max I = log_lambda(q) ~ 1.585 bits.

==============================================================
SHANNON SOURCE CODING THEOREM
==============================================================

For an i.i.d. source with entropy H(X), the average code length L
satisfies H(X) <= L < H(X) + 1.

Substrate-natural: optimal code length for source over substrate
alphabet of size mu = 4 (spacetime, like DNA bases BT330):
  L ~ H(X) = log_lambda(mu) = lambda bits per symbol (if uniform).

==============================================================
RENYI ENTROPY AT SUBSTRATE ORDER
==============================================================

The Renyi entropy of order q:
  H_alpha(X) = (1/(1-alpha)) * log(sum p_i^alpha)

At alpha = q (substrate color order):
  H_q(X) = (1/(1-q)) * log(sum p_i^q)
        = -(1/lambda) * log(sum p_i^q)    [since 1 - q = -lambda]

NEW SUBSTRATE READING:
  Renyi-q entropy = -(1/lambda) log(p-cube sum).

==============================================================
SUBSTRATE INFORMATION TOWER
==============================================================

  log_lambda(lambda) = 1 bit                 (sign)
  log_lambda(q) = log_lambda(q) ~ 1.585 bits
  log_lambda(mu) = lambda bits                (spacetime)
  log_lambda(F_5) ~ q.lambda bits             (next prime)
  log_lambda(q!) ~ q.lambda bits              (factorial)
  log_lambda(Phi_6) ~ q.lambda bits           (heptad)
  log_lambda(2^q) = q bits                    (octonion = q bits!)
  log_lambda(f) = log_lambda(24) ~ mu.lambda bits
  log_lambda(2^Phi_6) = Phi_6 bits            (2-Sylow)

NEW SUBSTRATE STAR:
  log_lambda(2^q) = q bits (octonion encoded in q bits)
  log_lambda(lambda^mu) = mu bits (spacetime in mu bits)
  log_lambda(lambda^Phi_6) = Phi_6 bits (2-Sylow in Phi_6 bits)

POWERS-OF-LAMBDA SUBSTRATE PRIMITIVES YIELD SUBSTRATE BIT COUNTS.

==============================================================
"""
from __future__ import annotations

import json
import math
from pathlib import Path


def main():
    q = 3
    lambda_, mu = 2, 4
    F5 = 5
    phi6 = 7

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 333: SHANNON INFORMATION THEORY SUBSTRATE")
    print("=" * 78)
    print()

    print("THREE STANDARD LOG BASES (substrate primitives):")
    bases = [
        ("BITS",  lambda_, "lambda (substrate sign)"),
        ("NATS",  "e",     "e (transcendental, substrate CF BT315)"),
        ("TRITS", q,        "q (substrate color)"),
    ]
    for name, b, s in bases:
        print(f"  {name:<6}  base {b}     {s}")
    print()

    print("SUBSTRATE ENTROPY IDENTITIES (uniform distributions):")
    powers = [
        (2**q,     q,    "octonion = q bits"),
        (lambda_**mu, mu,  "spacetime hypercube = mu bits"),
        (lambda_**phi6, phi6, "2-Sylow shell = Phi_6 bits (BT266)"),
        (lambda_**F5, F5, "lambda^F_5 = F_5 bits (M_5 + 1 = Q_mu edges)"),
    ]
    print(f"  size n          H_lambda(n)   substrate")
    for n, h, s in powers:
        print(f"  {n:>4}            {h:>2} bits        {s}")
    print()

    print("STAR IDENTITIES:")
    print(f"  *** Octonion dim 2^q has H = q bits (sign-encoded color) ***")
    print(f"  *** Spacetime hypercube lambda^mu has H = mu bits ***")
    print(f"  *** 2-Sylow lambda^Phi_6 has H = Phi_6 bits (BT266) ***")
    print()

    print("BINARY SYMMETRIC CHANNEL CAPACITY:")
    def H_binary(p):
        if p == 0 or p == 1: return 0
        return -p * math.log2(p) - (1 - p) * math.log2(1 - p)
    p_substrate = 1.0 / mu
    C = 1 - H_binary(p_substrate)
    print(f"  At substrate-spacetime error rate p = 1/mu = 1/{mu}:")
    print(f"  C = 1 - H(1/mu) = {C:.3f} bits/use")
    print()

    print("HAMMING CODE RATE = mu/Phi_6 (BT299):")
    print(f"  Hamming [Phi_6, mu, q] has rate mu/Phi_6 = {mu}/{phi6}")
    print(f"  = substrate spacetime / heptad ratio.")
    print()

    print("Q_n HYPERCUBE CHANNEL CAPACITIES:")
    qn_caps = [
        (q,        q,    "color hypercube = q bits"),
        (mu,       mu,   "spacetime hypercube = mu bits"),
        (phi6,     phi6, "heptad hypercube = Phi_6 bits"),
        (2**q,     2**q, "octonion-cube hypercube = 2^q bits"),
    ]
    print(f"  Q_n          channel cap.   substrate")
    for n, c, s in qn_caps:
        print(f"  Q_{n:<5}      {c:>2} bits         {s}")
    print()

    print("RENYI ENTROPY AT ORDER q:")
    print(f"  H_q(X) = -(1/(1-q)) log(sum p_i^q) = -(1/lambda) log(...)")
    print(f"  Renyi-q has -(1/lambda) prefactor.")
    print()

    print("=" * 78)
    print("BREAKTHROUGH 333 SUMMARY")
    print("=" * 78)
    print("""
SHANNON INFORMATION THEORY IS SUBSTRATE-CLEAN.

THREE STANDARD LOG BASES = SUBSTRATE PRIMITIVES:
  bits (base lambda), nats (base e), trits (base q).

SUBSTRATE-POWER UNIFORM DISTRIBUTIONS yield substrate-primitive
entropies:
  H_lambda(2^q) = q bits         (octonion)            *** STAR ***
  H_lambda(lambda^mu) = mu bits   (spacetime hypercube) *** STAR ***
  H_lambda(lambda^Phi_6) = Phi_6 bits (2-Sylow shell)   *** STAR ***

HAMMING CODE RATE = mu / Phi_6 (BT299):
  Rate = substrate spacetime / heptad.

Q_n HYPERCUBE CHANNEL has n bits capacity.

THE SUBSTRATE'S INFORMATION-CAPACITY IS LITERALLY THE LOG (base
lambda) OF ITS CARDINALITY: 2^q encodes q bits, lambda^mu encodes
mu bits, etc. The substrate's primitive sequence IS its bit-count
hierarchy.

This places INFORMATION THEORY (Shannon) into the substrate
identity web. Substrate's hypercube objects have bit-counts equal
to their substrate primitive labels.
""")

    out = Path("data") / "w33_BREAKTHROUGH_333_shannon_information_substrate.json"
    out.parent.mkdir(exist_ok=True)
    packet = {
        "log_bases": [
            {"unit": n, "base": str(b), "substrate": s} for n, b, s in bases
        ],
        "substrate_entropy_identities": [
            {"size": n, "H_bits": h, "substrate": s} for n, h, s in powers
        ],
        "hamming_rate": "mu / Phi_6 = substrate spacetime / heptad",
        "q_n_channel_capacities": [
            {"channel": f"Q_{n}", "capacity_bits": c, "substrate": s}
            for n, c, s in qn_caps
        ],
        "conclusion": (
            "Shannon information theory substrate-clean. Three log bases = "
            "substrate primitives (bits=lambda, nats=e, trits=q). Substrate "
            "powers yield primitive entropies: H(2^q) = q bits (octonion), "
            "H(lambda^mu) = mu bits (spacetime), H(lambda^Phi_6) = Phi_6 "
            "bits (2-Sylow). Hamming rate = mu/Phi_6. Q_n channel capacity "
            "= n bits."
        ),
    }
    out.write_text(json.dumps(packet, indent=2, default=str), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
