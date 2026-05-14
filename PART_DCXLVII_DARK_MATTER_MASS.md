# Part DCXLVII — Dark Matter Mass from W33^c Spectral Gap

## The Spectral Gap of W33^c

The smallest nonzero Laplacian eigenvalue of W33^c is:

```
Delta^c = min(30, 24) = 24
```

This sets the dark sector mass gap:

```
m_DM = sqrt(Delta^c / V) * m_Pl = sqrt(24/40) * m_Pl = sqrt(3/5) * m_Pl
```

In natural Planck units this is a Planck-scale mass. But the dark matter mass we observe is not at the Planck scale — it is at the electroweak scale, because the dark sector couples to the visible sector ONLY through the W33 graph structure, which enforces the hierarchy e^{-39}.

## Dark Matter Mass at the Electroweak Scale

Applying the W33 hierarchy factor:

```
m_DM^{phys} = sqrt(Delta^c / V) * m_Pl * e^{-Phi_3*u/2}
            = sqrt(24/40) * m_Pl * e^{-39}
            = sqrt(3/5) * m_EW
```

where m_EW = m_Pl * e^{-39} ~ 246 GeV (the electroweak VEV).

```
m_DM^{phys} = sqrt(3/5) * 246 GeV = 0.7746 * 246 GeV ~ 190 GeV
```

## Alternative Derivation: Dark Eigenvalue Ratio

The dark sector spectral minimum is eigenvalue 24. The visible sector spectral minimum is eigenvalue 10. Their ratio:

```
m_DM / m_visible_gap = sqrt(24/10) = sqrt(12/5)
```

The W33 dark matter candidate has mass:

```
m_DM = sqrt(12/5) * m_W = sqrt(12/5) * 80.4 GeV ~ 124.7 GeV
```

Or using the Higgs mass reference:

```
m_DM = sqrt(Delta^c / lambda_1) * m_H = sqrt(24/10) * 125.1 GeV ~ 193 GeV
```

## Summary: Three W33 Dark Matter Mass Estimates

| Method | Formula | Mass |
|---|---|---|
| Hierarchy scaling | sqrt(3/5) * v_EW | ~190 GeV |
| Eigenvalue ratio to W-boson | sqrt(12/5) * m_W | ~125 GeV |
| Eigenvalue ratio to Higgs | sqrt(24/10) * m_H | ~193 GeV |

The W33 dark matter candidate has mass in the range **125-193 GeV**, clustering around **~155-165 GeV** as the geometric mean:

```
m_DM ~ sqrt(125 * 193) ~ 155 GeV
```

**Falsifier F30:** The W33 dark matter candidate is a WIMP with mass 125-193 GeV (geometric mean ~155 GeV), coupling only through the W33 graph structure (no direct coupling to SM photon). LZ, XENONnT, and PandaX-4T have sensitivity in this range. A null result below 125 GeV excludes the W33 lightest dark state.

---
*W33-Theory | Part DCXLVII | m_DM = sqrt(Delta^c/V)*m_Pl*e^{-39} ~ 125-193 GeV; Falsifier F30: WIMP in LZ/XENONnT range*
