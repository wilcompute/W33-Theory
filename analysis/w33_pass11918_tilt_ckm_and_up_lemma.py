"""Pass 11918: the frame tilt gives a realistic first-generation down mass, but not the CKM -- and the reason is an exact
up-sector selection rule of magnetized SU(5).

1. Up lemma (all 12 det-3 fluxes, random compatible moduli and Wilson lines). In SU(5) the 10 carries Q, u^c and e^c on
   one brane, so a single-Higgs-mode 10.10 Yukawa is MONOMIAL: its support is the permutation matrix of an involution
   a -> c - a on Z3 with exactly one fixed point -- for every modulus and every Wilson line, including a hypercharge one.
   With a common Wilson line (unbroken SU(5)) the two entries of the 2-cycle are equal (theta evenness), so the spectrum
   always has a DEGENERATE PAIR (to 1e-15). This corrects the CKM samples of Passes 11915/11916, which gave Q and u^c
   independent Wilson lines without a GUT-breaking source.
2. The consistent source is a hypercharge Wilson line w: zeta_X = zeta_rep + Y_X N_rep^{-1} w. It lifts the degeneracy
   (min gap 2e-3 over the 12 fluxes), keeps the H_d position consistent (N10(z_e - z_Q) + N5(z_L - z_d) = 0), and
   makes the lepton Yukawa equal to the down Yukawa at the relative Wilson line shifted by the SCALAR (5m/18) w
   (checked on the spectra), so down and lepton spectra are identically distributed: no Georgi-Jarlskog factor.
3. Consequence of 1: the up mass basis is exactly the magnetic-translation basis of the 10, and the CKM is the down
   sector's left rotation in that basis -- nothing ties it to m_d/m_s.
4. Frozen scan of the (1,1,4) tilt model (279 moduli x 300 Higgs choices, data/w33_pass11918_tilt_scan_frozen.json):
   m_d/m_s > 0.01 in 17% of rows (the tilt lift is quantitatively sufficient); Gatto-Sartori-Tonin does not emerge
   (corr(log V_us, log sqrt(m_d/m_s)) = 0.11, median ratio 0.065); median (m_mu/m_tau)/(m_s/m_b) = 0.98; 82% of rows have
   a near-permutation CKM, 87% of the aligned rest have V_cb = 0 exactly, and of 222 rows with realistic quark masses
   (m_s/m_b, m_u/m_c, m_c/m_t within x3) none has a hierarchical CKM with all three angles nonzero.
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11915_su5_matrix_fluxes_on_t4 as F  # noqa: E402
import w33_pass11918_hypercharge_wilson_scan as S  # noqa: E402

OUT = ROOT / "data" / "w33_pass11918_tilt_ckm_and_up_lemma.json"
FROZEN = ROOT / "data" / "w33_pass11918_tilt_scan_frozen.json"


def support_is_involution(Y):
    A = abs(Y) > 1e-9 * abs(Y).max()
    return bool(A.sum() == 3 and (A.sum(0) == 1).all() and (A.sum(1) == 1).all() and (A == A.T).all() and np.trace(A) == 1)


def main():
    rng = np.random.default_rng(11918)
    saved = F.NS
    F.NS = np.array([(a, b) for a in range(-7, 8) for b in range(-7, 8)])
    forms = [[[a, b], [b, c]] for a in range(1, 5) for c in range(1, 5) for b in range(-3, 4) if a * c - b * b == 3]
    deg, lift, mono_common, mono_w = 0.0, 1.0, True, True
    for N in forms:
        Na = np.array(N, float)
        Om = 1j * (1.3 * np.eye(2) + 0.1 * Na) + 0.2 * np.eye(2)
        T = F.T4(Om, 10)
        z = rng.random(2) + Om @ rng.random(2)
        w = rng.random(2) - 0.5 + Om @ (rng.random(2) - 0.5)
        sw = np.linalg.solve(Na, w)
        for Y in F.yukawas(T, N, N, z, z):
            s = np.linalg.svd(Y, compute_uv=False)
            deg = max(deg, min(abs(s[0] - s[1]), abs(s[1] - s[2])) / s[0])
            mono_common &= support_is_involution(Y)
        for Y in F.yukawas(T, N, N, z + sw / 6, z - 2 * sw / 3):
            s = np.linalg.svd(Y, compute_uv=False)
            lift = min(lift, min(abs(s[0] - s[1]), abs(s[1] - s[2])) / s[0])
            A = abs(Y) > 1e-9 * abs(Y).max()
            mono_w &= bool((A.sum(0) == 1).all() and (A.sum(1) == 1).all())
    # lepton = down at relative Wilson line shifted by (5m/18) w
    lep = []
    for pair in ("114", "A2"):
        N10 = S.PAIRS[pair]
        N5 = np.round(3 * np.linalg.inv(N10)).astype(int).tolist()
        m = int(np.trace(N10))
        Om = 1j * (1.2 * np.eye(2) + 0.15 * np.array(N10, float)) + 0.1 * np.eye(2)
        T = F.T4(Om, 12)

        def lat(v):
            return v[:2] + Om @ v[2:]

        z10, z5, w = lat(rng.random(4)), lat(rng.random(4)), lat(rng.random(4) - 0.5)
        P = S.positions(N10, N5, z10, z5, w)
        hd1 = np.linalg.solve(m * np.eye(2), np.array(N10) @ P["Q"] + np.array(N5) @ P["d"])
        hd2 = np.linalg.solve(m * np.eye(2), np.array(N10) @ P["e"] + np.array(N5) @ P["L"])
        Se = sorted(tuple(np.round(np.linalg.svd(Y, compute_uv=False), 8)) for Y in F.yukawas(T, N10, N5, P["e"], P["L"]))
        Sd = sorted(tuple(np.round(np.linalg.svd(Y, compute_uv=False), 8))
                    for Y in F.yukawas(T, N10, N5, P["Q"], P["d"] - 5 * m / 18 * w))
        lep.append(dict(pair=pair, hd_position_diff=float(np.max(abs(hd1 - hd2))),
                        lepton_vs_shifted_down=float(np.max(abs(np.array(Se) - np.array(Sd))))))
    F.NS = saved
    fz = json.loads(FROZEN.read_text())
    rows = S.sample(fz["check_seed"], 1, "114")
    repro = float(np.max(abs(rows[:, 5:] - np.array(fz["check_rows"])[:, 5:])))
    res = dict(pass_id=11918, forms=len(forms), up_common_wilson_max_gap=deg, up_hypercharge_min_gap=lift,
               up_support_involution_common=mono_common, up_monomial_with_hypercharge=mono_w, lepton_down=lep,
               reproduced_rows_max_diff=repro, frozen={k: v for k, v in fz.items() if k != "check_rows"})
    res["checks"] = {k: bool(v) for k, v in dict(
        up_degenerate_pair_common_wilson=deg < 1e-12 and mono_common,
        up_monomial_with_hypercharge_wilson=mono_w,
        hypercharge_lifts_degeneracy=lift > 1e-4,
        hd_position_consistent=all(x["hd_position_diff"] < 1e-12 for x in lep),
        lepton_is_shifted_down=all(x["lepton_vs_shifted_down"] < 1e-7 for x in lep),
        tilt_reaches_realistic_md=fz["frac_md_ms_gt_001"] > 0.1,
        no_gst=abs(fz["gst_corr"]) < 0.3,
        no_georgi_jarlskog=0.8 < fz["median_mutau_over_sb"] < 1.25,
        no_realistic_mass_row_with_hierarchical_ckm=fz["realistic_mass_and_hier_nonzero_ckm"] == 0,
        frozen_scan_reproduces=repro < 1e-8,
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
