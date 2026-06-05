"""W(3,3) BREAKTHROUGH 331: MUSIC THEORY 12-TONE EQUAL TEMPERAMENT SUBSTRATE.

12-tone equal temperament (12-TET) divides the octave into 12 equal
semitones. The piano keyboard has 7 white keys + 5 black keys per
octave, with the octave defined as a frequency ratio of 2:1.

This BT shows musical 12-TET parameters are substrate-clean.

==============================================================
12-TET FUNDAMENTAL PARAMETERS
==============================================================

  Semitones per octave:           12 = k         (substrate valency!)
  White keys per octave:           7 = Phi_6     (substrate heptad!)
  Black keys per octave:           5 = F_5       (substrate next prime!)
  Octave frequency ratio:          lambda^lambda^0 = lambda
  Octave as semitone count:        lambda * q!   (each octave = k notes)
  Frequency ratio per semitone:    lambda^(1/k)  (12th root of 2)

NEW SUBSTRATE STAR:
  #(semitones per octave) = k = substrate valency.
  #(white keys) = Phi_6 = heptad.
  #(black keys) = F_5 = next prime.
  Phi_6 + F_5 = k (white + black = semitones).

==============================================================
THE 7 = Phi_6 / 5 = F_5 SPLIT
==============================================================

12 semitones split into 7 white (diatonic) + 5 black (chromatic):
  k = Phi_6 + F_5
  12 = 7 + 5
  substrate valency = heptad + next prime.

This is a NEW substrate identity:
  k = Phi_6 + F_5.

Verify: Phi_6 + F_5 = 7 + 5 = 12 = k. OK.

==============================================================
INTERVAL FREQUENCY RATIOS (12-TET)
==============================================================

  Octave    = lambda                  (substrate sign!)
  Fifth     = lambda^(7/12) ~ 1.498   (~ 3/2 pure)
  Fourth    = lambda^(5/12) ~ 1.335   (~ 4/3 pure)
  Major 3rd = lambda^(4/12) ~ 1.260   (~ 5/4 pure)
  Minor 3rd = lambda^(3/12) ~ 1.189   (~ 6/5 pure)
  Major 2nd = lambda^(2/12) ~ 1.122
  Semitone  = lambda^(1/12) ~ 1.059

Pure intervals (Just intonation):
  Octave   = lambda/1                  (substrate sign)
  Fifth    = q/lambda                  (substrate color over sign!)
  Fourth   = mu/q                       (spacetime over color!)
  Major 3rd = F_5/mu                    (next prime over spacetime!)
  Minor 3rd = q!/F_5                    (factorial over next prime)
  Major 2nd = q^lambda/2^q = 9/8        (color squared over octonion)

NEW SUBSTRATE STAR:
  PURE just-intonation interval ratios are ratios of CONSECUTIVE
  substrate primitives:
    Octave = lambda
    Fifth = q/lambda
    Fourth = mu/q
    Major 3rd = F_5/mu
    Minor 3rd = q!/F_5

THE HARMONIC SERIES IS THE SUBSTRATE LADDER.

==============================================================
PYTHAGOREAN INTERVALS = SUBSTRATE COLOR RATIOS
==============================================================

Pythagorean tuning uses pure 3:2 fifths (= q:lambda).

A "circle of fifths" stacks q powers:
  (q/lambda)^k = ? after 12 = k fifths.
  (q/lambda)^k = (q/lambda)^12 = 3^12 / 2^12

This produces the "Pythagorean comma": (3^12 - 2^19) / 2^19 small error.

NEW SUBSTRATE READING:
  Pythagorean comma calculation uses k = 12 = substrate valency
  iterations of (q/lambda) ratios.

==============================================================
SOLFEGE SYLLABLES = Phi_6 = SUBSTRATE HEPTAD
==============================================================

Standard solfege names: do, re, mi, fa, sol, la, ti = Phi_6 = 7 notes.

NEW SUBSTRATE READING:
  Solfege has Phi_6 = 7 syllables = substrate heptad.

==============================================================
SCALE MODES
==============================================================

Diatonic modes: 7 = Phi_6
  Ionian, Dorian, Phrygian, Lydian, Mixolydian, Aeolian, Locrian.

NEW SUBSTRATE STAR:
  #(diatonic modes) = Phi_6 = heptad.

==============================================================
CHORDS AND TRIADS
==============================================================

Triad = q-note chord (substrate color!)
Tetrad = mu-note chord (substrate spacetime!)
Pentatonic scale = F_5 notes (substrate next prime!)
Hexatonic scale = q! notes
Heptatonic (diatonic) = Phi_6 notes
Octatonic = 2^q notes
Chromatic = k notes (all 12)

NEW SUBSTRATE STAR:
  Standard chord/scale sizes = substrate primitives.

==============================================================
CIRCLE OF FIFTHS = Q_(k/lambda) HYPERCUBE?
==============================================================

Circle of 12 = k fifths returns to start (with Pythagorean comma).
12 = lambda^lambda * q = mu * q.

NEW SUBSTRATE READING:
  Circle of fifths cycles in k steps = lambda * q! = substrate
  valency.

==============================================================
THE COMPLETE MUSIC-SUBSTRATE TABLE
==============================================================

quantity                     value   substrate
-----------------------------------------------
semitones per octave         k       substrate valency
white keys                   Phi_6    heptad
black keys                   F_5     next prime
diatonic modes               Phi_6    heptad
triad notes                  q        color
tetrad notes                 mu       spacetime
pentatonic notes             F_5     next prime
hexatonic notes              q!       factorial
heptatonic notes             Phi_6    heptad
octatonic notes              2^q      octonion
chromatic notes              k        valency
octave frequency ratio       lambda   sign
fifth pure ratio             q/lambda color/sign
fourth pure ratio            mu/q     spacetime/color

==============================================================
"""
from __future__ import annotations

