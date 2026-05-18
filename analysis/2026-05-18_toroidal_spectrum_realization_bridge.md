# Toroidal Spectrum Realization Bridge

## Executive result

The minimal logical X-association scheme has unsigned Gram spectrum

\[
648^1,
\]

\[
(144+36\sqrt6)^{24},
\]

\[
72^{30},
\]

\[
(144-36\sqrt6)^{24},
\]

\[
40^{81}.
\]

The toroidal realization data explains the middle multiplicities:

\[
\boxed{1,24,30,24,81=1,4\cdot6,5\cdot6,4\cdot6,81.}
\]

Here:

- \(7=5+2\) is the toroidal realization heptad: 5 Császár + 2 Szilassi;
- subtracting the mean leaves a centered \(6\)-dimensional shell;
- the centered shell refines as \(4+1+1\);
- the genus numerator \(12\) is the oriented double cover of the centered shell;
- the two \(24=4\cdot6\) sectors are conjugate \(\sqrt6\)-branches;
- the middle \(30=5\cdot6\) sector is the Császár packet transported across the centered shell.

## Repo evidence used

The heptad projector bridge already parses the toroidal realization file and states the realization packet explicitly as 5 Császár realizations plus 2 Szilassi realizations.  It constructs rank-3 shell projectors, verifies the seven projectors span a 7D heptad, and verifies that subtracting the mean leaves a 6D centered shell. fileciteturn61file0L3-L37

The same script verifies the centered shell refines as \(4+1+1\), that the full heptad refines as \(4+3\), that the centered shell matches the six undirected tetrahedral bridges and the six bivectors in four dimensions, and that the toroidal genus numerator \(12\) is the orientation double cover of the centered shell. fileciteturn62file0L3-L50

The color-atlas script independently checks that the realization packet is \(5+2=\Phi_6=7\), with Császár count \(q+\lambda=5\) and Szilassi count \(\lambda=2\); it also verifies every Császár vertex graph is \(K_7\) and every Szilassi face graph is \(K_7\). fileciteturn64file0L3-L85

The realization data itself records the Császár version 1 seed as 7 vertices, 14 triangular faces, 21 edges, 10 different edge lengths, C2 symmetry, and dual toroid Szilassi; this is the concrete edge-data layer underlying the heptad. fileciteturn69file0L3-L27

## Eigenvalue decompositions

The spectrum values decompose through toroidal/W33 primitives:

\[
648=81\cdot8=H_1\cdot(1+7).
\]

Here \(8=1+7\) is the tetrahedron ground state plus the seven toroidal modes; equivalently it is the tomotope cell count.

\[
72=6\cdot12.
\]

Here \(6\) is the centered heptad/bivector shell and \(12\) is the toroidal genus numerator / orientation double cover.

\[
40=5\cdot8.
\]

Here \(5\) is the Császár realization packet and \(8=1+7\) is the tomotope/toroidal cell packet.

The conjugate pair satisfies

\[
144\pm36\sqrt6=36(4\pm\sqrt6)=6^2(4\pm\sqrt6).
\]

So the irrationality is controlled by the centered shell scale \(6^2\) and the same \(\sqrt6\) already forced by the 6D shell.

The pair also has clean symmetric invariants:

\[
(144+36\sqrt6)+(144-36\sqrt6)=288=4\cdot72,
\]

and

\[
(144+36\sqrt6)(144-36\sqrt6)=12960=160\cdot81.
\]

But

\[
160\cdot81
\]

is exactly the projective nonzero minimal \(X/Z\) pairing count.

## Edge-data bridge

The seven-realization oscillator script records the edge-type counts:

\[
\text{Császár edge types}=10,9,9,8,9,
\]

so

\[
10+9+9+8+9=45=\binom{10}{2}=\binom{\Phi_4}{2}.
\]

The Szilassi edge-type counts are

\[
12,11,
\]

so

\[
12+11=23=f-1=24-1.
\]

The total is

\[
45+23=68=4\cdot17.
\]

This gives a direct edge-data checksum tying the realization packet to the \(\Phi_4=10\) and \(f=24\) layers.

## Topological oscillator

The same seven-realization oscillator script identifies the genus levels as arithmetic sequences:

\[
v(h)=\mu+hq=4+3h,
\]

\[
e(h)=q!+hg=6+15h,
\]

\[
f(h)=\mu+h\Phi_4=4+10h.
\]

Therefore

\[
v(h)-e(h)+f(h)=2-2h.
\]

So the tetrahedron, torus, and double-torus layers form a topological harmonic oscillator for \(h=0,1,2\):

\[
(4,6,4),\quad(7,21,14),\quad(10,36,24).
\]

This is exactly the sequence needed to place the seven toroidal realizations between the tetrahedral ground state and the double-torus exception layer.

## The theorem

**Toroidal Spectrum Realization Theorem.** The non-\(H_1\) primitive multiplicities of the minimal logical X-association scheme factor through the seven-realization toroidal heptad:

\[
24,30,24=4\cdot6,5\cdot6,4\cdot6.
\]

The factor \(6\) is the centered realization shell; \(5\) is the Császár realization packet; and the two \(4\cdot6\) sectors are the conjugate \(\mathbb Q(\sqrt6)\) branches of the Császár internal shell.  The eigenvalues also respect the toroidal packet:

\[
648=81(1+7),
\]

\[
72=6\cdot12,
\]

\[
40=5\cdot8.
\]

Thus the spectrum of \(UU^T\) is the spectral shadow of the toroidal heptad acting on the minimal logical surface.

## Interpretation

The spectrum

\[
648^1,(144+36\sqrt6)^{24},72^{30},(144-36\sqrt6)^{24},40^{81}
\]

is now not merely an association-scheme artifact.  It has a toroidal realization reading:

\[
\boxed{1,24,30,24,81=1,4\cdot6,5\cdot6,4\cdot6,81.}
\]

That means the minimal logical visibility spectrum is organized by:

\[
\text{mean heptad line},
\]

\[
\text{two conjugate }4\times6\text{ branches},
\]

\[
\text{one }5\times6\text{ Császár middle branch},
\]

\[
\text{protected }H_1=81\text{ branch}.
\]

This links the association-scheme spectrum directly to the concrete 5+2 toroidal realization packet, the six-dimensional centered shell, the 7-color/Fano/Heawood layer, and the mod-12 genus numerator.

## Honesty boundary

This is an exact finite arithmetic/spectral bridge. It identifies how the toroidal realization packet organizes the association-scheme spectrum; it does not by itself prove physical dynamics, empirical observables, or continuum geometry.
