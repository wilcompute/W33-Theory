#!/usr/bin/env python3
"""Official DES Y6 data-product discovery and frozen S9 readiness gate.

Discover HTML links from official DES hosts, query public DES PPD GitHub
tree, and inspect binary magic only for directly supplied authoritative
FITS candidates. Refuse to score frozen S9 absent complete real unblinded
xi+/xi- vector, matched covariance/n(z), corrected scalar-field CLASS
theory and nuisance refit. Never turn published S8 into a likelihood.
"""
import json,hashlib,sys,urllib.parse,html.parser
from pathlib import Path
import requests
from w33_20261109_s9_frozen_likelihood_harness import FROZEN
ROOT=Path(__file__).resolve().parents[1]
class Links(html.parser.HTMLParser):
    def __init__(self):super().__init__();self.urls=[]
    def handle_starttag(self,tag,attrs):
        if tag.lower()=="a":
            u=dict(attrs).get("href")
            if u:self.urls.append(u)

def request(url,binary=False):
    try:
        with requests.get(url,stream=True,timeout=18,allow_redirects=True,
                          headers={"User-Agent":"W33-frozen-S9-2026-11-09"}) as r:
            result={"status_code":int(r.status_code),
                    "final_url":r.url,
                    "content_type":r.headers.get("Content-Type",""),
                    "content_length_header":r.headers.get("Content-Length"),
                    "fully_downloaded":False}
            if binary and r.status_code==200:
                # inspect ONLY the FITS first card; 200 HTML is not the data.
                chunk=next(r.iter_content(2880),b"")
                result["first_binary_card_sha256"]=hashlib.sha256(chunk).hexdigest()
                result["FITS_magic_at_first_card"]=chunk.startswith(b"SIMPLE  =")
                result["first_bytes_len"]=len(chunk)
            elif not binary and r.status_code==200:
                size=0; chunks=[]
                for chunk in r.iter_content(65536):
                    size+=len(chunk)
                    if size>2000000:break
                    chunks.append(chunk)
                data=b"".join(chunks)
                result["html_bytes_inspected"]=len(data)
                result["text_is_html"]=bool(data.strip().startswith(b"<!") or b"<html" in data.lower())
                if result["text_is_html"]:
                    link=Links()
                    link.feed(data.decode("utf8","replace"))
                    result["links"]=sorted(set(urllib.parse.urljoin(r.url,x) for x in link.urls))
            return result
    except requests.RequestException as e:
        return {"status_code":None,"error":str(e)[:160],
                "fully_downloaded":False}

def main(path=None):
    official=["https://des.ncsa.illinois.edu/releases/y6a2",
              "https://www.darkenergysurvey.org/des-y6-cosmology-results-papers/"]
    p={u:request(u) for u in official}
    # Search only URLs genuinely hyperlinked from the official pages.
    discovered=[]
    for site,record in p.items():
        for u in record.get("links",[]):
            low=u.lower()
            if any(x in low for x in (".fits",".fit",".h5","3x2pt","cosmic-shear","covariance")):
                discovered.append(u)
    discovered=sorted(set(discovered))
    # Explicit historically indexed unblinded candidate, verified 404.
    historic="https://desdr-server.ncsa.illinois.edu/despublic/y6a2_files/y6key_products/final_version/3x2pt_2025-07-28-20h_UNBLINDED_wmask_nob2.fits"
    candidates=[historic]+[u for u in discovered if
                           (u.lower().endswith(".fits") or ".fits?" in u.lower()) and
                           urllib.parse.urlparse(u).hostname in
                           ("des.ncsa.illinois.edu","desdr-server.ncsa.illinois.edu")]
    inspected={u:request(u,binary=True) for u in dict.fromkeys(candidates)}
    # Public published PPD method code is not a Y6 likelihood dataset.
    ppd=request("https://api.github.com/repos/des-science/y6-ppd-public/contents")
    y6three=request("https://api.github.com/repos/des-science/y6-3x2pt")
    valid=[u for u,v in inspected.items() if v.get("FITS_magic_at_first_card",False)]
    # Still cannot claim provenance, complete checksum, covariance and
    # physics even if a FITS first card is recovered.
    S9=False
    assert not S9
    out={"status":"PASS_DES_Y6_OFFICIAL_LINK_PROVENANCE_AUDIT_S9_UNSCORED",
         "S9_frozen":"2026-11-08",
         "S9_claim_sha256":hashlib.sha256(FROZEN["claim"].encode()).hexdigest(),
         "official_pages":{
           k:{kk:vv for kk,vv in v.items() if kk!="links"} for k,v in p.items()},
         "official_relevant_links":discovered[:60],
         "official_relevant_link_total":len(discovered),
         "tested_FITS_candidate_first_cards":inspected,
         "real_FITS_magic_found_unverified":valid,
         "PPD_public_GitHub_repo_root_status":ppd.get("status_code"),
         "DES_Y6_3x2pt_GitHub_repo_public_status":y6three.get("status_code"),
         "official_unblinded_validated_full_file_download":False,
         "complete_covariance_nz_model_refits_verified":False,
         "frozen_S9_scored":False,
         "safety_rule":"HTTP 200 HTML, a cached FITS path, README explaining measurement formats, published S8, and a first FITS magic card are NOT full provenance. The real-data S9 can run only after official raw bytes, hash, matching covariance, n(z), exact prereg cuts and CLASS/Halofit model-specific nuisance refits.",
         "scope":"Live read-only HTTPS provenance audit; online availability is time-sensitive. This is neither an observed cosmological test nor a proof that no public Y6 vector exists elsewhere."}
    if path:Path(path).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("DES_Y6_AUDIT",json.dumps({"site_http":{k:v.get("status_code") for k,v in p.items()},
       "historic_FITS":inspected[historic].get("status_code"),
       "linked_relevant":len(discovered),
       "found_FITS_magic":len(valid),
       "ppd_GitHub_http":ppd.get("status_code"),
       "y6_3x2_GitHub_http":y6three.get("status_code"),
       "S9_scored":False}))
    return out
if __name__=="__main__":main(sys.argv[1] if len(sys.argv)>1 else None)
