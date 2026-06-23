# BT1589-BT1591: OAM Radial, Lane, and Front-End Closure

## BT1589

The OAM recenter ABI is tested against a three-shell Laguerre-Gaussian radial
surrogate.  All five operation envelopes use the same stochastic channel family
`L(eta)`, so recenter corrections commute with centered witness gates at shell
level.

The composed envelope is:

```text
eta_total = eta_a + eta_b - (3/2)*eta_a*eta_b
```

The worst symbolic case is mixed OAM/phase recentering followed by `F3`:

```text
eta = 0.18296 < 0.20
```

The centered gate threshold remains `0.10`; the extra headroom is explicitly the
recenter tax, not a measured hardware result.

## BT1590

The full witness protocol is compiled into a compressed exact lane sheet:

```text
5 gates * 9 recenter sectors * 24 centered words * 72 ticks = 77760 ticks.
```

The sheet has `1080` exact 72-tick segments.  Each Hesse lane appears `12960`
times, each detector slot appears `19440` times, native D4 square-pulse words
occupy `25920` ticks, and S4 analyzer-relabel words occupy `51840` ticks.

## BT1591

The OAM-multiplexed diffractive-neural-network literature is promoted only as a
front-end design hint.  The physical proposal is a passive sectorizer: sort or
fan out the nine affine OAM recenter sectors before the exact 24-word transaction
kernel runs.

The firewall remains intact:

```text
OAM-MDNN front end -> 9 recenter sectors -> 24 centered words -> 216 exact ABI addresses.
```

No external optical paper is used as proof of the W(3,3) substrate, measured
leakage, calibrated loss, or quantum-gate coherence.
