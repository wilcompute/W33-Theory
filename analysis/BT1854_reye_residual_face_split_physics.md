# BT1854 — Reye/Residual Face Split Physics

BT1854 interprets the 44-face K12 horizon as two optical layers.

## Split

```text
Reye faces = 16
Residual faces = 28
Total faces = 44
```

Directed edge incidences:

```text
Reye layer = 16 * 3 = 48
Residual layer = 28 * 3 = 84
Total = 44 * 3 = 132
```

## Arithmetic dictionary

```text
48 = 4 * 12 = mu * k
84 = 7 * 12 = Phi6 * k
132 = 11 * 12 = (k-1) * k
```

## Current closure split

```text
Reye:     12 ordinary flat + 4 antipodal flat
Residual: 20 ordinary flat + 8 antipodal flat
```

## Interpretation

The Reye layer is the tomotope/Reye stabilizer skeleton inherited from the Q4 antipodal quotient.  The residual layer is not noise; it is the genus-6 completion shell.

So the finite optical compiler has two layers:

```text
Reye/tomotope stabilizer layer: 48 incidences = mu*k
Residual genus-completion layer: 84 incidences = Phi6*k
```

Together they produce the `[72,66,6]` optical face code.

## Connection to the Holonet paper

The Holonet TeX leaves error correction and UTM tape mapping as open questions.  This split supplies a concrete finite compiler surface: the single-photon qutrit route can be guarded by a K12/F12 face-code layer rather than by an ad hoc repetition code.

Boundary: this is a structural compiler interpretation, not a measured photonic implementation.
