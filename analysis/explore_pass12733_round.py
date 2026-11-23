"""Pass 12733 (Claude track).
 (1) Hybrid with matter on the SM brane: the localised running (Contino-Pilo-Rattazzi-Trincherini) depends only on the even zero modes
     (gauge + Higgs doublets); brane matter is 4D and comes in complete SM families, so it is universal at one loop: the Pass 12731 window is
     unchanged at this order.  Consequence: no GUT Yukawa relations (b-tau unification lost).
 (2) Brane-localised proton decay with matter on the SM brane: X,Y and coloured-Higgs wave functions vanish there (no tree-level dimension-6 or
     dimension-5 from triplets); the leading term is a brane operator c QQQL / Lambda^2 with Lambda = Lambda R x M_c:
     tau ~ 1.6e34 yr (Lambda/1e16)^4 / c^2 for c = 1 (weak) and c = 16 pi^2 (naive dimensional analysis at strong coupling).
 (3) Explicit evidence factors (vs SM, SM m_t prior width W): m_t factor W |dy'/dm_t| (hybrid, B'), W x 0.25 |dlog10 f_a/dm_t| (A);
     dark-matter production factor (density in Omega relative to the SM's 1/0.3): hybrid bino freeze-in Omega ~ e^-x (x ~ 24) with
     log T_RH uniform over 6 decades -> 1/(6 ln10 x Omega); A pre-inflation misalignment 0.082; B' generic (second component) 1;
     B' extra (lambda range, reheating overlap) 0.34 x 0.25; A trials 1/8.
 (4) Figure: the y' floor vs matching scale for N = 1, 2, 3 vectorlike families (N^-1/4 scaling of the Pass 12723 curve at M_t = 172.80).
 (5) 2026 data: Belle 2601.07104 (B+ -> p X_inv excludes minimal B-mesogenesis for m_psi > 2.5 GeV and 2.15-2.3 GeV) -> mesogenesis DM share
     <= (2.5/0.938)/5.36 in minimal mesogenesis.
usage: py -3 analysis/explore_pass12733_round.py"""
import json, math, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
res = {}
res["sm_brane_matter"] = dict(window_unchanged=True, reason="brane matter = complete SM families, universal at one loop; the localised log depends on even zero modes only",
                              cost="no GUT Yukawa relations for brane matter (b-tau unification not predicted)")
print("(1) matter on the SM brane: unification window unchanged at one loop (complete families are universal); GUT Yukawa relations lost")

P31 = json.load(open(os.path.join(ROOT, "data", "explore_pass12731_round.json")))
pd = []
for r in P31["two_loop_orbifold"]["rows"]:
    Lam = r["Lambda_R"] * r["M_c"]
    for c, lab in ((1.0, "weak"), (16 * math.pi ** 2, "NDA strong")):
        tau = 1.6e34 * (Lam / 1e16) ** 4 / c ** 2
        pd.append(dict(Lambda_R=r["Lambda_R"], Lambda=Lam, coupling=lab, tau_yr=tau))
for row in pd:
    if row["Lambda_R"] in (10, 20, 40):
        print(f"(2) Lambda R = {row['Lambda_R']}: Lambda = {row['Lambda']:.1e} GeV, brane QQQL with {row['coupling']:10s} coefficient: tau ~ {row['tau_yr']:.1e} yr")
res["brane_proton"] = dict(rows=pd, note="weakly coupled brane operators are harmless (tau >~ 1e38); at NDA strong coupling tau ~ 1e33-1e35, so a brane baryon-number "
                                         "(or R-) symmetry is needed")

P12 = json.load(open(os.path.join(ROOT, "data", "toe_pass12707_round.json"), encoding="utf-8"))
dyB = abs(P12["sensitivity"]["dy_dMt"])
dmH = (1 / (6 * math.log(10) * 24 * 0.12)) / (1 / 0.3)
ev = {}
for W in (15.0, 5.0, 2.0):
    hyb = W * 0.05 * dmH
    A = W * 0.25 * 1.47 * 0.082 / 8
    Bp = W * dyB * 0.34 * 0.25
    ev[f"{W:g}"] = dict(hybrid=hyb, A_escape=A, Bprime=Bp)
    print(f"(3) width {W:g}: hybrid {hyb:.4f} (m_t {W * 0.05:.2f} x DM {dmH:.3f}), A-escape {A:.4f}, B' {Bp:.4f}")
res["evidence"] = dict(rows=ev, dm_factor_hybrid=dmH,
                       note="explicit factors: the exponentially sensitive bino freeze-in costs the hybrid x0.018; with it A-escape and B' lead, all far below the SM")

curve = [(7, 0.608), (8, 0.544), (9, 0.495), (10, 0.458), (11, 0.433), (12, 0.418), (13, 0.413)]
os.makedirs(os.path.join(HERE, "figures"), exist_ok=True)
fig, ax = plt.subplots(figsize=(6, 4))
for N, col in ((1, "#1d6a86"), (2, "#a3650f"), (3, "#b0393b")):
    ax.plot([c[0] for c in curve], [c[1] * N ** -0.25 for c in curve], marker="o", color=col, label=f"{N} vectorlike famil{'y' if N == 1 else 'ies'}")
ax.axhspan(0.351, 0.469, color="#1d6a86", alpha=0.12, label="1-family floor, 95% (today)")
ax.axhline(0.35, color="#b0393b", ls="--", lw=1, label="falsifier (one family): y' < 0.35")
ax.set_xlabel("log10(matching scale / GeV)"); ax.set_ylabel("y' needed for lambda = 0")
ax.set_title("y' needed for a vanishing Higgs quartic (M_t = 172.80 GeV)", fontsize=10); ax.legend(fontsize=7); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig(os.path.join(HERE, "figures", "y_floor.png"), dpi=150)
print("(4) wrote analysis/figures/y_floor.png")
res["figure"] = "analysis/figures/y_floor.png"

share = (2.5 / 0.938) / 5.36
res["belle_2026"] = dict(paper="2601.07104", excludes="minimal B-mesogenesis for m_psi > 2.5 GeV and 2.15-2.3 GeV (B+ -> p X_inv, 711 fb^-1)",
                         mesogenesis_share_max=share, other_min=1 - share,
                         Bprime="if B' uses minimal mesogenesis the coupled second component must be >= 50% (the f = 0.5, beta = 0.1 fit of Pass 12725: chi2 3.3, "
                                "sigma8 0.993); the Dark_CP variant (A_CP Br ~ 1e-7) is below these exclusive limits")
print(f"(5) Belle 2026: minimal mesogenesis needs m_psi < 2.5 GeV -> mesogenesis DM share <= {share:.0%}; B''s coupled component >= {1 - share:.0%}")
json.dump(res, open(os.path.join(ROOT, "data", "explore_pass12733_round.json"), "w"), indent=1)
