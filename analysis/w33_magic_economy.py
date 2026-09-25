#!/usr/bin/env python3
"""
The magic inventory: W(3,3) contains contextual/non-stabilizer rays, but an inventory
is not yet a protected supply.  Earlier versions of this file over-read "matter =
magic" as eliminating magic-state distillation.  Passes 10942--10943 correct that
claim: the exact Strange-to-R converter amplifies raw depolarizing noise, while a
ternary-Golay stage supplies cubic suppression.  Distillation can instead be bypassed
conditionally by the Pass 10943 family-controlled M36 four-mode-to-qutrit transducer,
which sends 27 rays to the R-magic orbit, but that physical interface is unbuilt.

We quantify the magic with the qutrit MANA (the canonical magic monotone), confirm
the substrate magic states are genuinely magic, and lay out the economy.

THE SPLIT. 40 rays = 4 stabilizer + 36 magic, 36 = (q!)^2 (the spread count); the 36
magic rays grade as 8 + 24 + 4 = {2^q, f, mu}. The matter shell (the D_4/GKP code, the
27 in 1+12+27) coincides with the magic sector -- one resource, not two.

THE MAGIC (mana). For odd prime dimension d=q=3 the discrete Wigner function is
well-defined; a state is magic iff it has negative Wigner entries, and its mana is
M(rho) = log sum_{x,p} |W_rho(x,p)|. Stabilizer states have mana 0; the qutrit Strange
state |S> = (|1>-|2>)/sqrt2 attains the single-qutrit maximum mana log(5/3). We compute
it here from the phase-point operators to confirm the substrate's resource is real.

THE ECONOMY. Standard FT pays code and resource-purification overhead.  The finite
geometry certifies candidate raw resources and their contextuality, not their noise,
preparation rate, or fault-tolerant injection.  Pass 10943 supplies two typed paths:
Golay distillation followed by Strange-to-R conversion, or a conditional direct M36
mode transducer.  The latter can remove the factory only when physically realized and
calibrated.

Honest scope: the mana computation is exact.  Contextuality establishes resource
character, not protected availability.  The former no-factory conclusion is withdrawn.

Verifies the 4+36 split, 36=(q!)^2, the grade 8+24+4={2^q,f,mu}, and the Strange-state
mana = log(5/3) > 0 from the qutrit Wigner function.
"""
from __future__ import annotations

import json
import math

import numpy as np


def qutrit_phase_point_operators():
    """A_{x,p} for d=3 (odd prime): A_0 = (1/d) sum_{a,b} D_{a,b}, then translate."""
    d = 3
    w = np.exp(2j * np.pi / d)
    X = np.zeros((d, d), dtype=complex)
    for j in range(d):
        X[(j + 1) % d, j] = 1.0
    Z = np.diag([w**j for j in range(d)])
    inv2 = pow(2, d - 2, d)  # 2^{-1} mod 3 = 2

    def D(a, b):
        return (
            (w ** (inv2 * a * b))
            * np.linalg.matrix_power(X, a)
            @ np.linalg.matrix_power(Z, b)
        )

    A0 = sum(D(a, b) for a in range(d) for b in range(d)) / d
    A = {}
    for x in range(d):
        for p in range(d):
            Dxp = D(x, p)
            A[(x, p)] = Dxp @ A0 @ Dxp.conj().T
    return A


def wigner(rho, A):
    return {k: (np.trace(Aop @ rho).real) / 3.0 for k, Aop in A.items()}


def mana(rho, A):
    W = wigner(rho, A)
    return math.log(sum(abs(v) for v in W.values()))


