#!/usr/bin/env python3
"""
The interrupt controller of the Holonet microkernel: the tax arc, made executable inside the VM track.
The parallel VM/OS track's microkernel table maps "interrupt = point-star defect/escalation",
"scheduler tick = spread frame", and "relocation = automorphism action" -- rows that were, until now,
descriptive. The tax arc (Passes 57-61) proved the theorems those rows need: the defect is one movable
point-star; every spread frame serves exactly 9/10 under any optimum; the per-node vector table is the
AG(2,3) of ground states; and the runtime group moves everything. This witness fuses the two tracks
into a runnable interrupt controller whose runtime invariants ARE the committed theorems, and derives
one genuinely new law from the fusion:

  THE CLOSED-FORM VECTOR TABLE. ground(T) = T UNION (Gamma(p) \\ T-perp): for each of the nine
  all-centers-in-perp triads T at a center p, the ground state is T plus the perp minus T's four
  centers -- and the unlit quad IS the center quad, a transversal of the defect star. Verified equal,
  set-for-set, to the ILP enumeration. The controller builds its vector table in closed form; no
  optimizer runs at interrupt time.

  THE MIGRATION PRICE LAW (new, from the 360-orbit gluing). Computing the lit-set overlap of every
  pair of the 360 ground states, classified by the relation of their defect centers:
      same center:          overlap always 5   (vector switch costs 11-5 = 6 rays)
      collinear centers:    overlaps {0,2,3,8} (cheapest migration 11-8 = 3 rays)
      non-collinear:        overlaps {1,2,4,6} (cheapest 11-6 = 5 rays)
  and each ground state has EXACTLY 8 cheap (overlap-8) partners, sitting 2-per-center at exactly 4
  collinear centers -- which are the ground's OWN CENTER QUAD (its unlit neighbors). So the interrupt
  migrates cheapest ALONG FABRIC EDGES -- locality emerges in the OS layer -- its escape routes are
  written into its own vector (the unlit quad doubles as the cheap-target list), and, strikingly,
  relocating the defect to a neighboring node (3 rays) costs LESS than re-vectoring in place (6 rays).

  THE CONTROLLER. A seeded event loop over the 40 contexts: non-defect events are serviced in spread
  frames (each frame provably 9/10); defect-line events are escalations (the priced 9^t path, counted);
  when escalations at the current center exceed a threshold, the controller relocates the defect to the
  least-loaded collinear center through an overlap-8 cheap channel. Device ports follow the VM track's
  USB mapping: interrupt-class transfers inject defect-star urgent events, bulk-class inject ordinary
  line traffic. At every step the controller ASSERTS the theorems as runtime invariants: the failure
  set is exactly one star (Pass 57), the frame service rate is exactly 9/10 (Pass 58), the loading is
  uniform (2,2,2,2) (Pass 58/59), the vector table has exactly 9 closed-form entries (Pass 61), and
  every relocation lands on a valid ground state (Pass 59's orbit theorem).

Honest scope: the price law and vector-table closed form are exact finite computations; the controller
is a classical seeded simulation whose invariant checks bind it to the committed theorems -- it is the
interrupt layer the VM track's packet VM can adopt, not a claim about that in-flight code. Escalation
pricing cites the committed 9^t dial; no wall-clock claims.
"""

from __future__ import annotations

import json
import os
import random
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import w33_ground_affine_plane as gap  # noqa: E402
import w33_master_audit as audit  # noqa: E402
import w33_spread_star_anatomy as anat  # noqa: E402
import w33_tax_orbits as orb  # noqa: E402


def vector_table(p, pts, A, lines, n):
    """Closed-form vector table at center p: ground(T) = T + (Gamma(p) - T-perp), for the
    all-centers-in-perp triads T. Returns list of (lit frozenset, triad, center_quad).
    """
    from itertools import combinations

    nb = frozenset(j for j in range(n) if A[p][j])
    nonn = sorted(set(range(n)) - nb - {p})
    table = []
    for t in combinations(nonn, 3):
        a, b, c = t
        if A[a][b] or A[a][c] or A[b][c]:
            continue
        perp = tuple(j for j in range(n) if A[j][a] and A[j][b] and A[j][c])
        if len(perp) == 4 and all(x in nb for x in perp):
            table.append((frozenset(t) | (nb - set(perp)), t, perp))
    return table, nb


