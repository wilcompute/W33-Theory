"""Pass 12721 (1), (3), (4).
 (1) Second-45 Higgs splitting by Goldstone counting.  Decoupled sectors each with its own accidental symmetry: uneaten = sum of broken
     cosets - gauge coset (SO(10) -> SM, 33).  Cases: (a) Sigma (LR, 30) + H (SU(5), 21) [Pass 12716]; (b) Sigma (LR, 30) + a coupled
     (Sigma', H) sector breaking SO(10) all the way to the SM (33), as any H-sector that lifts the 16's triplets through Sigma' must;
     (c) the Pass 12720 eps = 0 content (Q + U + doublets + d^c triplets).  Two-loop unification (Pass 12703 machinery, hybrid M_SS = 1e10,
     light states at 1.74 TeV) for the light content of each case.
 (3) Qudit hardware: measured trapped-ion numbers (Innsbruck single-qutrit Clifford ~2e-3 vs ion qubit ~1e-4; Yb+ two-qudit 92.7% vs ion
     two-qubit 99.9%) against the break-even f < sqrt(log2 3) of Pass 12720.
 (4) Casimir quintessence (arXiv:2603.19819) at R <= 0.2 um: rho_Casimir ~ R^-4 fixed to rho_DE at R0 = 16.4 um -> required suppression of
     the Casimir coefficient at 0.2 um.
usage: py -3 analysis/explore_pass12721_misc.py"""
import json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
res = {}
src16 = open(os.path.join(HERE, "explore_pass12716_round.py"), encoding="utf-8").read()
blk = src16.split("# ======================================================================= (0) GIFT count")[1].split("bS, bH, eaten = ")[0]
G = {"np": np, "math": math}
exec(blk, G)
sm_content, complement, commutant, TBL = G["sm_content"], G["complement"], G["commutant"], G["TBL"]
lr = commutant(TBL); u5 = G["u5"]; sm_alg = G["sm_alg"]
cS, cH, cSM = sm_content(complement(lr)), sm_content(complement(u5)), sm_content(complement(sm_alg))


def diff(*adds, sub):
    tot = {}
    for a in adds:
        for k, v in a.items(): tot[k] = tot.get(k, 0) + v
    for k, v in sub.items(): tot[k] = tot.get(k, 0) - v
    return {k: v for k, v in tot.items() if v}


cases = {"(a) Sigma(LR) + H(SU5)": diff(cS, cH, sub=cSM), "(b) Sigma(LR) + coupled (Sigma', H) -> SM": diff(cS, cSM, sub=cSM)}
for k, v in cases.items():
    print(f"(1) {k}: uneaten {sum(v.values())}: {dict(sorted(v.items()))}")
assert sum(cases["(a) Sigma(LR) + H(SU5)"].values()) == 18 and sum(cases["(b) Sigma(LR) + coupled (Sigma', H) -> SM"].values()) == 30
res["counting"] = cases

src03 = open(os.path.join(HERE, "toe_pass12703_round.py"), encoding="utf-8").read()
G3 = {"__file__": os.path.join(HERE, "toe_pass12703_round.py")}
exec(src03.split("# ======================================================================= (4)")[0], G3)
G3["PIECE"]["X"] = (3, 2, 5 / 6)
uni = {}
for lab, names in (("Q + U (hybrid)", ["Q", "U"]), ("Q + U + X(3,2)_5/6  [case b]", ["Q", "U", "X"]), ("Q + U + D + L  [Pass 12720, eps = 0]", ["Q", "U", "D", "L"])):
    M12, ai, dl = G3["unify"](1740.0, 0.46, names)
    uni[lab] = dict(M12=M12, alpha_inv=ai, delta=dl)
    print(f"(1) light at 1.74 TeV: {lab:38s}: M12 = {M12:.2e}, delta = {dl:+.2f}")
res["unification"] = uni

ions = dict(single=(2e-3, 1e-4), two=(1 - 0.927, 1e-3))
qr = {}
for k, (pq3, pq2) in ions.items():
    f = pq3 / pq2; qr[k] = dict(p_qutrit=pq3, p_qubit=pq2, f=f, passes=f < math.sqrt(math.log2(3)))
    print(f"(3) trapped ions, {k}-qudit gates: qutrit {pq3:.1e} vs qubit {pq2:.1e} -> f = {f:.0f} (break-even 1.26): {'passes' if f < 1.26 else 'fails'}")
res["ions"] = qr

R0, Rmax = 16.4, 0.2
supp = (Rmax / R0) ** 4
print(f"(4) Casimir quintessence: rho ~ R^-4 normalised to rho_DE at {R0} um; at R = {Rmax} um it overshoots by {(R0 / Rmax) ** 4:.1e}: "
      f"the Casimir coefficient must be tuned to {supp:.1e} (or cancel between bosons and fermions to that level)")
res["casimir"] = dict(R0_um=R0, R_max_um=Rmax, required_suppression=supp)
json.dump(res, open(os.path.join(ROOT, "data", "explore_pass12721_misc.json"), "w"), indent=1)
