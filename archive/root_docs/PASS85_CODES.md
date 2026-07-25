# Pass 85 — The binary code C₂(W) = [40,16,8] and its weight enumerator

**Status: PASS** — GAP/GUAVA script `w33_pass85_codes.g` → certificate `w33_pass85_codes_out.txt`;
witness `w33_pass85_codes.py` (6/6 checks); test `tests/test_pass85_codes.py` (5/5).

The paper cites C₂(W) = [40,16,8] (Supplement N.2) as the binary code spanned by the rows of the
W(3,3) adjacency, but never computes its **weight distribution**. GUAVA gives the full enumerator:

| weight | 0 | 8 | 12 | 16 | 20 | 24 | 28 | 32 | 40 |
|---|---|---|---|---|---|---|---|---|---|
| # codewords | 1 | **45** | 1120 | 15570 | 32064 | 15570 | 1120 | **45** | 1 |

Total = 2¹⁶ = 65536 ✓.
`W(x,y) = x⁴⁰ + 45x³²y⁸ + 1120x²⁸y¹² + 15570x²⁴y¹⁶ + 32064x²⁰y²⁰ + 15570x¹⁶y²⁴ + 1120x¹²y²⁸ + 45x⁸y³² + y⁴⁰`.

## Structure
- **[40,16,8]** — confirms the cited parameters.
- **Doubly-even**: every codeword weight is divisible by 4.
- **Self-orthogonal** (C ⊆ C⊥) — and *not by accident*: over GF(2) the SRG identity
  `A² = kI + λA + μ(J−I−A) = 12I + 2A + 4(J−I−A) ≡ 0 (mod 2)` because k=12, λ=2, μ=4 are all **even**,
  so every pair of rows is orthogonal. (Verified directly: A² mod 2 = 0.)
- **Symmetric enumerator** (a_w = a_{40−w}) — the code contains the all-ones word.

## The E₆ connection
The **45 minimum-weight (weight-8) codewords = the 45 tritangent planes** of the cubic surface —
the E₆ orbit count (27 lines / 45 tritangent planes / 36 double-sixes) that recurs throughout the
substrate. The code's ground floor is the tritangent-plane geometry.

## Modular forms
Length 40 = 8·5, doubly-even, self-orthogonal. By **Gleason's theorem** the weight enumerators of
doubly-even self-dual codes are polynomials in the E₈ enumerator x⁸+14x⁴y⁴+y⁸ and the Golay
enumerator; C₂(W) is a doubly-even self-orthogonal length-40 code embedding in that modular-forms
ring — the coding-theory face of the same E₈/E₆ structure the graph carries.

## Files
- `w33_pass85_codes.g`, `w33_pass85_codes_out.txt` — GUAVA script + certificate.
- `w33_pass85_codes.py`, `.json` — witness + certificate (6 checks; verifies A²≡0 mod 2 directly).
- `tests/test_pass85_codes.py` — 5 assertions.