def migration_price_law(pts, A, lines, B):
    """The gluing spectrum of the 360 ground states, classified by center relation."""
    gens, G = orb.build_group(pts, B)
    n = len(pts)
    tbl0, _ = vector_table(0, pts, A, lines, n)
    g0 = tbl0[0][0]
    orbit = {g0}
    frontier = [g0]
    while frontier:
        nxt = []
        for x in frontier:
            for g in gens:
                y = frozenset(g[i] for i in x)
                if y not in orbit:
                    orbit.add(y)
                    nxt.append(y)
        frontier = nxt
    olist = sorted(orbit, key=sorted)
    cen = {}
    for o in olist:
        c, occ = orb.optimum_profile(o, lines)
        cen[o] = c
    spec = Counter()
    cheap_partners = Counter()
    for i, a in enumerate(olist):
        for b in olist[i + 1 :]:
            ca, cb = cen[a], cen[b]
            rel = "same" if ca == cb else ("collinear" if A[ca][cb] else "noncollinear")
            ov = len(a & b)
            spec[(rel, ov)] += 1
            if rel == "collinear" and ov == 8:
                cheap_partners[a] += 1
                cheap_partners[b] += 1
    return len(orbit), spec, cheap_partners, cen


class InterruptController:
    """The tax arc as a running microkernel interrupt layer."""

    def __init__(self, pts, A, lines, n, spreads, center=0, threshold=4, seed=0):
        self.pts, self.A, self.lines, self.n = pts, A, lines, n
        self.spreads = spreads
        self.rng = random.Random(seed)
        self.threshold = threshold
        self.invariant_failures = []
        self.counters = Counter()
        self._move_to(center, prefer=None)

    def _star(self, p):
        return [li for li, L in enumerate(self.lines) if p in L]

    def _move_to(self, p, prefer):
        table, nb = vector_table(p, self.pts, self.A, self.lines, self.n)
        if len(table) != 9:
            self.invariant_failures.append("vector table size != 9 (Pass 61)")
        if prefer is not None:
            lit = max((t[0] for t in table), key=lambda L: len(L & prefer))
            self.counters["migration_cost_rays"] += 11 - len(lit & prefer)
        else:
            lit = table[0][0]
        # runtime invariants (the theorems)
        c, occ = orb.optimum_profile(lit, self.lines)
        if c != p:
            self.invariant_failures.append(
                "failure set is not the star of the target center (Pass 57)"
            )
        if occ != (2, 2, 2, 2):
            self.invariant_failures.append("loading not uniform (2,2,2,2) (Pass 58/59)")
        self.center, self.lit, self.star = p, lit, set(self._star(p))
        self.escalations_here = 0

    def service(self, li):
        """One event on context li: classical spread-frame service, or escalation on the defect."""
        if li in self.star:
            self.counters["escalations"] += 1
            self.escalations_here += 1
            if self.escalations_here >= self.threshold:
                self._relocate()
            return "escalated"
        frame = next(S for S in self.spreads if li in S)
        served = sum(1 for x in frame if x not in self.star)
        if served != 9:  # Pass 58: every spread frame is exactly 9/10
            self.invariant_failures.append("spread frame not 9/10 (Pass 58)")
        self.counters["classical_services"] += 1
        return "serviced"

    def _relocate(self):
        """Cost-aware relocation: prefer cheap (overlap-8) channels, tie-break by load.

        The cheap channels of a ground sit at exactly 4 of the 12 collinear centers -- its own
        center quad (the unlit neighbors) -- so the controller checks those first.
        """
        nbrs = [x for x in range(self.n) if self.A[self.center][x]]
        best = None
        for x in nbrs:
            tbl, _ = vector_table(x, self.pts, self.A, self.lines, self.n)
            ov = max(len(t[0] & self.lit) for t in tbl)
            key = (11 - ov, self.counters[f"load@{x}"])
            if best is None or key < best[0]:
                best = (key, x)
        target = best[1]
        self.counters["relocations"] += 1
        self._move_to(target, prefer=self.lit)
        self.counters[f"load@{target}"] += 1

    def inject_device(self, endpoint_point, transfer_class):
        """Device-port hook per the VM track's USB mapping."""
        if transfer_class == "interrupt":
            li = self.rng.choice(sorted(self.star))  # point-star urgent packet
        else:  # bulk: ordinary line traffic near the endpoint
            li = self.rng.choice(
                [i for i, L in enumerate(self.lines) if endpoint_point in L]
            )
        return self.service(li)


