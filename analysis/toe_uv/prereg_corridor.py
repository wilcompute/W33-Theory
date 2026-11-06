"""Item 3: frozen statement S5 (2026-11-06), separate from prereg_statements.json (sha d2624061), which stays untouched.
usage: py -3 prereg_corridor.py"""
import hashlib
import json

S = dict(
    written="2026-11-06",
    S5_corridor=dict(
        claim="If the fading coupling (b ~ 0.05) is carried by a decay-produced sterile neutrino, its mass lies in 16-20 keV (Lyman-alpha edge 15.2-17.4 keV by mean or rms free-streaming match; clock cap above), with a heavy singlet m_S ~ 3-10 TeV, Higgs portal ~1e-6 and vev 1-3 TeV.  A decay line, if visible, sits at 8-10 keV and its rest-frame centroid drifts with source redshift by -0.7 to -0.9 percent (c < 0) or +0.75 to +0.94 percent (c > 0) at z = 0.5.",
        scored_by="X-ray line searches at 8-10 keV (XRISM, NuSTAR, Athena) and Lyman-alpha/half-mode WDM bounds",
        falsified_if="a robust thermal-equivalent WDM bound above about 7 keV (which pushes the edge past 20 keV and closes the corridor), or a detected 8-10 keV dark-matter line whose centroid shows no redshift drift at the stated level",
        not_falsified_by="the absence of a line: the mixing angle is free in this production mode",
    ),
)
js = json.dumps(S, indent=1, sort_keys=True)
open("prereg_corridor.json", "w", newline="\n").write(js)
h = hashlib.sha256(js.encode()).hexdigest()
open("prereg_corridor.sha256", "w", newline="\n").write(h + "  prereg_corridor.json\n")
print("sha256", h)
