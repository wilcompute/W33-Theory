"""Reproduce the pinned729-commit archive without claiming semantic reading.

GitKraken MCP was unavailable during this session. Reuse the repository's
documented local Git archive fallback. Git objects remain the durable originals;
gzip scratch copies are regenerated on demand and are not committed.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib
import gzip
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261027_research_intake as previous


def run():
    previous.SCRATCH = ROOT/'.research_20261028_intake'
    catalogue = json.loads((ROOT/'analysis/2026-10-28_two_week_commit_catalogue.json').read_text())
    chosen = catalogue['commits']
    assert len(chosen) == len({c['sha'] for c in chosen}) == 729
    with ThreadPoolExecutor(max_workers=2) as pool:
        rows = list(pool.map(previous.archive_commit,[c['sha'] for c in chosen]))
    for row in rows:
        row['full_patch_model_read'] = False
        raw = gzip.decompress((ROOT/row['archive']).read_bytes())
        assert len(raw) == row['patch_bytes']
        assert hashlib.sha256(raw).hexdigest() == row['patch_sha256']
    pdf = ROOT/'papers/forty_points/main.pdf'
    digest = hashlib.sha256(pdf.read_bytes()).hexdigest()
    expected = 'c813e604f3cb2c8fc6f6417f85e7ed96a2eeb8faa191d7ccbc6b869d21e3f9a5'
    return dict(snapshot_head=catalogue['snapshot_head'],from_utc=catalogue['from_utc'],
                to_utc=catalogue['to_utc'],commits=rows,
                full_patch_bytes=sum(r['patch_bytes'] for r in rows),
                archive_verification=dict(archives=729,bytes=sum(r['patch_bytes'] for r in rows),
                    all_decompressed_hashes_verified=True),
                paper=dict(sha256=digest,pages=210 if digest == expected else None,
                    full_text_pages_read=list(range(1,20))+list(range(135,140)) if digest == expected else [],
                    visual_pages_inspected=[132] if digest == expected else [],
                    scope='Read flags refer only to the named edition and selected complete pages; other inspected fragments are not counted.'),
                additional_full_patch_read=['9baf04f1752fec07d95f6d6fa0dedf44a116f9e5',
                    '686188ce06cb8580179eda56cc917d22965d53d0'],
                scope='Archival is not completed semantic reading. All historical diff flags start false; legacy-session flags are not inherited. Full paper and two-week diff reading remain unfinished.')


if __name__ == '__main__':
    result = run()
    (ROOT/'analysis/2026-10-28_two_week_patch_manifest.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(commits=len(result['commits']),patch_bytes=result['full_patch_bytes'])))
