#!/usr/bin/env python3
"""Occurrence-local identity guard for the five degree-540 PSp(4,3) sets.

Pass 1136 introduced a binary point/line classifier. Pass 1139 proves that
PSp(4,3) has five transitive degree-540 coset actions, so this guard now uses
the complete canonical species list. Explicit tags bind to the nearest literal
``540`` on the same line; a tag beside one occurrence can never classify a
second occurrence merely because both appear on that line.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
import os
from pathlib import Path
import re
import sys
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
SELF_PATH = Path(__file__).resolve()
DEFAULT_OUT = ROOT / "data" / "BT1634_540_audit_results.json"
EXTENSIONS = {".md", ".tex", ".py", ".json", ".txt", ".csv", ".jsonl"}
EXCLUDED_RELATIVE_PATHS = {
    "data/BT1634_540_audit_results.json",
    "data/BT1634_540_audit_results.synthetic.json",
    "data/w33_540_occurrence_registry_v1.json",
    "data/w33_formula_search_universe_v1.json",
}
WINDOW = 180
PRUNED_DIRS = {
    ".continuity",
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "site-packages",
    "venv",
}

CANONICAL_SPECIES = (
    "point-nonedge",
    "double-six-nonincident",
    "gq42-arc",
    "outer-4c",
    "line-nonedge",
)
COMPATIBILITY_TAGS = ("both", "mixed", "unrelated")
TAGS = {
    category: f"{{540:{category}}}"
    for category in (*CANONICAL_SPECIES, *COMPATIBILITY_TAGS)
}
TAG_PATTERN = re.compile(
    r"\{540:(?P<category>"
    + "|".join(re.escape(category) for category in TAGS)
    + r")\}",
    re.I,
)
NUMBER_PATTERN = re.compile(r"(?<![A-Za-z0-9_])540(?![A-Za-z0-9_])")

MIXED_SIGNALS = {
    "degree_species_census": (
        r"(?:degree.{0,8}540|540[- ](?:element|object|species)|"
        r"transitive.{0,24}540).{0,100}"
        r"(?:species|census|coset|actions?|sets?|class(?:es)?)|"
        r"transitive.{0,60}degree.{0,8}540"
    ),
    "complete_or_five": (
        r"(?:complete|five|all five|exactly five).{0,80}(?:540|species)"
    ),
    "multiple_we6_classes": (
        r"(?:three|multiple).{0,50}(?:classes|carriers).{0,30}540|"
        r"classes.{0,60}540|class_sizes.{0,30}540|"
        r"we6Class[A-Za-z]+.{0,30}540"
    ),
    "aggregate_field": (
        r"(?:coset_degrees|class_sizes|subgroup_class_lengths|"
        r"expectedClassLengths).{0,100}540|"
        r"540.{0,100}(?:coset_degrees|class_sizes)"
    ),
    "factorization_warning": (
        r"(?:factorization|factorisation|identif(?:y|ies|ied)|shared "
        r"(?:number|cardinality)).{0,100}540|"
        r"540.{0,80}identif(?:y|ies|ied)|(?:25920|51840)\s*=\s*540"
    ),
    "identity_tooling": (
        r"540.{0,30}(?:classifier|guard|tag|occurrence|audit)|"
        r"(?:classifier|guard|tag|occurrence|audit).{0,30}540"
    ),
    "alias_inventory": r"(?:aliases|vocabulary).{0,100}540",
    "both_carriers": r"(?:both|several).{0,60}(?:carrier|action|class).{0,30}540",
}

SPECIES_SIGNALS = {
    "point-nonedge": {
        "noncollinear_point": r"noncollinear.{0,20}point",
        "point_pair": r"point[-_ ]?pairs?",
        "point_nonedge": r"point[-_ ]?nonedge|point.{0,12}non[-_ ]?edge",
        "mu4": r"(?:mu|\\mu)\s*[=:]\s*4",
        "srg": r"SRG\s*\(\s*40\s*,\s*12\s*,\s*2\s*,\s*4\s*\)",
        "mu_distribution": r"mu[_ -]?distribution",
        "tom77": r"TOM.{0,12}(?:position.{0,4})?77",
        "class4a": r"(?:class|WE6|W\(E_6\)).{0,16}4A",
    },
    "double-six-nonincident": {
        "double_six_nonincident": r"(?:non[- ]?incident.{0,30}double[- ]six|double[- ]six.{0,30}non[- ]?incident)",
        "cubic_line_complement": r"(?:cubic[- ]line|27[- ]line).{0,35}(?:complement|non[- ]?incident)",
        "36x15": r"36\s*(?:\*|\\cdot|x|times)\s*15",
        "rank28": r"rank[-_ ]?28",
        "tom78": r"TOM.{0,12}(?:position.{0,4})?78",
        "nonincident_flags": r"nonincident[_ -]?flags?",
    },
    "gq42-arc": {
        "hashimoto_arc": r"Hashimoto.{0,16}arcs?",
        "gq42_arc": r"(?:GQ|\\GQ)\s*\(\s*4\s*,\s*2\s*\).{0,24}arcs?",
        "support_geometry_arc": r"support[-_ ]geometry.{0,24}arcs?",
        "45x12": r"45\s*(?:\*|\\cdot|x|times)\s*12",
        "rank27": r"rank[-_ ]?27",
        "tom79": r"TOM.{0,12}(?:position.{0,4})?79",
    },
    "outer-4c": {
        "outer4c": r"(?:outer|class|WE6|W\(E_6\)).{0,20}4C",
        "a4_c4": r"A4\s*[:x]\s*C4|A_4\s*[:x]\s*C_4",
        "c4_s4": r"C4\s*x\s*S4|C_4\s*\\times\s*S_4",
        "rank21": r"rank[-_ ]?21",
        "tom80": r"TOM.{0,12}(?:position.{0,4})?80",
    },
    "line-nonedge": {
        "frame": r"\bframes?\b",
        "cube": r"\bcubes?\b",
        "skew": r"skew[-_ ]?(?:pair|line)",
        "line_nonedge": r"line[-_ ]?nonedge",
        "three_A1": r"3A1",
        "Oh": r"O_h|O\\_h",
        "chart": r"\bchart\b",
        "line_stabilizer": r"line.{0,30}stabili[sz]er",
        "root_triples_alias": r"root[_ -]?triples",
        "class2d": r"(?:class|WE6|W\(E_6\)).{0,16}2D",
        "tom81": r"TOM.{0,12}(?:position.{0,4})?81",
    },
}


def signal_hits(window: str, signals: dict[str, str]) -> list[str]:
    return [
        name
        for name, pattern in signals.items()
        if re.search(pattern, window, re.I | re.S)
    ]


def selftest() -> int:
    """Planted-fault recall for the 540-species signal matcher.

    540 is the ambiguous number in this corpus: several genuinely different carriers have
    that size, and a file naming one while meaning another is failure mode 1 with a number
    attached. signal_hits is the whole disambiguation, so it needs to fire on the species
    vocabulary and stay silent on a bare mention of 540 (Pass 5250).
    """
    pn = SPECIES_SIGNALS["point-nonedge"]
    cases = [
        ("planted: noncollinear point", "a noncollinear point pair here", pn, True),
        ("planted: SRG(40,12,2,4)", "the graph SRG(40,12,2,4) again", pn, True),
        ("planted: mu = 4", "with mu = 4 throughout", pn, True),
        ("clean: bare 540", "there are 540 of them", pn, False),
        ("clean: unrelated srg", "the graph SRG(112,30,2,10)", pn, False),
    ]
    ok = True
    print("  selftest -- 540 species signal recall\n")
    for name, window, sigs, want in cases:
        got = bool(signal_hits(window, sigs))
        good = got == want
        ok &= good
        print(f"    {name:32s} hits={str(got):5s} want={str(want):5s} "
              f"{'PASS' if good else 'FAIL'}")
    print(f"""
  THE BARE-540 CASE IS THE POINT OF THE WHOLE GUARD. "there are 540 of them" names the
  number and identifies nothing, and must NOT be read as any species -- {len(SPECIES_SIGNALS)} distinct carriers
  in this corpus have size 540, so the integer alone carries no information. What
  disambiguates is the surrounding vocabulary, which is what signal_hits reads.

  ITS LIMIT: this tests the matcher, not the windowing. Whether the right window reaches the
  right signals depends on _tag_spans and _bounded_context, which are span arithmetic and
  are not exercised here.""")
    return 0 if ok else 1


def _span_gap(left: tuple[int, int], right: tuple[int, int]) -> int:
    if left[1] <= right[0]:
        return right[0] - left[1]
    if right[1] <= left[0]:
        return left[0] - right[1]
    return 0


def _tag_spans(text: str) -> list[tuple[int, int]]:
    return [match.span() for match in TAG_PATTERN.finditer(text)]


def _number_matches(
    text: str,
    start: int = 0,
    end: int | None = None,
) -> list[re.Match[str]]:
    limit = len(text) if end is None else end
    tag_spans = _tag_spans(text)
    matches = []
    for match in NUMBER_PATTERN.finditer(text, start, limit):
        if any(lo <= match.start() < hi for lo, hi in tag_spans):
            continue
        prefix = text[max(start, match.start() - 24):match.start()]
        suffix = text[match.end():min(limit, match.end() + 2)]
        if re.search(
            r"(?:Pass(?:es)?|BT|PART)[~\s-]*$|"
            r"Pass(?:es)?\s+\d+\s*[-–—]+\s*$",
            prefix,
            re.I,
        ):
            continue
        if prefix.endswith(("{", "{{")) and suffix.startswith(":"):
            continue
        line_start = text.rfind("\n", start, match.start()) + 1
        line_prefix = text[line_start:match.start()]
        if re.search(r"[\"']passed_checks[\"']\s*:", line_prefix):
            continue
        if re.search(
            r"\\(?:label|ref|eqref|autoref|path|texttt)\{[^}]*$",
            line_prefix,
        ):
            continue
        matches.append(match)
    return matches


def bound_explicit_tags(text: str, start: int, end: int) -> list[str]:
    """Bind each same-line tag to exactly one nearest numeric occurrence.

    A tie deliberately binds nothing: the passage then needs a less ambiguous
    placement. Compatibility tags ``both`` and ``mixed`` normalize to ``both``.
    """

    line_start = text.rfind("\n", 0, start) + 1
    line_end = text.find("\n", end)
    if line_end < 0:
        line_end = len(text)
    numbers = _number_matches(text, line_start, line_end)
    tags = list(TAG_PATTERN.finditer(text, line_start, line_end))
    assigned: list[str] = []
    target_span = (start, end)
    for tag in tags:
        distances = [
            (_span_gap(tag.span(), number.span()), number)
            for number in numbers
        ]
        if not distances:
            continue
        minimum = min(distance for distance, _ in distances)
        nearest = [
            number for distance, number in distances if distance == minimum
        ]
        if len(nearest) != 1 or nearest[0].span() != target_span:
            continue
        category = tag.group("category").lower()
        assigned.append("both" if category == "mixed" else category)
    return sorted(set(assigned))


def _bounded_context(text: str, start: int, end: int) -> str:
    line_start = text.rfind("\n", 0, start) + 1
    line_end = text.find("\n", end)
    if line_end < 0:
        line_end = len(text)
    return text[line_start:line_end]


def classify_occurrence(text: str, start: int, end: int, path: str) -> dict:
    explicit = bound_explicit_tags(text, start, end)
    context = _bounded_context(text, start, end)
    species_hits = {
        category: signal_hits(context, SPECIES_SIGNALS[category])
        for category in CANONICAL_SPECIES
    }
    mixed_hits = signal_hits(context, MIXED_SIGNALS)
    signalled = [
        category for category, hits in species_hits.items() if hits
    ]

    explicit_species = [
        category for category in explicit if category in CANONICAL_SPECIES
    ]
    if "unrelated" in explicit:
        category, reason = "unrelated", "explicit_unrelated_tag"
    elif "both" in explicit or len(explicit_species) > 1:
        category, reason = "both", "explicit_mixed_tag"
    elif len(explicit_species) == 1:
        category, reason = explicit_species[0], "explicit_tag"
    elif mixed_hits:
        category, reason = "both", "mixed_census_vocabulary"
    elif len(signalled) == 1:
        category, reason = signalled[0], "local_vocabulary"
    elif len(signalled) > 1:
        category, reason = "ambiguous", "conflicting_local_vocabulary"
    else:
        category, reason = "ambiguous", "no_local_object_vocabulary"

    line_number = text.count("\n", 0, start) + 1
    return {
        "line": line_number,
        "category": category,
        "reason": reason,
        "explicit_tags": explicit,
        "species_signals": {
            name: hits for name, hits in species_hits.items() if hits
        },
        "mixed_signals": mixed_hits,
        # Compatibility fields retained for downstream Pass 1136 consumers.
        "line_signals": species_hits["line-nonedge"],
        "point_signals": species_hits["point-nonedge"],
        "snippet": re.sub(
            r"\s+",
            " ",
            text[max(0, start - 90):min(len(text), end + 90)],
        ).strip(),
    }


def audit_file(path: Path, root: Path) -> dict | None:
    if path.resolve() == SELF_PATH:
        return None
    resolved = path.resolve()
    try:
        relative = resolved.relative_to(root.resolve()).as_posix()
    except ValueError:
        relative = resolved.as_posix()
    if relative in EXCLUDED_RELATIVE_PATHS:
        return None
    try:
        text = path.read_text(errors="replace")
    except OSError:
        return None
    occurrences = [
        classify_occurrence(
            text,
            match.start(),
            match.end(),
            path.as_posix(),
        )
        for match in _number_matches(text)
    ]
    if not occurrences:
        return None
    categories = {occurrence["category"] for occurrence in occurrences}
    if "ambiguous" in categories:
        file_category = "ambiguous"
    elif len(categories) == 1 and (
        next(iter(categories)) in CANONICAL_SPECIES
        or next(iter(categories)) == "unrelated"
    ):
        file_category = next(iter(categories))
    else:
        file_category = "mixed-explicit"
    return {
        "path": relative,
        "category": file_category,
        "occurrence_count": len(occurrences),
        "occurrences": occurrences,
    }


def iter_files(root: Path) -> Iterable[Path]:
    """Walk deterministically while pruning repositories, caches, and builds."""

    for directory, dirnames, filenames in os.walk(root, topdown=True):
        dirnames[:] = sorted(
            name for name in dirnames if name not in PRUNED_DIRS
        )
        base = Path(directory)
        for filename in sorted(filenames):
            path = base / filename
            if path.suffix.lower() in EXTENSIONS:
                yield path


def audit(root: Path, selected: list[Path] | None = None) -> dict:
    files: Iterable[Path] = selected if selected is not None else iter_files(root)
    records = []
    for path in files:
        record = audit_file(path, root)
        if record is not None:
            records.append(record)
    counts = Counter(record["category"] for record in records)
    occurrence_counts = Counter(
        occurrence["category"]
        for record in records
        for occurrence in record["occurrences"]
    )
    ambiguous_occurrences = occurrence_counts["ambiguous"]
    total_occurrences = sum(occurrence_counts.values())
    return {
        "schema": "w33.540_occurrence_audit.v3",
        "status": "PASS" if ambiguous_occurrences == 0 else "NEEDS_TAGGING",
        "object_definitions": {
            "point-nonedge": (
                "540 unordered noncollinear point pairs; TOM 77, rank 25"
            ),
            "double-six-nonincident": (
                "540 nonincident double-six/cubic-line flags; TOM 78, rank 28"
            ),
            "gq42-arc": (
                "540 ordered Hashimoto arcs of GQ(4,2); TOM 79, rank 27"
            ),
            "outer-4c": (
                "540 elements of W(E6) class 4C restricted to PSp; "
                "TOM 80, rank 21"
            ),
            "line-nonedge": (
                "540 unordered disjoint/skew line pairs; TOM 81, rank 32"
            ),
            "unrelated": (
                "a literal 540 that is explicitly not one of the five "
                "transitive degree-540 PSp(4,3) carriers"
            ),
        },
        "compatibility_tags": list(COMPATIBILITY_TAGS),
        "file_counts": dict(sorted(counts.items())),
        "occurrence_counts": dict(sorted(occurrence_counts.items())),
        "files_mentioning_540": len(records),
        "literal_occurrences": total_occurrences,
        "ambiguous_occurrences": ambiguous_occurrences,
        "ambiguity_rate_percent": (
            0.0
            if total_occurrences == 0
            else round(100.0 * ambiguous_occurrences / total_occurrences, 6)
        ),
        "target_below_10_percent": (
            total_occurrences > 0
            and 100.0 * ambiguous_occurrences / total_occurrences < 10.0
        ),
        "pruned_directories": sorted(PRUNED_DIRS),
        "excluded_relative_paths": sorted(EXCLUDED_RELATIVE_PATHS),
        "records": records,
    }


def main() -> None:
    if "--selftest" in sys.argv:
        raise SystemExit(selftest())
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="*")
    parser.add_argument("--root", default=str(ROOT))
    parser.add_argument("--json-out", nargs="?", const=str(DEFAULT_OUT))
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="exit 1 when any occurrence is ambiguous",
    )
    args = parser.parse_args()
    root = Path(args.root)
    selected = [Path(filename) for filename in args.files] if args.files else None
    result = audit(root, selected)
    if args.json_out:
        out = Path(args.json_out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            json.dumps(result, indent=2) + "\n",
            encoding="utf-8",
        )
    ambiguous_records = [
        record for record in result["records"]
        if record["category"] == "ambiguous"
    ]
    for record in ambiguous_records:
        print(f"ERROR: {record['path']} has ambiguous 540 occurrence(s)")
        for occurrence in record["occurrences"]:
            if occurrence["category"] == "ambiguous":
                print(
                    f"  line {occurrence['line']}: "
                    f"{occurrence['snippet'][:180]}"
                )
        print(
            "  Add an occurrence-local canonical tag: "
            + ", ".join(TAGS[name] for name in CANONICAL_SPECIES)
            + "; use {540:both} or {540:mixed} only for a genuinely mixed "
              "single occurrence, and {540:unrelated} only when the literal "
              "is not one of the five degree-540 carriers."
        )
    if not args.check_only:
        print(json.dumps({
            "status": result["status"],
            "file_counts": result["file_counts"],
            "occurrence_counts": result["occurrence_counts"],
            "ambiguity_rate_percent": result["ambiguity_rate_percent"],
        }, indent=2))
    if args.strict and ambiguous_records:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
