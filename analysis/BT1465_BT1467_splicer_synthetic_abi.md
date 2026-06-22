# BT1465--BT1467: splicer diff manifest, synthetic formula fill, and closure packet ABI

## BT1465 — splicer expected-diff manifest

The Holonet splicer is now paired with an expected-diff manifest.  It records:

- the main source file, `photonic_holonet.tex`;
- the insert file, `analysis/BT1457_claim_firewalled_holonet_section.tex`;
- the local command, `python tools/bt1459_holonet_splicer.py`;
- the target anchor, the fuel section;
- the post-run contract: one marker and one input immediately before that anchor.

This makes the local splice auditable even when the large TeX source is not rewritten through the connector.

## BT1466 — synthetic formula-fill test

The formula parser now has a known-good synthetic worksheet.  Synthetic formulas

```text
g_over_2, a_e, delta_g, ratio_12_13, Schwinger
```

classify exactly to their intended targets.  The quartic demo

```text
4-phi**2
```

evaluates to the structural value \(3.618033988749895\), but is deliberately not classified as a physical target.

This proves the parser logic before the actual Otto equation bodies are transcribed.

## BT1467 — closure packet ABI

The closure schedule is now packaged as a reusable runtime ABI:

\[
(c,s,o)\in C_3\times C_2\times C_2,
\qquad
\mathrm{strand}=4c+2s+o.
\]

The deterministic outputs are

\[
\mathrm{active}=14\mathrm{strand}+13,
\qquad
\mathrm{guard}=(216+2\mathrm{strand},\,216+2\mathrm{strand}+1).
\]

The ABI also carries the retwined frame rule, the syndrome contract, and the claim-tier firewall.

## Current architecture

\[
\boxed{
\text{auditable splice contract}
+\text{synthetic formula parser proof}
+\text{closure packet ABI}
}
\]
