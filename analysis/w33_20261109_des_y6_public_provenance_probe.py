#!/usr/bin/env python3
"""DES Y6 public full-shear vector provenance: explicit active acquisition gate.
Never treat an HTTP 200 HTML release shell, GitHub analysis code or
published S8 posterior as the required FITS vector+covariance.
"""
import json,sys,re,hashlib
from pathlib import Path
from urllib.parse import urljoin,urlparse
import requests

URLS={
 "DES_Y6_release":"https://des.ncsa.illinois.edu/releases/y6a2/",
 "DES_Y6_papers":"https://www.darkenergysurvey.org/des-y6-cosmology-results-papers/",
 "DES_Y6_old_3x2_directory":"https://desdr-server.ncsa.illinois.edu/despublic/y6a2_files/y6key_products/final_version/",
 "DES_Y6_old_unblinded_FITS":"https://desdr-server.ncsa.illinois.edu/despublic/y6a2_files/y6key_products/final_version/3x2pt_2025-07-28-20h_UNBLINDED_wmask_nob2.fits",
 "DES_Y6_old_pipeline_notebook":"https://desdr-server.ncsa.illinois.edu/despublic/y6a2_files/y6key_products/final_version/3x2pt_pipeline_public.ipynb",
 "DES_Y6_public_PPD_repo":"https://github.com/des-science/y6-ppd-public",
 "DES_Y6_3x2_analysis_arxiv":"https://arxiv.org/abs/2601.14559"
}
def fetch(url):
    try:
        with requests.get(url,timeout=24,stream=True,
                          allow_redirects=True,
                          headers={"User-Agent":"W33-Research-Verification/2026"}) as r:
            resp={"HTTP_status":r.status_code,
                  "final_url":r.url,
                  "content_type":r.headers.get("Content-Type",""),
                  "Content_Length_header":r.headers.get("Content-Length",""),
                  "is_actual_verified_data_vector":False}
            typ=resp["content_type"].lower()
            if r.status_code==200 and ("text/html" in typ or urlparse(r.url).path.endswith(".html")):
                raw=b""
                for chunk in r.iter_content(8192):
                    raw+=chunk
                    if len(raw)>=150000:break
                text=raw.decode("utf8",errors="replace")
                resp["HTML_bytes_inspected"]=len(raw)
                resp["HTML_SHA256_prefix"]=hashlib.sha256(raw).hexdigest()[:16]
                matches=sorted(set(re.findall(
                    r'["\x27]([^"\x27]{1,180}(?:\.fits(?:\.gz)?|\.zip|\.dat|\.csv|\.js))["\x27]',text,re.I)))
                resp["FITS_or_script_href_candidates"]=matches[:30]
                resp["is_Polymer_or_JS_shell"]=bool(re.search(r'polymer|<script|angular|javascript',text,re.I))
                resp["contains_unblinded_FITS_filename"]=bool("3x2pt_2025-07-28-20h_UNBLINDED" in text)
            return resp
    except Exception as ex:
        return {"HTTP_status":None,"error_type":type(ex).__name__,
                "message":str(ex)[:180],"is_actual_verified_data_vector":False}
def main(path=None):
    results={k:fetch(u) for k,u in URLS.items()}
    fit=results["DES_Y6_old_unblinded_FITS"]
    assert not fit["is_actual_verified_data_vector"]
    original=json.loads((Path(__file__).resolve().parents[1]/
                         "analysis/toe_uv/prereg_noshear.json").read_text())["S9_shear_no_split"]
    assert original["frozen"]=="2026-11-08"
    output={
     "status":"S9_UNSCORED_DV_COV_PROVENANCE_GATED",
     "record_date":"2026-11-09",
     "public_endpoint_checks":results,
     "original_preregistration_date":"2026-11-08",
     "actual_unblinded_cosmic_shear_FITS_downloaded_and_parsed":False,
     "matched_full_covariance_downloaded_and_validated":False,
     "patched_CLASS_Halofit_predictions_completed":False,
     "same_data_nuisance_refits_completed":False,
     "S9_model_likelihood_scored":False,
     "public_provenance_notes":"The Dark Energy Survey Y6 paper page links releases/y6a2/ and says some Y6 cosmology products released, more coming. The Y6 public PPD README explicitly requires a 2pt FITS for data-vector element order and scale-cut files; the public software repo is not itself that FITS.",
     "S8_misuse_warning":"S8=0.789 +/- 0.012 is a DES 3x2 LambdaCDM conditional posterior and CANNOT be used as the frozen S9 alternate-model full-covariance chi-squared.",
     "next_data_requirements":["verified official unblinded FITS plus SHA256 and provenance",
          "precise xi-plus/minus angular tomographic bin/row mapping",
          "matched covariance and source n(z) distributions",
          "nuisance priors and scale-cut masks in same DES pipeline version",
          "model-specific CLASS/Halofit predictions with original frozen parameter priors",
          "reoptimized nuisance and held-out likelihood control for all frozen S9 model alternatives"]}
    if path:Path(path).write_text(json.dumps(output,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("DES Y6 public audit",json.dumps({k:v["HTTP_status"] for k,v in results.items()}),"S9_SCORING=False")
    return output
if __name__=="__main__":
    main(sys.argv[1] if len(sys.argv)>1 else None)
