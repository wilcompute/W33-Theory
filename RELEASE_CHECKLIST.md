Release checklist — one-line steps

- Replace [ARXIV-ID] in LINKEDIN_ANNOUNCEMENT.md and OUTREACH_EMAILS.md
- Commit .zenodo.json update with arXiv id
- Tag release: `git tag -a v1.0.0 -m "ArXiv submission — April 2026"`
- Push master + tags: `git push origin master --tags` (this mints Zenodo DOI)
- Replace [ZENODO-DOI] in LINKEDIN_ANNOUNCEMENT.md and OUTREACH_EMAILS.md
- Post LinkedIn primary + X thread
- Send outreach emails per schedule
- Schedule Day 3 and Day 7 follow-ups

Local build

- Run: `bash compile.sh --arxiv`
- Verify generated PDF and figures in `figures/`