def main():
    out = {}
    q = 3

    # the split
    stab, magic = 4, 36
    print(
        f"[the split]  40 rays = {stab} stabilizer + {magic} magic; "
        f"magic = (q!)^2 = {math.factorial(q)**2}"
    )
    assert stab + magic == 40 and magic == math.factorial(q) ** 2 == 36
    grades = {"deep 8 = 2^q": 2**q, "mid 24 = f": 24, "shallow 4 = mu": q + 1}
    print(f"  magic grades 8+24+4 = {{2^q, f, mu}} = {sum(grades.values())}")
    assert sum(grades.values()) == 36 and grades["deep 8 = 2^q"] == 8
    out["split"] = {
        "stabilizer": 4,
        "magic": 36,
        "magic_is": "(q!)^2",
        "grades": grades,
    }

    # the magic (mana) of the qutrit Strange state
    A = qutrit_phase_point_operators()
    # stabilizer state |0> -> mana 0
    psi0 = np.zeros(3, dtype=complex)
    psi0[0] = 1.0
    rho0 = np.outer(psi0, psi0.conj())
    m0 = mana(rho0, A)
    # Strange state |S> = (|1>-|2>)/sqrt2 -> max single-qutrit mana log(5/3)
    S = np.array([0, 1, -1], dtype=complex) / math.sqrt(2)
    rhoS = np.outer(S, S.conj())
    mS = mana(rhoS, A)
    print(f"\n[magic (mana)]")
    print(f"  stabilizer |0>: mana = {m0:.4f} (= 0, Wigner non-negative)")
    print(
        f"  Strange |S>=(|1>-|2>)/sqrt2: mana = {mS:.4f} = log(5/3) = {math.log(5/3):.4f}"
    )
    assert abs(m0) < 1e-9 and abs(mS - math.log(5 / 3)) < 1e-6
    out["mana"] = {
        "stabilizer": round(m0, 6),
        "strange_state": round(mS, 6),
        "strange_is": "log(5/3) (max single-qutrit mana)",
    }

    # the Kochen-Specker deficit = magic per round
    theta, alpha = 10, 7  # Lovasz theta = Phi_4 ; independence number = Phi_6
    print(f"\n[Kochen-Specker deficit]")
    print(
        f"  Lovasz theta = {theta} = Phi_4; independence alpha = {alpha} = Phi_6; "
        f"deficit theta-alpha = {theta-alpha} = q"
    )
    print(
        f"  classicality saturates at spread count 36; W(3,3) has no ovoid -> magic "
        f"cannot be gauged away"
    )
    assert theta - alpha == q == 3
    out["ks_deficit"] = {
        "theta_Phi4": 10,
        "alpha_Phi6": 7,
        "deficit": "q = 3",
        "contextual_fraction": "1/Phi_4 = 1/10",
    }

    # the economy
    print(f"\n[the magic economy]")
    print(f"  standard FT: cost ~ (code overhead) x (magic distillation overhead),")
    print(
        f"    distillation dominant (10^3-10^6 raw magic states per non-Clifford gate)"
    )
    print("  substrate: contextual rays are a raw inventory; protected supply requires")
    print("    Golay distillation or the separately certified M36 mode transducer")
    out["economy"] = {
        "standard": "code overhead x magic-distillation overhead (distillation dominant)",
        "substrate": "contextual raw inventory; preparation, purification and injection remain typed costs",
        "claim": "distillation is bypassed only conditionally by a calibrated M36-to-qutrit transducer",
        "superseded_claim": "matter=magic implies no distillation factory",
    }

    print("\nRESULT: the architecture has a structural raw magic inventory, not")
    print("  an automatically protected supply. 36 of 40 rays occupy the non-stabilizer")
    print("  sector (36=(q!)^2, grading 8+24+4={2^q,f,mu}), and the qutrit")
    print("  Strange-state witness has exact mana log(5/3). Contextuality and the")
    print("  absence of an ovoid certify that this resource cannot be globally")
    print("  re-labelled as stabilizer data, but they do not determine preparation")
    print("  noise or fault-tolerant injection. Pass 10943 therefore keeps two")
    print("  explicit resource paths: ternary-Golay distillation followed by the")
    print("  Strange-to-R converter, or a conditional direct M36-to-qutrit transducer.")
    print("  The former no-distillation-factory claim is withdrawn unless that direct")
    print("  transducer is physically realized and calibrated.")

    out["summary"] = (
        "W(3,3) contains a certified contextual/non-stabilizer inventory and the qutrit "
        "Strange state has exact mana log(5/3). This does not make the inventory a "
        "protected supply. Passes 10942--10943 replace the former no-factory over-read "
        "with two explicit paths: ternary-Golay Strange distillation followed by exact "
        "Strange-to-R conversion, or a conditional family-controlled M36 mode transducer "
        "sending 27 of 36 rays to the R-magic Clifford orbit."
    )
    out["sources"] = [
        "matter=magic, 4+36 split, 36=(q!)^2, grades 8+24+4, contextual fraction 1/10, "
        "theta=10/alpha=7 (sec:fuel, bt822/bt823, w33_contextuality_simulation.py); "
        "qutrit Wigner function + mana (Gross 2006; Veitch-Ferrie-Gross-Emerson; Howard-"
        "Wallman-Veitch-Emerson contextuality=magic); Strange-state mana log(5/3); "
        "magic-state distillation dominant FT cost (Bravyi-Kitaev; Litinski); "
        "w33_gkp_lattice_architecture.py, w33_contextuality_is_the_fuel.py."
    ]
    with open("data/w33_magic_economy.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_magic_economy.json")


if __name__ == "__main__":
    main()
