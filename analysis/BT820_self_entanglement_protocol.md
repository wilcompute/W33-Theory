# BT820 — How to Self-Entangle a Photon, and the One-Device TQC/TQN

The build document.  Every quantitative claim verified in
bt820_self_entanglement_protocol.py.

## What self-entanglement IS

Entanglement is a relation between tensor factors; nothing requires the
factors to be different particles.  A photon carries at least four
independent degrees of freedom (polarization, path, time-bin, sideband),
so ONE photon is already a multi-register machine: dim >= 3^4 = 81 = the
matter sector.  Self-entanglement = entanglement BETWEEN a photon's own
registers.  In the temporal form it is the photon's past register
entangled with its own future register: the "now" is the interference of
its own history with its own anticipation (companion paper; Aharonov-
Bergmann-Lebowitz two-time formalism).

## HOW to do it (three stages, all standard optics)

```text
L0a  SPATIAL.  Diagonal photon -> polarizing beam splitter:
     (|H,a> + |V,b>)/sqrt2.  One element.  This is the C2(x)C2 = C4
     Witting carrier (BT817): the holonet split 1+12+27 is now the
     photon's measurable entanglement stratification.

L0b  TEMPORAL.  Tritter (symmetric 3-port = the F3 Fourier gate) into a
     0/tau/2tau delay ladder; one electro-optic modulator applies
     CX_{p->f} conditioned on bin index.  Verified exactly:
        |Omega> = CX (F3 x I)|00>  =  (1/sqrt3) sum_j |j>_p |j>_f.
     Two Clifford operations; the photon is entangled with its own
     future.  Readout: Franson-type recombination; inserting U in the
     future arm gives visibility V(U) = |Tr U|/3 (verified: V(F3) = 1/3,
     V(X) = V(Z) = 0) - the photon implements the Choi-Jamiolkowski
     isomorphism on itself: it MEASURES CHANNELS with its own past.

L2   CLOCK (time quasicrystal).  Drive the recombination loop with a
     polarization rotation of theta = arccos(-2/3) - the Boerdijk-
     Coxeter twist - per round trip.  Niven's theorem: theta/pi is
     irrational, so the stroboscopic orbit NEVER repeats: a discrete
     TIME QUASICRYSTAL (the photonic sibling of the Fibonacci-drive
     dynamical topological phase, Dumitrescu et al., Nature 607, 463
     (2022) - quasiperiodic driving protects edge coherence longer than
     any periodic drive can).  Verified: no recurrence to 1e-4 over
     10^4 steps; Steinhaus three-distance signature (<= 3 gap values)
     at n = 7, 12, 13, 40 - and EXACTLY 2 gaps at n = 30 = h(E8): the
     BC ring length is the drive's moment of maximal order, with circle
     deficit 0.0158 (closure happens in S^3 - the 600-cell - not S^1:
     BT485's "aperiodic in 3D, periodic in 4D" made stroboscopic).
```

## Why the machine is hardware = software = network at once

```text
hardware   the 540-chart photonic mesh: each chart an 8-state Q3 block
           with native XOR addressing (BT777); charts ARE the W33 cubes
software   braid words: sigma^5 = Z exact in Q(zeta10) (BT740) - gate
           sequences are routing masks and vice versa
network    the 1620 apartment links of the Tits building (BT744/777):
           inter-chart hops; diameter 5
memory     the Steinberg 81-sector (BT742): cohomologically protected,
           gauge-invariant - the firewall
immune     the 15 = g_neg eigenspace pressed against the Ramanujan
           bound (BT778): spectral drift shows there first
sync       beacon heptads: 7-state constellations, all pairwise
           visibility 1/3, master beacon + two triads (BT819)
timetable  the 36 spreads = all complete measurement schedules (BT817)
clock      internal Z12 gauge clock + external Z7/Z13 references +
           the irrational BC drive for quasicrystalline protection
```

Transporting the photon through the mesh IS applying the braid word IS
routing the packet: one physical process, three descriptions.  That is
the precise sense of "the network is the computer": the holonet thesis
with every layer now a verified theorem.

## The geometric-optics layer

The flat F2^4 register (BT741) is a Pancharatnam-Berry statement: loops
in the chart atlas accumulate zero geometric phase (trivial holonomy),
so register states are geometric-phase-protected; the duo bit (corner
choice at the chart center, BT775/776) is the one holonomy-bearing
datum.  Geometric quantum optics is the natural implementation layer:
polarization-path cycles realize the chart-atlas connection physically.

## Boundary

Open: the L0b hardware tolerance budget (visibility 1/3 witnesses under
loss/dephasing - the q/mu = 3/4 Werner threshold of the companion);
OAM as the fifth register (lifting C4 toward the 81-dim matter space on
one photon); and the experimental discriminator between periodic 7:13
two-tone driving (period-91 approximant) and the true irrational BC
drive (three-distance statistics distinguish them at n ~ 91).
