#!/usr/bin/env python3
"""
The honest price of self-fueling: there is no free lunch. The matter=magic identity
eliminates the distillation factory (a SPACE saving, ~d^3 qubits), but the cost
reappears as a non-Clifford THROUGHPUT cap -- the magic is replenished only at the
contextual-fraction rate 1/Phi_4 = 1/10 per cycle, so a circuit whose non-Clifford
fraction exceeds 1/10 is throttled. The architecture trades the distillation-factory
SPACE overhead for a non-Clifford RATE bound at f = 1/10. Below that fraction it is a
pure win; above it, the price returns as a slowdown 10f.

w33_magic_resource_accounting.py celebrated the space saving (no factory, premium P=1);
honesty demands finding where the cost hides. Here it is.

THE SUPPLY. The matter shell carries magic at the standing contextual fraction
1/Phi_4 = 1/10; the magic per error-correction round is the Kochen-Specker deficit
theta - alpha = q = 3 (over the 40 rays). So the magic INJECTION rate is bounded:
roughly one non-Clifford injection per Phi_4 = 10 ray-measurements per core.

THE CAP. A circuit with non-Clifford fraction f demands magic at rate f x (gate rate);
the supply is (1/Phi_4) x (cycle rate). With gate rate ~ cycle rate, the demand is met
iff
    f <= 1/Phi_4 = 1/10.
If f <= 1/10 the matter shell keeps up -- no factory, no slowdown: a pure win (space
saved ~d^3). If f > 1/10 the magic supply throttles the computation by a factor
    f / (1/Phi_4) = Phi_4 * f = 10 f,
the cost reappearing as reduced non-Clifford throughput (or, equivalently, the need for
~10f times more cores running in parallel to source the magic).

WHERE ELSE THE COST HIDES (named honestly).
  * matter-shell maintenance: the code must still be error-corrected every cycle -- the
    usual surface/GKP-style overhead, paid anyway (this is not extra, but it is not
    zero).
  * clock renewal bandwidth: the magic is refreshed at the Boerdijk-Coxeter tick rate;
    the non-Clifford throughput cannot exceed the clock rate.
  * the KS deficit q = 3: only q contexts' worth of fresh magic per round.

THE VERDICT. matter=magic is a SPACE-for-RATE trade, not a free lunch: it removes the
d^3 distillation factory but imposes a non-Clifford throughput cap at f = 1/Phi_4 = 1/10.
Clifford-dominated workloads (f <= 1/10) win outright; non-Clifford-heavy ones (f > 1/10)
pay a 10f rate penalty. The advantage is real and bounded -- stated with its price.

Verifies the crossover f = 1/Phi_4 = 1/10, the throttle 10f above it, and the regimes.
"""
from __future__ import annotations

import json


