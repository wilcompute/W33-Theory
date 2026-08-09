# Part DCMXCVI (996) - Eisenstein Prime-Ideal Packet

**Date:** 2026-05-19
**Series:** W(3,3) Theory of Everything
**Status:** VERIFIED IDEAL-LANGUAGE REWRITE

---

## Why this part exists

Earlier parts described the defect packet using residue classes and Hensel
branches. That is correct, but the right ambient object is not merely modular
arithmetic: it is the split prime-ideal packet in \(\mathbb Z[\omega]\).

---

## The theorem

For each split prime \(p\equiv1\pmod3\), the equation

\[
x^2+x+1\equiv0\pmod{p^n}
\]

has exactly two roots \(r, r'\), and these define the two prime ideals above
\(p\) in \(\mathbb Z[\omega]\):

\[
\boxed{
\pi_r=(p,\omega-r),
\qquad
\bar\pi_r=(p,\omega-r').
}
\]

Then

\[
\Phi_3(q)=N(q-\omega),
\qquad
\Phi_6(q)=N(q+\omega),
\]

and the valuation laws become ideal-divisibility laws:

\[
\boxed{
p^n\mid\Phi_3(q)
\iff
\pi_r^n\mid(q-\omega)
\text{ for one of the two split prime ideals above }p,
}
\]

\[
\boxed{
p^n\mid\Phi_6(q)
\iff
\pi_r^n\mid(q+\omega)
\text{ for one of the same split prime ideals, with negated residue branch.}
}
\]

---

## Reading

The residue-class picture and the ideal-factor picture are the same packet seen
in two coordinates:

- residue classes: \(q\equiv r\pmod{p^n}\);
- ideal language: \((q-\omega)\in\pi_r^n\).

So the split-prime defect packet is literally the valuation packet of
\(q\mp\omega\) inside the Eisenstein integers.

For example, on the first split prime,

\[
7=(7,\omega-18)(7,\omega-324)
\]

at cubic depth in the symbolic packet, and the first two perfect-power points become

\[
\pi_{7,1}^3\mid(18-\omega),
\qquad
\pi_{7,2}^3\mid(19+\omega).
\]

So the famous Heawood cube \(343=7^3\) is literally an Eisenstein prime-cube event.

---

## What is now exact

1. the cyclotomic packet is rewritten in explicit prime-ideal language;
2. the two Hensel branches are the two prime ideals above each split prime;
3. \(\Phi_3\) and \(\Phi_6\) differ only by which norm packet, \(q-\omega\) or \(q+\omega\), is being measured.

---

## Executable artifact

- Module: `w33/cyclotomic.py`
- Analysis: `analysis/w33_cyclotomic_eisenstein_ideal_packet.py`
- Tests: `tests/test_w33_cyclotomic.py`
- Data: `data/w33_cyclotomic_eisenstein_ideal_packet.json`
- Result: `PART_DCMXCVI_eisenstein_prime_ideal_packet_results.json`