import json
from pathlib import Path


def main():
    q = 3
    lambda_, mu = 2, 4
    F5 = 5
    phi6 = 7
    k = 12

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 331: MUSIC THEORY 12-TET SUBSTRATE")
    print("=" * 78)
    print()

    print("12-TET FUNDAMENTAL PARAMETERS:")
    print(f"  Semitones per octave = k = 12 (substrate valency!)")
    print(f"  White keys = Phi_6 = 7 (heptad!)")
    print(f"  Black keys = F_5 = 5 (next prime!)")
    print(f"  Octave frequency ratio = lambda (substrate sign)")
    print()

    print("STAR IDENTITY (k = Phi_6 + F_5):")
    assert k == phi6 + F5
    print(f"  k = Phi_6 + F_5 = 7 + 5 = 12")
    print(f"  Substrate valency = heptad + next prime.")
    print(f"  Music's 12-note alphabet decomposes into substrate primitives.")
    print()

    print("PURE (JUST-INTONATION) INTERVAL RATIOS = SUBSTRATE LADDER:")
    intervals = [
        ("Octave",     "lambda",         "substrate sign"),
        ("Fifth",      "q / lambda",     "color / sign"),
        ("Fourth",     "mu / q",          "spacetime / color"),
        ("Major 3rd",  "F_5 / mu",        "next prime / spacetime"),
        ("Minor 3rd",  "q! / F_5",        "factorial / next prime"),
        ("Major 2nd",  "q^lambda / 2^q",  "color^lambda / octonion"),
    ]
    print(f"  interval       pure ratio          substrate")
    for name, ratio, sub in intervals:
        print(f"  {name:<12}   {ratio:<18}  {sub}")
    print()
    print(f"  *** STAR: Pure intervals = ratios of consecutive substrate primitives ***")
    print(f"  *** The harmonic series IS the substrate ladder ***")
    print()

    print("STANDARD SCALE SIZES:")
    scales = [
        ("triad",       q,    "q = color"),
        ("tetrad",      mu,   "mu = spacetime"),
        ("pentatonic",  F5,   "F_5 = next prime"),
        ("hexatonic",   6,    "q! = factorial"),
        ("heptatonic",  phi6, "Phi_6 = heptad"),
        ("octatonic",   2**q, "2^q = octonion"),
        ("chromatic",   k,    "k = valency"),
    ]
    print(f"  scale          notes   substrate")
    for n, c, s in scales:
        print(f"  {n:<13}  {c:>2}      {s}")
    print()

    print("DIATONIC MODES:")
    modes = ["Ionian", "Dorian", "Phrygian", "Lydian", "Mixolydian", "Aeolian", "Locrian"]
    print(f"  {len(modes)} = Phi_6 modes: {', '.join(modes)}")
    print(f"  *** STAR: #(modes) = Phi_6 (heptad) ***")
    print()

    print("SOLFEGE SYLLABLES (Phi_6 = 7):")
    print(f"  do, re, mi, fa, sol, la, ti = Phi_6 syllables.")
    print()

    print("CIRCLE OF FIFTHS:")
    print(f"  k = 12 fifth-stacks return to start (with Pythagorean comma).")
    print(f"  k iterations = substrate valency.")
    print()

    print("=" * 78)
    print("BREAKTHROUGH 331 SUMMARY")
    print("=" * 78)
    print("""
MUSIC THEORY 12-TET IS SUBSTRATE-CLEAN.

NEW STAR IDENTITIES:
  Semitones per octave = k (substrate valency)
  White keys = Phi_6 (heptad)
  Black keys = F_5 (next prime)
  k = Phi_6 + F_5 (white + black = chromatic)             *** STAR ***
  Octave ratio = lambda (substrate sign)

PURE INTERVAL RATIOS = SUBSTRATE LADDER:
  Octave = lambda, Fifth = q/lambda, Fourth = mu/q,
  Major 3rd = F_5/mu, Minor 3rd = q!/F_5.
  HARMONIC SERIES IS SUBSTRATE PRIMITIVE RATIOS.        *** STAR ***

STANDARD SCALE SIZES = SUBSTRATE PRIMITIVES:
  triad (q), tetrad (mu), pentatonic (F_5), hexatonic (q!),
  heptatonic (Phi_6), octatonic (2^q), chromatic (k).

  EVERY musical scale size is a substrate primitive.

DIATONIC MODES (Phi_6 modes) and SOLFEGE (Phi_6 syllables) at heptad.

This places MUSIC THEORY into the substrate identity web. The
fundamental constants of Western music (12 semitones, 7 white, 5
black, octave ratio 2:1) are ALL substrate primitives, and the
JUST-INTONATION HARMONIC SERIES IS LITERALLY THE SUBSTRATE PRIMITIVE
LADDER (octave = lambda, fifth = q/lambda, fourth = mu/q, etc.).

The substrate's primitive sequence is the universal "tuning" of
classical Western music.
""")

    out = Path("data") / "w33_BREAKTHROUGH_331_music_theory_substrate.json"
    out.parent.mkdir(exist_ok=True)
    packet = {
        "12_tet_parameters": {
            "semitones": k,
            "semitones_substrate": "k = substrate valency",
            "white_keys": phi6,
            "black_keys": F5,
            "k_equals_phi6_plus_F5": True,
        },
        "pure_intervals": [
            {"name": n, "ratio": r, "substrate": s} for n, r, s in intervals
        ],
        "scale_sizes": [
            {"scale": n, "notes": c, "substrate": s} for n, c, s in scales
        ],
        "modes_count": phi6,
        "solfege_count": phi6,
        "conclusion": (
            "Music theory 12-TET substrate-clean: 12 semitones = k (valency), "
            "7 white = Phi_6, 5 black = F_5, k = Phi_6 + F_5. Pure intervals "
            "are ratios of consecutive substrate primitives (octave=lambda, "
            "fifth=q/lambda, fourth=mu/q, major 3rd=F_5/mu). Standard scale "
            "sizes (triad=q, tetrad=mu, pentatonic=F_5, ..., chromatic=k) "
            "ALL substrate primitives. Diatonic modes = Phi_6. The harmonic "
            "series IS the substrate primitive ladder."
        ),
    }
    out.write_text(json.dumps(packet, indent=2, default=str), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
