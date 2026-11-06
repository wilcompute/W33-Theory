"""Item 1: frozen falsifiable statements (2026-11-06), written before the joint CPL+DES refit, the shear-held posterior predictive (Pass 12627) and any future data.  Hashed.
Each statement names the data that score it and the outcome that falsifies it.
usage: py -3 prereg_statements.py"""
import hashlib
import json

S = dict(
    written="2026-11-06",
    S1_shear=dict(claim="Fading (c<0 mode, Dovekie full-data fit) predicts cosmic shear better than CPL: Delta chi2_shear(CPL - fading) > 0 at fixed full-data backgrounds with the class_des_fit.py pipeline (nuisances refitted).", scored_by="the next public cosmic-shear 2pt release with covariance (DES Y6 or KiDS-Legacy), analysed with the same pipeline and cuts 10'/60'", falsified_if="Delta chi2_shear(CPL - fading) <= 0", current_DES_Y3_value=2.99),
    S2_phantom_iff_cneg=dict(claim="Within the fading model, w_eff (uncoupled-CDM convention) crosses -1 iff c < 0, near z = 0.8; the c > 0 mode never goes phantom.", scored_by="DESI DR3 (or later) non-parametric w(z) reconstructions combined with CMB + SN", falsified_if="a fading fit to the new data with c < 0 and no crossing, or c > 0 with a crossing"),
    S3_line_drift=dict(claim="If a dark-matter decay line is detected in clusters, and the decaying particle carries the fading coupling, its rest-frame energy at z ~ 0.5 is offset from local sources by -0.7 to -0.9 percent for c < 0 and +0.75 to +0.94 percent for c > 0.", scored_by="XRISM / Athena line centroids versus redshift", falsified_if="a detected line with offset inconsistent with both signs at the stated amplitude (conditional on the coupling acting on the particle)"),
    S4_dr3_bao=dict(claim="DESI DR3 BAO alone will not separate fading from CPL by more than Delta chi2 = 4 (Asimov upper bound 3.3-3.9) and will not determine the sign of c (0.2-0.3).", scored_by="DESI DR3 BAO compared with the frozen dr3_prereg.json (sha 6d76b63b)", falsified_if="Delta chi2(CPL vs fading) > 6 from DR3 BAO alone at the frozen fits"),
)
js = json.dumps(S, indent=1, sort_keys=True)
open("prereg_statements.json", "w", newline="\n").write(js)
h = hashlib.sha256(js.encode()).hexdigest()
open("prereg_statements.sha256", "w", newline="\n").write(h + "  prereg_statements.json\n")
print("sha256", h)
