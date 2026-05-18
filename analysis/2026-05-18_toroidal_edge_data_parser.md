# Toroidal Edge-Data Parser and Ledger

## What I found

You were right: the repo does contain the edge-data layer.  The clean coordinate/face source is the uploaded PDF, while the repo's bundled text file

```text
data/Toroidal-Polyhedra-Realizations.txt
```

contains both realization coordinates and edge-length class metadata.

The uploaded PDF gives the clean coordinate and face lists.  For example, it records Császár version 1 with vertices \(V_0\) through \(V_6\) and the shared 14 triangular faces; it also records Császár versions 2--5 and Szilassi versions 1--2 with explicit coordinates and face lists. fileciteturn70file0

The repo text adds the edge data.  For Császár version 1, it records:

- 7 vertices,
- 14 triangular faces,
- 21 edges,
- 10 different edge lengths,
- C2 symmetry,
- dual toroid: Szilassi,
- exact edge-length expressions and multiplicities.

fileciteturn69file0L3-L27

## New parser

I added:

```text
analysis/w33_toroidal_edge_data_parser.py
```

It parses the bundled realization text and exports a clean machine-readable ledger:

```text
data/w33_toroidal_edge_data_bridge.json
```

This removes the need to rely on hardcoded constants like:

```python
edge_type_counts = [10, 9, 9, 8, 9, 12, 11]
```

from exploratory scripts.

## Parsed edge-type spectrum

The seven realizations give edge-type counts:

\[
10,9,9,8,9,12,11.
\]

Grouped by family:

\[
\text{Császár}: 10,9,9,8,9,
\]

\[
\text{Szilassi}: 12,11.
\]

Each realization still has exactly 21 actual edge instances.  These numbers count metric edge-length classes, not combinatorial edges.

## Closed forms

The Császár metric edge-type packet satisfies

\[
10+9+9+8+9=45.
\]

But

\[
45=\binom{10}{2}=\binom{\Phi_4}{2}.
\]

The Szilassi metric edge-type packet satisfies

\[
12+11=23=f-1=24-1.
\]

Together:

\[
45+23=68=4\cdot17.
\]

So the edge-data layer gives a real checksum:

\[
\boxed{\text{Császár metric packet}=\binom{\Phi_4}{2}}
\]

\[
\boxed{\text{Szilassi metric packet}=f-1}
\]

\[
\boxed{\text{Total metric packet}=4\cdot17.}
}
\]

## Mod-12 observation

The heptad edge-type counts occupy the consecutive mod-12 residues

\[
8,9,10,11,0.
\]

Explicitly:

\[
8,9,9,9,10,11,12\equiv8,9,9,9,10,11,0\pmod{12}.
\]

This is not the same as the genus-equation allowed residues \(0,3,4,7\), but it is adjacent to them as a metric-spectrum packet.  My current read is:

- \(0,3,4,7\pmod{12}\) governs allowed topological/genus roots;
- \(8,9,10,11,0\pmod{12}\) is the metric edge-splitting shadow of the seven realized charts.

That distinction matters: topological residues classify allowed holes; edge-type residues classify metric degeneracy breaking inside the realized heptad.

## Theorem statement

**Toroidal Edge-Data Ledger Theorem.** The repo's bundled toroidal realization text contains a seven-realization edge spectrum with edge-type counts

\[
10,9,9,8,9,12,11.
\]

The five Császár counts sum to

\[
45=\binom{\Phi_4}{2},
\]

the two Szilassi counts sum to

\[
23=f-1,
\]

and all seven edge-type counts sum to

\[
68=4\cdot17.
\]

Each realization still has 21 actual edge instances, so this is a metric-spectrum layer, not a combinatorial edge-count layer.

## How this modifies the previous spectrum bridge

The previous toroidal-spectrum bridge used the hardcoded edge-type counts from `w33_seven_realizations_oscillator.py`.  This new parser confirms those counts directly from the repo text and exports them cleanly.

So the spectrum bridge now rests on two repo-backed data streams:

1. coordinate/face stream: the uploaded PDF and realization text;
2. metric edge-spectrum stream: the edge class lines inside `Toroidal-Polyhedra-Realizations.txt`.

The next execution should use this parsed edge ledger to build an actual edge-class operator instead of only using sums.
