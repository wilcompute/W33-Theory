#!/usr/bin/env python3
"""DES Y6 S9 official-product GET audit. Fail closed until FITS + covariance +
matched CLASS/Halofit/nuisance model artifacts verified in full.

HTTP 200 on a JavaScript application shell or a stale web search index does
not prove that a real DES xi+/- likelihood data vector is downloadable.
"""
import json,sys
from pathlib import Path
from urllib.parse import urlparse
import requests

ROOT=Path(__file__).resolve().parents[1]
frozen=json.loads((ROOT/"analysis/toe_uv/prereg_noshear.json").read_text(encoding="utf8"))
assert frozen["S9_shear_no_split"]["frozen"]=="2026-11-08"

urls={
 "official_DES_Y6_data_release_app":"https://des.ncsa.illinois.edu/releases/y6a2/",
 "official_DES_Y6_paper_index":"https://www.darkenergysurvey.org/des-y6-cosmology-results-papers/",
 "formerly_indexed_NCSA_directory":"https://desdr-server.ncsa.illinois.edu/despublic/y6a2_files/y6key_products/final_version/",
 "formerly_indexed_unblinded_3x2pt_FITS":"https://desdr-server.ncsa.illinois.edu/despublic/y6a2_files/y6key_products/final_version/3x2pt_2025-07-28-20h_UNBLINDED_wmask_nob2.fits",
 "formerly_indexed_redshift_distribution_H5":"https://desdr-server.ncsa.illinois.edu/despublic/y6a2_files/y6key_products/final_version/desy6_source_redshift.h5",
 "formerly_indexed_pipeline_notebook":"https://desdr-server.ncsa.illinois.edu/despublic/y6a2_files/y6key_products/final_version/3x2pt_pipeline_public.ipynb",
}
def probe(url):
    try:
        with requests.get(url,stream=True,timeout=15,allow_redirects=True,
                          headers={"User-Agent":"W33-Theory-Research-Data-Readiness/2026-11-09"}) as r:
            status=int(r.status_code)
            typ=r.headers.get("Content-Type","")
            n=r.headers.get("Content-Length")
            # A requested 22 MB FITS still requires an entire file and
            # checksum; opening a 200 HTTP stream is never scored as data.
            return {"status_code":status,"content_type":typ,
                    "reported_content_length":n,"final_host":urlparse(r.url).hostname,
                    "complete_bytes_downloaded":0,"full_checksum_verified":False}
    except requests.RequestException as exc:
        return {"status_code":None,"error":type(exc).__name__+": "+str(exc)[:220],
                "complete_bytes_downloaded":0,"full_checksum_verified":False}
def main(path=None):
    records={k:probe(v) for k,v in urls.items()}
    # Only a valid local FITS with matching covariance, n(z), blinded
    # treatment, and corrected model predictions can unlock S9.
    s9=False
    assert not s9
    d={
      "status":"S9_FAIL_CLOSED_NO_VALIDATED_Y6_LIKELIHOOD_VECTOR",
      "audit_date":"2026-11-09",
      "frozen_preregistration":"2026-11-08",
      "remote_endpoints":records,
      "previously_indexed_FITS_size": "22 MB according to cached NCSA search index, not current verified object",
      "DES_papers_confirm_some_cosmology_products_available":True,
      "genuine_DES_cosmic_shear_data_vector_acquired":False,
      "genuine_matching_full_covariance_acquired":False,
      "corrected_SCALAR_CLASS_Halofit_predictions_refit":False,
      "source_nz_priors_and_cuts_matched":False,
      "S9_chi_squared_scored":False,
      "frozen_procedure_preserved":True,
      "blocked_inference":"The published DES Y6 LambdaCDM/wCDM posterior and summary S8 cannot substitute for held-out exact likelihood vectors under the frozen S9 model. A URL index, response 200 HTML, or unverified FITS listing is not a data product.",
      "next_acquisition_gate":"Obtain official actual unblinded xi+/- 2pt FITS with checksum, complete covariance, redshift bins/scale cuts, nuisance priors, patched scalar-field CLASS/Halofit, and run independent model-specific nuisance refits.",
      "sources":[
        "https://www.darkenergysurvey.org/des-y6-cosmology-results-papers/",
        "https://des.ncsa.illinois.edu/releases/y6a2/",
        "https://github.com/des-science/y6-ppd-public"
      ]}
    if path:Path(path).write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("DES Y6 official GET gate",json.dumps({
        "status":d["status"],
        "endpoints":{k:v["status_code"] for k,v in records.items()},
        "S9_scored":False}))
    return d
if __name__=="__main__":
    main(sys.argv[1] if len(sys.argv)>1 else None)
