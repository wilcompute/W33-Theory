#!/usr/bin/env python3
"""
Simple utility to find a Zenodo DOI for a GitHub release and insert it into
repository files (release draft, README, outreach). Intended to be run manually
or from CI (workflow_dispatch / scheduled).

Usage (dry-run):
  python scripts/zenodo_sync.py --repo wilcompute/W33-Theory --tag v2026-02-15-qec-mlut

Apply changes:
  python scripts/zenodo_sync.py --repo wilcompute/W33-Theory --tag v2026-02-15-qec-mlut --apply

CI: run with --apply and let the workflow commit/push the changes.
"""
import argparse
import json
import os
import re
import sys
from urllib import request, parse

ZENODO_SEARCH_URL = "https://zenodo.org/api/records/"


def zenodo_search_by_repo_and_tag(repo_full: str, tag: str, max_results: int = 100):
    """Search Zenodo for records referencing the GitHub repo and tag.

    Returns the first matching record dict or None.
    """
    query = parse.quote(repo_full)
    url = f"{ZENODO_SEARCH_URL}?q={query}&size={max_results}"
    with request.urlopen(url, timeout=30) as resp:
        data = json.load(resp)

    for hit in data.get("hits", {}).get("hits", []):
        md = hit.get("metadata", {})
        # 1) quick text match for tag in the JSON dump
        text = json.dumps(hit)
        if tag in text:
            return hit
        # 2) check related_identifiers for a release/tree/tag reference
        for rid in md.get("related_identifiers", []) or []:
            ident = rid.get("identifier", "")
            if repo_full in ident and tag in ident:
                return hit
        # 3) check metadata.version
        if md.get("version") and md.get("version").lower() == tag.lower():
            return hit
        # 4) check custom.code:codeRepository
        custom = md.get("custom", {}) or {}
        code_repo = custom.get("code:codeRepository")
        if code_repo and repo_full in code_repo:
            # tag may be in title or related fields
            if tag in text:
                return hit
    return None


def insert_doi_into_release_draft(draft_path: str, tag: str, doi_url: str) -> bool:
    if not os.path.exists(draft_path):
        return False
    with open(draft_path, "r", encoding="utf-8") as f:
        txt = f.read()

    # If DOI already present, no-op
    if doi_url in txt:
        return False

    # Insert DOI under "Post-release next steps" if present, else append to top
    anchor = "Post-release next steps"
    insert_text = f"\n- Zenodo DOI: {doi_url}  \n"
    if anchor in txt:
        # find anchor and the following list; insert DOI as the first bullet after the anchor
        parts = txt.split(anchor)
        head, tail = parts[0], parts[1]
        # insert DOI at start of tail (after the anchor heading)
        new_tail = anchor + tail
        # attempt to put DOI right after the anchor line-break
        new_txt = head + anchor + "\n" + insert_text + tail
    else:
        new_txt = f"Zenodo DOI: {doi_url}\n\n" + txt

    with open(draft_path, "w", encoding="utf-8") as f:
        f.write(new_txt)
    return True


def insert_doi_into_readme(readme_path: str, tag: str, doi_url: str) -> bool:
    if not os.path.exists(readme_path):
        return False
    with open(readme_path, "r", encoding="utf-8") as f:
        txt = f.read()

    if doi_url in txt:
        return False

    # Try to find the release badge link for the tag and append the DOI beside it
    pattern = re.escape(tag)
    if re.search(pattern, txt):
        # Simple approach: append a DOI line right after the first occurrence of the tag
        new_txt = re.sub(f"({pattern})", f"\\1 — Zenodo: {doi_url}", txt, count=1)
    else:
        # Fallback: add DOI under the title (first header)
        new_txt = txt
        lines = new_txt.splitlines()
        for i, line in enumerate(lines):
            if line.strip().startswith("# "):
                lines.insert(i+1, f"**Zenodo DOI:** {doi_url}")
                new_txt = "\n".join(lines)
                break
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_txt)
    return True


def insert_doi_into_outreach(outreach_paths: list, doi_url: str) -> bool:
    changed = False
    for p in outreach_paths:
        if not os.path.exists(p):
            continue
        with open(p, "r", encoding="utf-8") as f:
            txt = f.read()
        if doi_url in txt:
            continue
        # Append DOI to the top of the file under title or at the end
        new_txt = txt + f"\n\nDOI: {doi_url}\n"
        with open(p, "w", encoding="utf-8") as f:
            f.write(new_txt)
        changed = True
    return changed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, help="GitHub repo (owner/repo)")
    parser.add_argument("--tag", required=True, help="Release tag to look for")
    parser.add_argument("--apply", action="store_true", help="Write changes to files")
    parser.add_argument("--commit", action="store_true", help="Create a local git commit after changes")
    args = parser.parse_args()

    repo = args.repo
    tag = args.tag
    repo_url = f"https://github.com/{repo}"

    print(f"Searching Zenodo for records referencing {repo_url} (tag={tag})...")
    hit = zenodo_search_by_repo_and_tag(repo_url, tag)
    if not hit:
        print("No Zenodo record found for that repo+tag (yet).")
        sys.exit(0)

    doi = hit.get("doi") or hit.get("metadata", {}).get("doi")
    if not doi:
        print("Found Zenodo record but DOI not present in API response (unexpected).")
        print(json.dumps(hit, indent=2)[:2000])
        sys.exit(1)

    doi_url = f"https://doi.org/{doi}" if not doi.startswith("http") else doi
    print(f"Found Zenodo DOI: {doi_url}")

    if not args.apply:
        print("Dry-run mode (use --apply to modify files).")
        # show minimal suggested edits
        print(f"Would insert DOI into: RELEASES/DRAFT_{tag}.md, README.md, outreach/*")
        sys.exit(0)

    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    changed_any = False

    draft_path = os.path.join(repo_root, "RELEASES", f"DRAFT_{tag}.md")
    if insert_doi_into_release_draft(draft_path, tag, doi_url):
        print(f"Updated {draft_path}")
        changed_any = True
    else:
        print(f"No change to {draft_path}")

    readme_path = os.path.join(repo_root, "README.md")
    if insert_doi_into_readme(readme_path, tag, doi_url):
        print(f"Updated {readme_path}")
        changed_any = True
    else:
        print(f"No change to {readme_path}")

    outreach_files = [
        os.path.join(repo_root, "outreach", "social_posts.md"),
        os.path.join(repo_root, "outreach", "blog_post.md"),
    ]
    if insert_doi_into_outreach(outreach_files, doi_url):
        print("Updated outreach files")
        changed_any = True
    else:
        print("No change to outreach files")

    if changed_any and args.commit:
        # Create a simple git commit
        try:
            import subprocess
            subprocess.check_call(["git", "add", "RELEASES/" + f"DRAFT_{tag}.md", "README.md", "outreach/social_posts.md", "outreach/blog_post.md"], cwd=repo_root)
            subprocess.check_call(["git", "commit", "-m", f"Add Zenodo DOI for {tag} (automated)"], cwd=repo_root)
            print("Created local git commit (files staged and committed).")
        except Exception as e:
            print("Failed to create git commit:", e)

    if not changed_any:
        print("No files changed.")
    else:
        print("Files updated. If running in CI please commit & push changes.")


if __name__ == "__main__":
    main()
