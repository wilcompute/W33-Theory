#!/usr/bin/env python3
"""Strictly frozen S9 DES likelihood evidence gate and public archive audit.

Tests the distinction between accessible Y6 paper/catalog, legitimate 3x2pt
unblinded correlation + covariance + z distributions, and corrected CLASS
fading-coupling model fits. No real cosmology score without full evidence.
"""
import json,sys,hashlib,re,urllib.parse
from pathlib import Path
import requests
from w33_20261109_des_y6_official_link_audit import request
ROOT=Path(__file__).resolve().parents[1]
FROZEN=ROOT/"analysis/toe_uv/prereg_noshear.json"
OLD=ROOT/"data/w33_20261109_des_y6_repeat_public_audit.json"

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def validate(packet,claim_hash):
    fails=[]
    froze=json.loads(FROZEN.read_text(encoding="utf8"))["S9_shear_no_split"]
    if froze["frozen"]!="2026-11-08":fails.append("S9 freeze date modified")
    if hashlib.sha256(froze["claim"].encode()).hexdigest()!=claim_hash:
        fails.append("S9 frozen claim modified")
    if packet.get("source_kind")!="full_DES_Y6_xi_pm_not_posterior_summary":
        fails.append("not full xi+ xi- survey correlation vector")
    url=packet.get("official_data_url","")
    if not url.startswith("https://desdr-server.ncsa.illinois.edu/despublic/") and not url.startswith("https://des.ncsa.illinois.edu/"):
        fails.append("file URL outside official DES data hosts")
    if not packet.get("publisher_independent_hash_verified",False):
        fails.append("no independently authenticated publisher digest")
    h=packet.get("publisher_sha256","")
    if not re.fullmatch("[0-9a-f]{64}",h):
        fails.append("missing publisher full SHA256")
    p=packet.get("local_full_fits_path")
    if not isinstance(p,str) or not Path(p).is_file():
        fails.append("full downloaded FITS absent")
    else:
        b=Path(p).read_bytes()
        if not b.startswith(b"SIMPLE  ="):fails.append("not FITS binary")
        if sha(p)!=h:fails.append("download digest not the publisher digest")
    for field in ("matched_covariance_nz","corrected_CLASS_Halofit_scf_model",
                  "NLA_no_baryons","full_nuisance_profiled_each_model"):
        if packet.get(field) is not True:fails.append("missing "+field)
    if packet.get("xi_plus_cut_arcmin")!=10 or packet.get("xi_minus_cut_arcmin")!=60 or packet.get("cuts_are_strict_gt") is not True:
        fails.append("angular scale cuts differ from freeze")
    if packet.get("models_scored")!=["LCDM","CPL","fading_c_negative","fading_c_positive"]:
        fails.append("frozen competing theory model set mismatch")
    ids=packet.get("data_vector_labels",[])
    if not ids or len(ids)!=len(set(ids)) or ids!=packet.get("covariance_labels") or ids!=packet.get("theory_labels"):
        fails.append("data/covariance/model vector index mismatch")
    return fails

def main(path=None):
    previous=json.loads(OLD.read_text(encoding="utf8"))
    expected=previous["S9_claim_sha256"]
    frozen=json.loads(FROZEN.read_text(encoding="utf8"))["S9_shear_no_split"]
    assert hashlib.sha256(frozen["claim"].encode()).hexdigest()==expected
    # No real unblinded matched FITS / covariance was found in past
    # searches. Query two actual NCSA archive listings, never invent files.
    sites=["https://desdr-server.ncsa.illinois.edu/despublic/y6a2_files/",
           "https://desdr-server.ncsa.illinois.edu/despublic/y6a2_files/y6key_products/",
           "https://des.ncsa.illinois.edu/releases/y6a2"]
    live={u:request(u) for u in sites}
    # An authenticated independent publisher digest cannot be inferred
    # merely from HTTP 200/HTML or FITS first header. We do not score.
    cases={
       "empty_manifest":{},
       "publisher_web_paper_masquerade":{"source_kind":"published_S8_posterior","official_data_url":"https://www.darkenergysurvey.org/des-y6-cosmology-results-papers/"},
       "fabricated_fits_header_only":{"source_kind":"full_DES_Y6_xi_pm_not_posterior_summary",
          "official_data_url":sites[0]+"test.fits","publisher_sha256":"0"*64,
          "publisher_independent_hash_verified":False},
       "wrong_scales_and_model_list":{"xi_plus_cut_arcmin":10,"xi_minus_cut_arcmin":10,
          "cuts_are_strict_gt":False,"models_scored":["LCDM","CPL"]},
       "unverifiable_local_path":{"local_full_fits_path":"C:\\\\not-an-actual-verified-survey-file.fits",
          "publisher_sha256":"a"*64}}
    rejected={n:validate(v,expected) for n,v in cases.items()}
    assert all(len(z)>0 for z in rejected.values())
    out={"status":"PASS_S9_STRICT_FROZEN_SOURCE_SHA256_AND_FIVE_FAIL_CLOSED_ATTACKS",
         "frozen_date":frozen["frozen"],
         "frozen_claim_sha256":expected,
         "public_archive_probe":{k:{x:y for x,y in value.items() if x!="links"} for k,value in live.items()},
         "public_archive_html_direct_links":{
            k:[x for x in value.get("links",[]) if x.lower().endswith((".fits",".fit",".sacc",".h5"))][:15]
            for k,value in live.items()},
         "prereg_directives":{
            "strict_xi_plus_gt_arcmin":10,"strict_xi_minus_gt_arcmin":60,
            "models":["LCDM","CPL","fading_c_negative","fading_c_positive"],
            "nonlinear":"CLASS Halofit scalar field patch required",
            "intrinsic_alignment":"NLA no baryons; refit every model's nuisance parameters"},
         "deliberately_invalid_evidence_manifests_rejected":rejected,
         "independent_publisher_SHA256_and_full_FITS":False,
         "corrected_four_model_nuisance_fits_executed_on_DES_Y6":False,
         "real_S9_Delta_chi2_scored":False,
         "scope":"The provenance gate deliberately refuses to infer data availability from HTTP 200, a printed published S8 posterior, or a first FITS card. This is a security/identifiability unit test, not a new cosmology result. Even an all-true user-supplied manifest would not prove an independent publisher digest; authenticated release metadata and real bytes must be established outside it. No official model comparison was computed."}
    if path:Path(path).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("S9_RESCAN",json.dumps({"statuses":{k:v.get("status_code") for k,v in live.items()},
       "attack_rejections":len(rejected),"actual_scored":False}))
    return out
if __name__=="__main__":main(sys.argv[1] if len(sys.argv)>1 else None)
