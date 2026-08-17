"""Pass5929-5932: Theorem-tier CI linter.

CI MUST fail if any scripts/PART_*.py contains bare assertion words
(CLOSED, PROVED, prediction, realization, oracle) without a PRODUCER tag.

Usage: python ci_theorem_linter.py [--strict]
  --strict: also flag ANSATZ, COMPARISON-ONLY without explicit label
  Exit code 0 = clean, 1 = violations found.

Design rationale (from other-assistant audit):
  The Yang-Mills, neutrino, inflation, scalar, and Weyl-dimension producers
  all contained back-solved or circular definitions that were only caught by
  manual source-code audit. This linter automates the first layer of that check.
"""
import re, sys, pathlib

TRIGGER_WORDS = [
    r'\bCLOSED\b',
    r'\bPROVED\b',
    r'\bprediction\b',
    r'\brealization\b',
    r'\boracle\b',
]

STRICT_WORDS = [
    r'\bANSATZ\b',
    r'\bCOMPARISON.ONLY\b',
]

PRODUCER_TAG = re.compile(r'#\s*PRODUCER\s*:', re.IGNORECASE)


def lint_file(path: pathlib.Path, strict: bool = False) -> list[str]:
    violations = []
    lines = path.read_text(encoding='utf-8', errors='replace').splitlines()
    triggers = [re.compile(p, re.IGNORECASE) for p in TRIGGER_WORDS]
    if strict:
        triggers += [re.compile(p, re.IGNORECASE) for p in STRICT_WORDS]

    for lineno, line in enumerate(lines, 1):
        for pat in triggers:
            if pat.search(line):
                # Check same line or immediately preceding line for PRODUCER tag
                preceding = lines[lineno-2] if lineno >= 2 else ''
                if not (PRODUCER_TAG.search(line) or PRODUCER_TAG.search(preceding)):
                    violations.append(
                        f"{path.name}:{lineno}: bare '{pat.pattern}' without # PRODUCER: tag"
                    )
    return violations


def main():
    strict = '--strict' in sys.argv
    root = pathlib.Path(__file__).parent
    part_files = sorted(root.glob('PART_*.py'))

    all_violations = []
    for f in part_files:
        all_violations.extend(lint_file(f, strict=strict))

    if all_violations:
        print(f"THEOREM-TIER LINTER: {len(all_violations)} violation(s) found")
        for v in all_violations:
            print(' ', v)
        sys.exit(1)
    else:
        print(f"THEOREM-TIER LINTER: clean ({len(part_files)} PART files checked)")
        sys.exit(0)


if __name__ == '__main__':
    main()
