"""Trinification axion (Pass 12616): E/N = 8/3 (the DFSZ coupling), N_DW = 1, f >= 7e12 GeV from sigma stability with 27 colour components, pre-inflation misalignment.
theta needed for the full dark matter: Omega h^2 = 0.12 (f_a/9e11)^(7/6) theta^2, anharmonic corrections ignored (they matter only near theta ~ pi).
DMRadio-m3 (arXiv:2204.13781): designed for 20-800 neV, DFSZ sensitivity above about 120 neV in a 5-year scan (projection, as summarised by the search tool; not re-read).
Isocurvature: pre-inflation axions need H_I below roughly 1e-5 theta f (order of magnitude, from memory), reported as a bound on H_I.
usage: py -3 trin_window.py"""
import json, math
rows = []
for ma in (0.8, 0.5, 0.3, 0.2, 0.12, 0.05, 0.02, 0.006):
    fa = 5.70e12 / ma
    th = math.sqrt(0.12 / (0.12 * (fa / 9e11) ** (7 / 6)))
    rows.append(dict(m_a_ueV=ma, f_a=fa, theta=th, DMRadio_m3_DFSZ=ma >= 0.12, H_I_max_GeV=1e-5 * th * fa))
    print("m_a %.3f ueV f_a %.2g theta %.3f DMRadio-m3 DFSZ %s H_I < %.1g" % (ma, fa, th, ma >= 0.12, 1e-5 * th * fa))
json.dump(rows, open("trin_window.json", "w"), indent=1)
