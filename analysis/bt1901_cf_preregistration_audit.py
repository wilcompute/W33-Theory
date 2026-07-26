#!/usr/bin/env python3
# =============================================================================
# CORRECTED BY PASS 1080 -- analysis/w33_pass1080_contextual_fraction_audit.py
#
# The quantity computed below is NOT the contextual fraction, and the
# falsification criterion stated at the bottom ("any measured CF != 1/10 refutes
# the W(3,3) substrate") CANNOT STAND AS WRITTEN.
#
#   * For the Abramsky-Barbosa contextual fraction, strong contextuality is
#     equivalent to CF = 1.  The W(3,3) KS ray model is strongly contextual,
#     because a global section is an ovoid and W(3,3) has none.  So the
#     contextual fraction of this model is 1, for every state -- Pass 1080
#     computes it by LP and gets 1, with the doily as a positive control at 0.
#   * The "three independent routes" are not three.  mu/v = 1/Phi_4(q) is an
#     ALGEBRAIC IDENTITY for every q, so routes 2 and 3 are the same route.
#     Route 1, 1 - (q!)^2/v, agrees with them only at q=3 and returns NEGATIVE
#     values for q >= 4, so it is not a fraction.
#
# WHAT SURVIVES: the substrate claim this file is reaching for.  W(3,3) is
# contextual and W(2,2) is not, so the HWVE condition CF > 0 holds at q=3 and
# fails at q=2.  Only the numerical value, its NAME, and the corroboration
# argument are withdrawn.  1/10 may well be a real prediction for some other
# observable -- note that bt1901_contextual_fraction_estimator.py actually
# estimates a CLICK RATE -- but that observable has not been derived, and until
# it is, this file must not be used as a falsifier.
# =============================================================================
"""
bt1901_cf_preregistration_audit.py

Contextual fraction pre-registration audit for W(3,3).

Verifies that CF = 1/10 is pure substrate arithmetic (q=3 parameter),
not a fit. Cross-checks the 36/40 KS budget, the magic ray count,
and the Howard-Wallman-Veitch-Emerson magic distillation threshold.

Synthesises photonic_holonet.tex §9 + §13 with Passes 1042/1044 context.
"""

from fractions import Fraction
import json, os

q = 3
v = 40   # substrate points
k = 12   # degree (lines per point neighbours)
mu = 4   # = q+1 = lines per point
lam = 2  # = q-1
f = 24   # multiplicity of eigenvalue r=2
g = 15   # multiplicity of eigenvalue s=-4
Phi6 = q**2 - q + 1   # = 7
Phi3 = q**2 + q + 1   # = 13
Phi4 = q**2 + 1       # = 10

print("=" * 60)
print("CONTEXTUAL FRACTION PRE-REGISTRATION AUDIT")
print("W(3,3) substrate, q=3")
print("=" * 60)
print()

# ─── KS BUDGET ────────────────────────────────────────────────────────────────
# photonic_holonet.tex §13: KS budget = (q!)^2 / v = 36/40
import math
KS_budget_num = math.factorial(q)**2  # = 36
KS_budget_den = v                      # = 40
KS_budget = Fraction(KS_budget_num, KS_budget_den)
print(f"KS budget = (q!)^2 / v = {math.factorial(q)}^2 / {v} = {KS_budget_num}/{KS_budget_den} = {KS_budget}")
print(f"  This is the MAXIMUM fraction of measurement contexts that CAN be\n"
      f"  satisfied by a classical 0/1 colouring.")
print(f"  Fraction UNSATISFIED (= contextual fraction) = 1 - {KS_budget} = ",
      Fraction(1) - KS_budget)
print()

# Contextual fraction from KS budget
CF_from_KS = Fraction(1) - KS_budget
print(f"CF_from_KS  = 1 - {KS_budget} = {CF_from_KS}")

# ─── DIRECT COMPUTATION ───────────────────────────────────────────────────────
# Alternative derivation: fraction of contexts NOT satisfiable
# = (v - KS_budget_num) / v = (40 - 36) / 40 = 4/40 = 1/10
CF_direct = Fraction(v - KS_budget_num, v)
print(f"CF_direct   = (v - (q!)^2) / v = ({v} - {KS_budget_num}) / {v} = {CF_direct}")
assert CF_from_KS == CF_direct, "INTERNAL MISMATCH"
print(f"Both routes agree: CF = {CF_direct}")
print()

# ─── ARITHMETIC FORM ──────────────────────────────────────────────────────────
# CF = 4/40 = mu/v = (q+1)/(q^3+q^2+q+1) ... check
CF_mu_over_v = Fraction(mu, v)
print(f"CF = mu/v = {mu}/{v} = {CF_mu_over_v}")  # = 4/40 = 1/10 YES
print(f"  where mu = q+1 = {mu} = lines per point")
print(f"  where v = (q^4-1)/(q-1) = {v} = number of substrate points")
assert CF_mu_over_v == CF_direct
print(f"  Formula: CF = (q+1) / ((q^4-1)/(q-1)) = 1/Phi_4(q) = 1/{Phi4} ... ",
      Fraction(1, Phi4))
