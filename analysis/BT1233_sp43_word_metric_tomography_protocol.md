# BT1233 -- Sp43 Word-Metric Tomography Protocol

## Purpose

BT1221 made the full two-qutrit Clifford target exact. BT1228 compressed it to four projective transvections. BT1231 proved that four is exact-minimal inside the projective-transvection family.

BT1233 turns that minimal gate set into a tomography-facing word-metric fingerprint.

## Symmetric gate set

Start with the four BT1228 projective transvections:

\[
(0,0,0,2),\quad (0,2,0,0),\quad (0,0,2,2),\quad (1,0,0,0).
\]

Since each transvection has order \(3\), its inverse is its square. The symmetric gate set therefore has

\[
\boxed{8}
\]

gates.

## Exact word-metric fingerprint

The BFS Cayley closure has

\[
\boxed{51840}
\]

elements, as required for \(Sp(4,3)\). The diameter is

\[
\boxed{14}.
\]

The sphere histogram is

\[
\boxed{1,8,36,126,363,916,2052,4096,7396,12170,16916,7247,476,36,1}.
\]

The checkpoint balls are

\[
\boxed{|B_4|=534,\quad |B_8|=14994,\quad |B_{12}|=51803,\quad |B_{14}|=51840.}
\]

## Protocol

A real tomography recovery can now be checked against the exact finite target:

1. recover the four base transvections and their inverses;
2. verify the order-three local gate law;
3. BFS the recovered symmetric Cayley graph;
4. match order, diameter, sphere histogram, and checkpoint balls;
5. only then compare noisy tomography against the exact finite Clifford fingerprint.

## Boundary

This is not hardware data. It is the exact finite word-metric target that hardware or synthetic tomography must recover.

## Files

- Code: `analysis/bt1233_sp43_word_metric_tomography_protocol.py`
- Result: `data/bt1233_sp43_word_metric_tomography_summary.json`