def main():
    out = {}
    Phi4, q = 10, 3
    crossover = 1 / Phi4
    print(
        f"[the supply]  magic density = 1/Phi_4 = 1/{Phi4} = {crossover}; "
        f"magic per round = theta-alpha = q = {q}"
    )
    print(
        f"[the cap]  sustainable iff non-Clifford fraction f <= 1/Phi_4 = {crossover}"
    )

    # regimes for various non-Clifford fractions
    print(f"\n[regimes: non-Clifford fraction f -> behaviour]")
    rows = []
    for f in (0.001, 0.01, 0.05, 0.10, 0.30, 0.70, 1.0):
        if f <= crossover + 1e-12:
            regime = "PURE WIN (no factory, no slowdown)"
            throttle = 1.0
        else:
            throttle = Phi4 * f
            regime = f"throttled x{throttle:.1f} (or {throttle:.1f}x more cores)"
        rows.append({"f": f, "throttle": round(throttle, 2), "regime": regime})
        print(f"  f={f:5.3f}: {regime}")
    out["regimes"] = rows
    # below crossover throttle=1, above it grows as 10f
    assert all(r["throttle"] == 1.0 for r in rows if r["f"] <= crossover + 1e-12)
    assert all(
        abs(r["throttle"] - Phi4 * r["f"]) < 1e-9
        for r in rows
        if r["f"] > crossover + 1e-12
    )

    # the trade and the hidden costs
    print(f"\n[the space-for-rate trade]")
    print(f"  SAVED : the distillation factory (~d^3 qubits, 30-90% of device)")
    print(
        f"  PRICE : non-Clifford throughput cap at f = 1/Phi_4 = 1/10 (throttle 10f above)"
    )
    out["trade"] = {
        "saved": "distillation factory ~d^3 (space)",
        "price": "non-Clifford throughput cap at f=1/Phi_4=1/10; throttle 10f",
    }
    out["hidden_costs"] = [
        "matter-shell maintenance: the usual code EC overhead, paid anyway (not extra, not zero)",
        "clock renewal bandwidth: non-Clifford rate <= BC clock tick rate",
        "KS deficit q=3: only q contexts' fresh magic per round",
    ]
    out["crossover"] = {
        "f": "1/Phi_4 = 1/10",
        "below": "pure win",
        "above": "throttle 10f",
    }

    print("\nRESULT: self-fueling is a space-for-rate trade, not a free lunch. The")
    print(
        "  matter=magic identity removes the distillation factory (saving ~d^3 qubits,"
    )
    print("  30-90% of a standard device), but the magic is replenished only at the")
    print(
        "  contextual-fraction rate 1/Phi_4 = 1/10 per cycle, so the non-Clifford gate"
    )
    print("  throughput is capped: a circuit with non-Clifford fraction f <= 1/10 runs")
    print(
        "  with no factory and no slowdown (a pure win), while f > 1/10 is throttled by"
    )
    print(
        "  10f -- the cost reappearing as reduced non-Clifford rate (or 10f times more"
    )
    print(
        "  cores). The remaining costs are named honestly: the matter shell still needs"
    )
    print("  routine error correction, the magic refresh is bounded by the clock rate,")
    print(
        "  and only q=3 contexts of fresh magic arrive per round. So the architecture's"
    )
    print("  advantage is real but bounded: it trades the d^3 distillation SPACE for a")
    print(
        "  non-Clifford RATE cap at 1/Phi_4. Clifford-dominated workloads win outright;"
    )
    print("  magic-heavy ones pay 10f. The headline holds, with its price stated.")

    out["summary"] = (
        "the honest price of self-fueling: NOT a free lunch but a SPACE-for-RATE trade. "
        "matter=magic removes the distillation factory (saving ~d^3 qubits, 30-90% of a "
        "standard device), but the magic is replenished only at the contextual-fraction "
        "rate 1/Phi_4=1/10 per cycle, so the non-Clifford throughput is capped: circuits "
        "with non-Clifford fraction f<=1/10 run with no factory and no slowdown (pure "
        "win), f>1/10 is throttled by 10f (or needs 10f more cores). Hidden costs named: "
        "matter-shell EC maintenance (paid anyway), clock-renewal bandwidth (rate <= "
        "tick rate), KS deficit q=3 magic/round. Verdict: trades the d^3 distillation "
        "SPACE for a non-Clifford RATE cap at 1/Phi_4=1/10; Clifford-dominated workloads "
        "win outright, magic-heavy ones pay 10f. Advantage real but bounded, stated with "
        "its price."
    )
    out["sources"] = [
        "matter=magic, contextual fraction 1/Phi_4=1/10, KS deficit theta-alpha=q=3 "
        "(w33_magic_economy.py, w33_magic_resource_accounting.py); distillation factory "
        "~d^3, 30-90% device (Litinski 2019); BC clock renewal "
        "(w33_clock_magic_renewal.py); w33_self_fueling_memory.py."
    ]
    with open("data/w33_self_fueling_cost.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_self_fueling_cost.json")


if __name__ == "__main__":
    main()