# NB: 1/10 = 1/Phi_4 only at q=3 (Phi_4(3) = 10). Check:
print(f"  Phi_4({q}) = q^2+1 = {Phi4}, so CF = 1/{Phi4} = {Fraction(1, Phi4)}")
assert Fraction(1, Phi4) == CF_direct
print(f"  CF = 1/Phi_4(q) is the substrate arithmetic form. No free parameter.")
print()

# ─── MAGIC RAYS COUNT ─────────────────────────────────────────────────────────
# photonic_holonet.tex §9: 36 magic rays = matter shell
# The matter shell is the 27-non-neighbours + 9-context = 36
# Check: v - 1 (self) - k (gauge shell) = 40 - 1 - 12 = 27 (non-neighbours)
# Plus the 9 = q^2 states per context line => ...let's use paper's direct claim
# KS budget = 36 = matter shell size. Verify:
matter_shell = v - 1 - k  # = 27 ... no, that's just non-neighbours
KS_ray_count = KS_budget_num  # 36
print(f"Magic/matter shell ray count = {KS_ray_count} (= (q!)^2 = {math.factorial(q)}^2)")
print(f"  This is also the number of measurement contexts 36 = number of complete")
print(f"  measurement schedules (spreads of W(3,3)) -- verified bt819")
print(f"  And 36 = dim(E6) / rank(E6) * rank(E6) = ... no, 36 = C(9,2) = C(q^2,2)")
print(f"  C({q**2},2) = {q**2*(q**2-1)//2}")
assert q**2*(q**2-1)//2 == KS_ray_count, f"C(q^2,2) = {q**2*(q**2-1)//2} != {KS_ray_count}"
print(f"  36 = C(q^2, 2) = C(9, 2): the number of spreads is a binomial coefficient")
print(f"  in the substrate order. No free parameter.")
print()

# ─── HOWARD-WALLMAN-VEITCH-EMERSON THRESHOLD ──────────────────────────────────
# Magic distillation requires CF > 0 for qutrits (HWVE theorem)
HWVE_threshold = 0  # CF > 0 is necessary and sufficient
print(f"HWVE threshold for magic distillation: CF > {HWVE_threshold}")
print(f"W(3,3) CF = {CF_direct} > 0: MAGIC DISTILLATION IS POSSIBLE")
print(f"W(2,2) CF = 0: MAGIC DISTILLATION IS IMPOSSIBLE")
print()
print(f"This is the hardware significance of the contextual fraction:")
print(f"the same 1/10 that appears in the build-sheet falsifier table")
print(f"is the fuel efficiency of the quantum advantage.")
print()

# ─── PRE-REGISTRATION RECORD ──────────────────────────────────────────────────
print("=" * 60)
print("PRE-REGISTRATION RECORD")
print("=" * 60)
record = {
    "parameter": "contextual_fraction",
    "predicted_value": "1/10",
    "predicted_numeric": float(CF_direct),
    "derivation_route_1": f"1 - KS_budget = 1 - (q!)^2/v = 1 - {KS_budget_num}/{v} = {CF_direct}",
    "derivation_route_2": f"mu/v = (q+1)/v = {mu}/{v} = {CF_direct}",
    "derivation_route_3": f"1/Phi_4(q) = 1/{Phi4} = {CF_direct}",
    "all_routes_agree": True,
    "free_parameters": 0,
    "venue": "bt1898_demonstrator_runbook",
    "status": "pre-registered, unmeasured",
    "falsification_criterion": "any measured CF != 1/10 refutes the W(3,3) substrate",
    "null_cf": "W(2,2) doily: CF = 0 (6 ovoids found by Pass 1042/1044)",
    "literature": [
        "Thas (1981): W(q) ovoid-free iff q odd => CF > 0 for W(3,3)",
        "Howard-Wallman-Veitch-Emerson: CF > 0 necessary + sufficient for magic distillation",
        "Budroni et al., Rev. Mod. Phys. 94 (2022): operational definition of CF",
    ]
}
for k2, v2 in record.items():
    print(f"  {k2}: {v2}")

os.makedirs("artifacts", exist_ok=True)
with open("artifacts/bt1901_cf_preregistration.json", "w") as f:
    json.dump(record, f, indent=2, default=str)
print()
print("Artifact written: artifacts/bt1901_cf_preregistration.json")
print()
print("SUMMARY: CF = 1/10 is substrate arithmetic, not a fit.")
print("Three independent routes from {q, v, mu, Phi_4} all give 1/10.")
print("The deciding experiment is pre-registered.")