def main():
    print(
        "== the interrupt controller: the tax arc running inside the VM track's microkernel ==\n"
    )
    checks = []

    def chk(name, ok):
        checks.append((name, bool(ok)))
        print(f"  [{'PASS' if ok else 'FAIL'}]  {name}")

    pts, A, lines, B = audit._build(3)
    n = len(pts)

    # A. closed-form vector table == ILP
    tbl0, nb0 = vector_table(0, pts, A, lines, n)
    sols, star0 = anat._enumerate_optima_for_center(lines, n, 0)
    ilp = {
        frozenset(i for i, v in enumerate(s) if v)
        for s in sols
        if s[0] == 0
        and tuple(sorted(sum(s[p] for p in lines[li]) for li in star0)) == (2, 2, 2, 2)
    }
    chk(
        "CLOSED FORM: ground(T) = T + (Gamma(p) - T-perp) reproduces the ILP vector table exactly",
        {t[0] for t in tbl0} == ilp and len(tbl0) == 9,
    )
    sl = {}
    for li in star0:
        for u in lines[li]:
            if u != 0:
                sl[u] = li
    chk(
        "the unlit quad IS the center quad, a transversal of the defect star",
        all(
            sorted(Counter(sl[c] for c in perp).values()) == [1, 1, 1, 1]
            for (_, t, perp) in tbl0
        ),
    )

    # B. the migration price law
    n_orbit, spec, cheap, cen = migration_price_law(pts, A, lines, B)
    chk(f"the ground bundle has 360 states (got {n_orbit})", n_orbit == 360)
    same_ov = sorted({ov for (rel, ov) in spec if rel == "same"})
    col_ov = sorted({ov for (rel, ov) in spec if rel == "collinear"})
    non_ov = sorted({ov for (rel, ov) in spec if rel == "noncollinear"})
    chk(
        f"same-center overlaps always 5 (vector switch costs 6 rays): {same_ov}",
        same_ov == [5],
    )
    chk(
        f"collinear overlaps {col_ov} with max 8 (cheapest migration 3 rays)",
        col_ov == [0, 2, 3, 8],
    )
    chk(
        f"non-collinear overlaps {non_ov} with max 6 (cheapest 5 rays)",
        non_ov == [1, 2, 4, 6],
    )
    chk(
        "PRICE LAW: relocating to a neighbor (3 rays) beats re-vectoring in place (6 rays); "
        "the interrupt migrates cheapest along fabric edges",
        max(col_ov) > 5 > 11 - 6 - 2,
    )
    chk(
        f"every ground has EXACTLY 8 cheap (overlap-8) channels, all at collinear centers "
        f"(got {sorted(set(cheap.values()))})",
        set(cheap.values()) == {8} and len(cheap) == 360,
    )
    # where the cheap channels sit: 2 at each of 4 centers = the ground's own center quad
    g0 = tbl0[0][0]
    quad0 = set(tbl0[0][2])
    cheap_centers = Counter()
    for o in cen:
        if o != g0 and len(o & g0) == 8:
            cheap_centers[cen[o]] += 1
    chk(
        f"the cheap channels sit 2-per-center at exactly 4 centers = the ground's own CENTER QUAD "
        f"(the unlit neighbors): {sorted(cheap_centers) == sorted(quad0)}",
        set(cheap_centers.values()) == {2} and set(cheap_centers) == quad0,
    )

    # C. the controller, run
    spreads = anat.enumerate_spreads(lines, n)
    ctl = InterruptController(pts, A, lines, n, spreads, center=0, threshold=4, seed=7)
    rng = random.Random(42)
    for _ in range(2000):
        ctl.service(rng.randrange(len(lines)))
    for _ in range(50):
        ctl.inject_device(endpoint_point=5, transfer_class="interrupt")
        ctl.inject_device(endpoint_point=5, transfer_class="bulk")
    c = ctl.counters
    chk(
        f"controller ran 2100 events: {c['classical_services']} classical, {c['escalations']} escalations, "
        f"{c['relocations']} relocations",
        c["classical_services"] + c["escalations"] == 2100,
    )
    chk(
        "ALL runtime invariants held (Pass 57 star, Pass 58 9/10 + uniform loading, Pass 61 table)",
        not ctl.invariant_failures,
    )
    avg_cost = c["migration_cost_rays"] / max(c["relocations"], 1)
    chk(
        f"every relocation used a cheap channel: average migration cost {avg_cost:.2f} = 3 rays",
        avg_cost == 3.0,
    )

    all_ok = all(ok for _, ok in checks)
    print(
        "\nFUSION: the VM track's microkernel rows (interrupt = point-star escalation, tick = spread"
        "\nframe, relocation = automorphism action) now run on the tax arc's theorems as live invariants,"
        "\nwith a closed-form vector table and a new price law: same-center re-vector = 6 rays, edge"
        "\nmigration = 3, non-collinear = >= 5. The defect moves like a particle that prefers the fabric's"
        "\nedges -- and moving it next door is cheaper than reconfiguring in place."
    )
    print(f"\n{'ALL PASS' if all_ok else 'FAILURES present.'}")

    out = {
        "closed_form_vector_table": "ground(T) = T + (Gamma(p) - T_perp); unlit quad = center quad = star transversal",
        "migration_price_law": {
            "same_center_overlap": same_ov,
            "collinear_overlaps": col_ov,
            "noncollinear_overlaps": non_ov,
            "costs_rays": {
                "revector_in_place": 6,
                "edge_migration": 3,
                "noncollinear_min": 5,
            },
            "cheap_channels_per_ground": 8,
            "spectrum_counts": {
                f"{rel}:{ov}": v for (rel, ov), v in sorted(spec.items())
            },
        },
        "controller_run": {
            "events": 2100,
            "classical_services": c["classical_services"],
            "escalations": c["escalations"],
            "relocations": c["relocations"],
            "avg_migration_cost_rays": avg_cost,
            "invariant_failures": ctl.invariant_failures,
        },
        "all_pass": bool(all_ok),
        "summary": (
            "the interrupt controller: the tax arc running inside the VM track's microkernel. The VM/OS "
            "track's table rows (interrupt = point-star defect/escalation; scheduler tick = spread frame; "
            "relocation = automorphism action; USB interrupt transfer = point-star urgent packet) are made "
            "executable with the tax theorems as RUNTIME INVARIANTS. CLOSED FORM: ground(T) = T + "
            "(Gamma(p) - T_perp) rebuilds the 9-entry AG(2,3) vector table with no optimizer (verified == "
            "ILP; the unlit quad IS the center quad, a star transversal). NEW MIGRATION PRICE LAW from "
            "the 360-state bundle gluing: same-center overlap always 5 (re-vector costs 6 rays); "
            "collinear-center overlaps {0,2,3,8} (cheapest migration 3 rays); non-collinear {1,2,4,6} "
            "(>=5); every ground has exactly 8 cheap channels, 2-per-center at exactly 4 collinear "
            "centers = the ground's OWN CENTER QUAD (its unlit neighbors): the interrupt's escape routes "
            "are written into its own vector, it migrates cheapest along fabric edges, and moving next "
            "door beats reconfiguring in place. The seeded "
            "controller (2100 events incl. device-port interrupt/bulk injections) held every invariant "
            "and used only cheap channels (avg cost 3.00). HONEST: exact price/table computations; a "
            "classical simulation bound to committed theorems; the escalation price cites the 9^t dial; "
            "complements (does not modify) the in-flight packet VM and multi-star packing/queue work."
        ),
        "sources": [
            "VM/OS track: microkernel table + packet VM + loader (in-flight); tax packing/queue witnesses (in-flight)",
            "tax arc: w33_contextuality_tax (57), w33_spread_star_anatomy (58), w33_tax_orbits (59), w33_perp_states (60), w33_ground_affine_plane (61)",
            "the 9^t dial (w33_magic_dial) for escalation pricing",
        ],
    }
    with open("data/w33_interrupt_controller.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("wrote data/w33_interrupt_controller.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
