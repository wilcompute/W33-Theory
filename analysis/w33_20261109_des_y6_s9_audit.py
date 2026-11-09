#!/usr/bin/env python3
"""Fail-closed DES Y6 S9 held-out likelihood data-acquisition audit.

Do not calculate S9 from a published LambdaCDM S8 marginal or a stale
web search index. Only a verified unblinded xi+/xi- data-vector, matching
covariance/n(z)/nuisances and corrected CLASS predictions can score S9.
"""
import importlib.util,json,sys
from pathlib import Path
from urllib.parse import urlparse
import requests

ROOT=Path(__file__).resolve().parents[1]
URLS={
 "official_release":"https://des.ncsa.illinois.edu/releases/y6a2/",
 "former_public_directory":"https://desdr-server.ncsa.illinois.edu/despublic/y6a2_files/y6key_products/final_version/",
 "former_unblinded_3x2pt_FITS":"https://desdr-server.ncsa.illinois.edu/despublic/y6a2_files/y6key_products/final_version/3x2pt_2025-07-28-20h_UNBLINDED_wmask_nob2.fits",
 "former_public_pipeline_notebook":"https://desdr-server.ncsa.illinois.edu/despublic/y6a2_files/y6key_products/final_version/3x2pt_pipeline_public.ipynb",
 "DES_Y6_public_papers":"https://www.darkenergysurvey.org/des-y6-cosmology-results-papers/",
 "DES_Y6_public_PPD_code":"https://github.com/des-science/y6-ppd-public"
}
def main(path=None):
    prereg=json.loads((ROOT/"analysis/toe_uv/prereg_noshear.json").read_text())["S9_shear_no_split"]
    assert prereg["frozen"]=="2026-11-08"
    statuses={}
    for key,url in URLS.items():
        try:
            # stream=True prevents accidental transfer of a multi-GiB catalog.
            with requests.get(url,stream=True,timeout=20,allow_redirects=True) as r:
                statuses[key]={"HTTP_GET_status":int(r.status_code),
                    "Content_Type":r.headers.get("Content-Type",""),
                    "Content_Length_header":r.headers.get("Content-Length",""),
                    "final_host":urlparse(r.url).hostname,
                    "actual_data_bytes_downloaded":0,
                    "verified_complete_FITS":False}
        except Exception as exc:
            statuses[key]={"HTTP_GET_status":None,"error":type(exc).__name__+": "+str(exc)[:170],
                           "verified_complete_FITS":False}
    known={k:bool(importlib.util.find_spec(k)) for k in ("classy","cosmosis","pyccl","astropy")}
    result={
        "status":"S9_UNSCORED_PUBLIC_Y6_DV_NOT_DOWNLOADED",
        "record_date":"2026-11-09",
        "frozen_S9_date":prereg["frozen"],
        "release_endpoint_test":statuses,
        "python_theory_tools_available":known,
        "exact_prereg":prereg,
        "S9_chi2_computed":False,
        "why":"No validated complete unblinded DES Y6 xi+/- FITS vector plus matching covariance and corrected CLASS/Halofit scalar-field predictions/nuisance re-optimization in this run.",
        "alternative_public_inputs":"DES Y6 publishes LambdaCDM S8=0.789 +/-0.012 and a public PPD code repository; neither by itself provides the model-specific frozen S9 likelihood.",
        "required_pipeline_artifacts":[
          "actual unblinded xi+/- vector with correct bin and scale metadata",
          "matched full covariance, and exact scale-cut indices",
          "source redshift n(z) and calibration covariance",
          "intrinsic alignment and other systematics nuisance priors",
          "patched CLASS/Halofit for CPL and fading c<0 cosmologies",
          "same-data nuisance refits for each model",
          "frozen absolute Delta_chi2 score and LCDM-envelope checks"],
        "scientific_disposition":"Fail closed. No claim of S9 success or failure, no fake sigma from LambdaCDM-only S8 marginal.",
        "source_prior_art":[
          "https://www.darkenergysurvey.org/des-y6-cosmology-results-papers/",
          "https://github.com/des-science/y6-ppd-public/"
        ]
    }
    assert not result["S9_chi2_computed"]
    if path:Path(path).write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("DES Y6 S9:",result["status"],{k:v.get("HTTP_GET_status") for k,v in statuses.items()})
    return result
if __name__=="__main__":
    main(sys.argv[1] if len(sys.argv)>1 else None)
