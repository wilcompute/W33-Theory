"""Item 3: E/N as a discriminator between the embeddings considered in Passes 12603-12616.
For each embedding, the allowed E/N with N_DW = 1 (or all, where N_DW = 1 is impossible), the axion-photon coupling relative to KSVZ, and where it sits against the GUT line E/N = 8/3 of arXiv:2511.21830 (|E/N - 1.92| <= 0.747 is on or below the line).
  4D Model A, tuned splitting, or orbifold: E/N = 2/3.
  Trinification, 3 x (3, 3bar, 1) vectorlike: E/N = 8/3 or -4/3.
  Standard complete SU(5) KSVZ (5 + 5bar): E/N = 8/3; (10 + 10bar): 8/3.
  KSVZ with a single (3,1,-1/3): 2/3; single (3,1,2/3): 8/3 (control values from the reviews quoted by the search tool in Pass 12603).
usage: py -3 en_discriminator.py"""
import json
from fractions import Fraction as Fr

T3 = {1: Fr(0), 3: Fr(1, 2)}
T2 = {1: Fr(0), 2: Fr(1, 2)}


def EN(reps, q):
    N = sum(a * w * T3[c] for a, (c, w, y) in zip(q, reps))
    E = sum(a * c * w * (y * y + Fr(w * w - 1, 12)) for a, (c, w, y) in zip(q, reps))
    return E / N, abs(2 * N)


cases = {
    "control: single (3,1,-1/3)": ([(3, 1, Fr(-1, 3))], [1]),
    "control: single (3,1,2/3)": ([(3, 1, Fr(2, 3))], [1]),
    "control: SU(5) 5 complete": ([(3, 1, Fr(-1, 3)), (1, 2, Fr(1, 2))], [1, 1]),
    "control: SU(5) 10 complete": ([(3, 2, Fr(1, 6)), (3, 1, Fr(2, 3)), (1, 1, Fr(1))], [1, 1, 1]),
    "Model A, N_DW = 1": ([(3, 1, Fr(-1, 3)), (3, 2, Fr(1, 6)), (3, 2, Fr(1, 6))], [1, 1, -1]),
    "Model A, all +": ([(3, 1, Fr(-1, 3)), (3, 2, Fr(1, 6)), (3, 2, Fr(1, 6))], [1, 1, 1]),
    "trinification 3 pairs, N_DW = 1 (a)": ([(3, 2, Fr(1, 6)), (3, 1, Fr(-1, 3))] * 3, [1, 1, 1, -1, -1, -1]),
    "trinification 3 pairs, N_DW = 1 (b)": ([(3, 2, Fr(1, 6)), (3, 1, Fr(-1, 3))] * 3, [1, 1, -1, 1, -1, 1]),
}
out = {}
LINE = abs(Fr(8, 3) - Fr(48, 25))
for k, (r, q) in cases.items():
    en, ndw = EN(r, q)
    gk = abs(float(en) - 1.92) / 1.92
    out[k] = dict(EN=str(en), NDW=str(ndw), g_over_KSVZ=gk, above_GUT_line=abs(float(en) - 1.92) > 0.747)
    print(k, "E/N", en, "N_DW", ndw, "g/KSVZ %.3f" % gk, "above GUT line" if out[k]["above_GUT_line"] else "on/below", flush=True)
json.dump(out, open("en_discriminator.json", "w"), indent=1)
