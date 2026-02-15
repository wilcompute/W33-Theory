#!/usr/bin/env python3
"""
Create a Zenodo deposition for a GitHub release (automates steps of the bash helper).
Usage:
  ZENODO_TOKEN=<token> GITHUB_TOKEN=<token> python scripts/manual_zenodo_deposit.py --tag v2026-02-15-qec-mlut
Notes:
  - Requires `requests` (pip install requests).
  - Uses environment variables ZENODO_TOKEN and optionally GITHUB_TOKEN.
  - Prints the published DOI on success.
"""
import argparse
import json
import os
import sys
from pathlib import Path

try:
    import requests
except Exception:
    print("Please install requests: pip install requests")
    raise

ZENODO_HOST = os.environ.get("ZENODO_HOST", "https://zenodo.org")
ZENODO_TOKEN = os.environ.get("ZENODO_TOKEN")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

if not ZENODO_TOKEN:
    print("ERROR: set ZENODO_TOKEN environment variable (https://zenodo.org/account/settings/applications)")
    sys.exit(2)

parser = argparse.ArgumentParser()
parser.add_argument("--repo", default="wilcompute/W33-Theory")
parser.add_argument("--tag", required=True)
parser.add_argument("--download-assets", action="store_true")
args = parser.parse_args()

repo = args.repo
tag = args.tag

headers = {"Authorization": f"Bearer {ZENODO_TOKEN}"}

session = requests.Session()
session.headers.update(headers)

print(f"Creating Zenodo deposition for {repo} {tag}...")
# 1) create deposit
dep_resp = session.post(f"{ZENODO_HOST}/api/deposit/depositions", json={})
dep_resp.raise_for_status()
dep = dep_resp.json()
dep_id = dep.get("id")
print("Draft created id=", dep_id)

# 2) download GitHub release assets (optional)
asset_paths = []
if args.download_assets:
    gh_headers = {"Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        gh_headers["Authorization"] = f"token {GITHUB_TOKEN}"
    rel = requests.get(f"https://api.github.com/repos/{repo}/releases/tags/{tag}", headers=gh_headers)
    rel.raise_for_status()
    rj = rel.json()
    for a in rj.get("assets", []):
        url = a.get("browser_download_url")
        fname = Path(url).name
        print("Downloading", url)
        with requests.get(url, headers=gh_headers, stream=True) as r:
            r.raise_for_status()
            with open(fname, "wb") as fh:
                for chunk in r.iter_content(32768):
                    fh.write(chunk)
        asset_paths.append(fname)

# 3) upload files to deposition
if asset_paths:
    for p in asset_paths:
        print("Uploading", p)
        files = {"file": open(p, "rb")}
        up = session.post(f"{ZENODO_HOST}/api/deposit/depositions/{dep_id}/files", files=files)
        up.raise_for_status()

# 4) set metadata
metadata = {
    "metadata": {
        "title": "Pillar-45 — GF(3) QEC primitives + MLUT (v2026-02-15-qec-mlut)",
        "upload_type": "software",
        "publication_date": "2026-02-15",
        "creators": [{"name": "Wilj D."}],
        "description": f"Pillar-45 release (GitHub): https://github.com/{repo}/releases/tag/{tag}",
        "version": tag,
        "license": "MIT",
        "related_identifiers": [
            {"identifier": f"https://github.com/{repo}/releases/tag/{tag}", "relation": "isSupplementTo", "scheme": "url"}
        ]
    }
}
print("Setting metadata...")
setm = session.put(f"{ZENODO_HOST}/api/deposit/depositions/{dep_id}", json=metadata)
setm.raise_for_status()

# 5) publish
print("Publishing deposition...")
pub = session.post(f"{ZENODO_HOST}/api/deposit/depositions/{dep_id}/actions/publish")
pub.raise_for_status()
pr = pub.json()
doi = pr.get("doi") or pr.get("metadata", {}).get("doi")
if doi:
    print("Published — DOI:", doi)
    print("DOI URL:", f"https://doi.org/{doi}")
else:
    print("Publish response:\n", json.dumps(pr, indent=2))
    sys.exit(1)
