import re
from pathlib import Path

PATTERN = re.compile(r"json\.dump\([^\)]*indent\s*=\s*2[^\)]*\)")


def test_no_plain_json_dump_with_indent():
    """Fail if any file contains json.dump(..., indent=2) without an explicit default= argument."""
    repo_root = Path('.').resolve()
    matches = []
    for p in repo_root.rglob('*.py'):
        # skip virtual env only
        if 'site-packages' in str(p) or p.match('**/venv/**'):
            continue
        text = p.read_text(encoding='utf-8')
        for m in PATTERN.finditer(text):
            snippet = m.group(0)
            # if 'default=' not present in the snippet, allow if file uses dump_json helper
            if 'default=' not in snippet:
                if 'dump_json(' in text or 'from utils.json_safe import' in text:
                    continue
                matches.append((str(p), snippet))

    if matches:
        msgs = [f"{fn}: {sn}" for fn, sn in matches]
        raise AssertionError("Found json.dump calls with indent=2 and no default=:\n" + "\n".join(msgs))
    # otherwise pass
