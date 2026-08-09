# Passes 4394–4397 — the convention reinstated, and the certificates repaired

## Pass 4394 — "Honest boundary", back as a checked convention

Pass 4388 went looking for one thing and found another. The hypothesis (coincidence
language concentrates in decorative sections) was refuted at 19-vs-20 over all 216 flags.
The falsifying run turned up this instead:

| arc | files | closes with an "Honest boundary" section |
|---|---:|---:|
| 2026-05 | 98 | **86 (88%)** |
| 2026-06 | 15 | 0 |
| 2026-07 | 69 | 0 |
| everything else | 1427 | 22 (2%) |

One arc wrote a short closing section on nearly every file naming what had been proved and
what had not. It worked — three of the five hardest passages in Pass 4388's sample turned
out to be scoped by their own file's boundary section — and then it stopped, and nothing
replaced it.

`scripts/check_honest_boundary.py` reinstates it. It **warns, never blocks**: a blocking
gate here would train `--no-verify`, which is the same calibration `check_rediscovery.py`
was given for the same reason.

### The number it reports is not a defect count, and the checker says so

| | corpus | this session |
|---|---:|---:|
| scope statement in a **findable** place | 27% | 29% |
| scope language present but **buried** in prose | 6% | 13% |
| **no scope language anywhere** | 67% | 58% |

The middle row is the interesting one and it is not a fault. Pass 4363 says *"SO THE THIRD
FACTOR IS AN ASSUMPTION, not a measurement"* mid-paragraph; Pass 4335 says *"that pass
audits only the LINEAR subgroup"* on line 87. Both are exemplary, and both are invisible to
a grep. **The 2026-05 arc did not write better scope statements than these — it wrote them
under a standard heading, which is what turns a habit into something auditable.**

Retrofitted eight passes this track authored and can scope accurately (4335, 4343, 4353,
4363, 4367, 4374, 4380, 4381), taking the findable share from 15% to 29%. Passes this track
did not write were left alone: inventing a scope for someone else's result is the failure
the convention exists to prevent.

## Pass 4395 — the two repairable certificate classes

`scripts/cert_util.py`, self-tested, one function per class from Pass 4392's taxonomy.

- **float-tail** — `round_floats` to a declared precision of 12. Applied to Passes 4301 and
  4321; both now **REPRODUCE** where they previously DRIFTED. The selftest checks both
  directions: two LAPACK-noise variants must collapse to the same bytes, *and* a genuine
  1e-6 difference must still show. A rounding that hides everything is failure mode 7 in a
  different hat.
- **line-number** — `anchor(path, text)` records what was matched plus a 16-hex digest of
  the file, never the position. The four passes that record manuscript line numbers need
  their data restructured to use it; that is a follow-up, not done badly here.

## Pass 4396 — batch six

37 plain-language boxes placed, backlog **185 → 174**. Same guard as batch five's second
attempt: the owning command must be a sectioning command, control characters are asserted
absent, and `begin`/`end` counts must match before the file is written.

## Pass 4397 — corpus-wide regeneration audit

Running. `scripts/check_certificates_regenerate.py` over every `analysis/w33_pass*.py` at a
240-second budget; this re-runs several thousand passes and will take hours. Results will be
recorded when it finishes — **no rate is claimed from the session-sized sample**, which is
the mistake Pass 4388 made and Pass 4392 declined to repeat.

## Evidence boundary

Pass 4394's percentages are counts of a text signature, not judgements of scope quality; a
file in the "findable" row has a boundary statement, not necessarily a good one. Pass 4395
repairs two of six drifted certificates and leaves four. Pass 4397 has produced no results
yet and nothing here depends on it.
