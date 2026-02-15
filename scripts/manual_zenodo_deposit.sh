#!/usr/bin/env bash
# Manual Zenodo deposition helper (production).
# Usage:
#   ZENODO_TOKEN=<your-token> ./scripts/manual_zenodo_deposit.sh --tag v2026-02-15-qec-mlut
# Optional:
#   Set GITHUB_TOKEN to download private release assets.
# Notes:
#   - Requires curl and Python (for small JSON parsing helper).
#   - This creates a *published* Zenodo record and returns the DOI.
#   - For testing use SANDBOX by setting ZENODO_HOST=https://sandbox.zenodo.org

set -euo pipefail
ZENODO_HOST=${ZENODO_HOST:-https://zenodo.org}
ZENODO_TOKEN=${ZENODO_TOKEN:-}
REPO=${REPO:-wilcompute/W33-Theory}
TAG=${TAG:-v2026-02-15-qec-mlut}
GITHUB_TOKEN=${GITHUB_TOKEN:-}

usage(){
  echo "Usage: ZENODO_TOKEN=<token> $0 --tag <tag> [--repo owner/repo]"
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --tag) TAG="$2"; shift 2;;
    --repo) REPO="$2"; shift 2;;
    --help) usage;;
    *) echo "Unknown arg: $1"; usage;;
  esac
done

if [ -z "$ZENODO_TOKEN" ]; then
  echo "ERROR: set ZENODO_TOKEN environment variable (see https://zenodo.org/account/settings/applications)"
  exit 2
fi

echo "Creating Zenodo deposition for ${REPO} ${TAG} (host=${ZENODO_HOST})"

# 1) create draft deposition
resp=$(curl -s -X POST "${ZENODO_HOST}/api/deposit/depositions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${ZENODO_TOKEN}" \
  -d '{}')
deposit_id=$(python - <<PY
import sys,json
r=json.load(sys.stdin)
print(r.get('id',''))
PY
<<<"$resp")
if [ -z "$deposit_id" ]; then
  echo "Failed to create deposition. Response:\n$resp"
  exit 3
fi
echo "Draft deposition id=$deposit_id"

# 2) optionally download release assets from GitHub (recommended)
release_json=$(curl -s -H "Accept: application/vnd.github+json" ${GITHUB_TOKEN:+-H "Authorization: token $GITHUB_TOKEN"} "https://api.github.com/repos/${REPO}/releases/tags/${TAG}")
# parse assets (browser_download_url)
assets=$(python - <<PY
import sys,json
r=json.load(sys.stdin)
for a in r.get('assets',[]):
    print(a.get('browser_download_url'))
PY
<<<"$release_json")

tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"' EXIT
fcount=0
for url in $assets; do
  fname="$tmpdir/$(basename $url)"
  echo "Downloading asset: $url -> $fname"
  curl -L ${GITHUB_TOKEN:+-H "Authorization: token $GITHUB_TOKEN"} -o "$fname" "$url"
  fcount=$((fcount+1))
done

# 3) upload downloaded files to Zenodo draft
if [ $fcount -gt 0 ]; then
  for f in "$tmpdir"/*; do
    echo "Uploading $f to Zenodo..."
    curl -s -X POST "${ZENODO_HOST}/api/deposit/depositions/${deposit_id}/files" \
      -H "Authorization: Bearer ${ZENODO_TOKEN}" \
      -F "file=@${f}" || { echo "file upload failed"; exit 4; }
  done
else
  echo "No assets found on the GitHub release (continuing with metadata-only deposition)."
fi

# 4) set metadata (title/description/version/related identifier -> GitHub release URL)
metadata=$(cat <<MET
{
  "metadata": {
    "title": "Pillar-45 — GF(3) QEC primitives + MLUT (v2026-02-15-qec-mlut)",
    "upload_type": "software",
    "publication_date": "2026-02-15",
    "creators": [{"name": "Wilj D."}],
    "description": "Pillar-45: GF(3) qutrit QEC primitives + MLUT decoder. GitHub release: https://github.com/${REPO}/releases/tag/${TAG}",
    "version": "${TAG}",
    "license": "MIT",
    "related_identifiers": [
      {"identifier": "https://github.com/${REPO}/releases/tag/${TAG}", "relation": "isSupplementTo", "scheme": "url"}
    ]
  }
}
MET
)

echo "Setting metadata..."
curl -s -X PUT "${ZENODO_HOST}/api/deposit/depositions/${deposit_id}" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${ZENODO_TOKEN}" \
  -d "$metadata" > /dev/null

# 5) publish
echo "Publishing deposition..."
pub_resp=$(curl -s -X POST "${ZENODO_HOST}/api/deposit/depositions/${deposit_id}/actions/publish" \
  -H "Authorization: Bearer ${ZENODO_TOKEN}")

doi=$(python - <<PY
import sys,json
r=json.load(sys.stdin)
print(r.get('doi',''))
PY
<<<"$pub_resp")

if [ -n "$doi" ]; then
  echo "Published — DOI: https://doi.org/$doi"
  echo "You can now add the DOI to the GitHub release and README."
else
  echo "Publish response did not include a DOI; response:\n$pub_resp"
  exit 5
fi

exit 0
