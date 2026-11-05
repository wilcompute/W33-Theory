# Passes 12603–12608: one PQ scale for unification and axion dark matter

Claude track. Follows parallel commit `193b7c00a`, whose inverse threshold fit left the masses free. Producer: `analysis/w33_pass12603_to_12608_pq_unification.py`. Test: `tests/test_w33_pass12603_to_12608.py`. Drivers: `analysis/toe_uv/pq_*.py`.

**This is not a theory of everything.** It is an effective field theory below about 4×10¹⁵ GeV. It does not explain generations, flavour, dark energy or quantum gravity, and its GUT completion is not built. It is the one candidate in this programme with several sharp near-term falsifiers.

## The idea

The KSVZ axion needs heavy vectorlike quarks. Ask whether those same quarks make the gauge couplings meet, so one scale does strong CP, dark matter and unification, with the mass tied to f_a and not fitted. Representations then fix E/N, and so the axion-photon coupling, while proton decay bounds M_U.

**Prior art.** Di Luzio, Mescia, Nardi, arXiv:1705.05370, already call this "Q-assisted unification" for a single (3,2,1/6), citing an earlier reference. They decline to use it as a selection criterion, for two reasons that apply here: a GUT completion where only a fragment stays light is not straightforward, and it could be an accident of scanning many representations. They also note N_DW = 1 by opposite charges. Their multiple-representation section concerns coupling bounds, as far as I read it. In two searches I found no multi-representation unification scan with a proton filter that ties the threshold to the axion scale. Those searches were limited, so **no novelty is claimed**. SMASH (Ballesteros, Redondo, Ringwald, Tamarit) has the axion, seesaw and inflation with a single Q, as I recall it, and I did not re-read it.

## 12603: one-loop scan

`pq_unification.py`. Control: reproduces `193b7c00a` to all printed digits, (3,2,1/6) at 1.43822×10⁶ and 2.41792×10¹⁵ GeV.

Of 15 coloured and 6 colourless representations, 1 to 3 coloured with 0 or 1 colourless, 2033 sets have a solution. Those with M_X in 10⁸ to 10¹² GeV, a proton-safe M_U and 1/α_U > 10, whose Q can decay: 5, 3, 1 for an M_U floor of 2, 4, 8×10¹⁵.

## 12604: two-loop

`pq_twoloop.py`, with top Yukawa. **Control:** the generation part of b_ij and the single-Q threshold of Di Luzio et al: 2.12×10⁷ GeV against their 2×10⁷. Single Q: M_U = 1.3×10¹⁵, τ ≈ 4×10³² yr, excluded.

| Model | M_X (GeV) | M_U (GeV) | 1/α_U | τ(p→e⁺π⁰), yr | |
|---|---:|---:|---:|---:|---|
| **A:** (3,1,−⅓) + 2×(3,2,⅙) | 2.7×10¹⁰ | 4.0×10¹⁵ | 37.3 | 3.5×10³⁴ | above Super-K |
| B: (3,1,⅔) + 2×(3,2,⅙) | 1.7×10⁹ | 2.7×10¹⁵ | 35.5 | 8×10³³ | below |
| C: A + (1,1,1) | 1.7×10⁹ | 2.7×10¹⁵ | 35.5 | 8×10³³ | below |

τ = 1.6×10³⁶ yr (M_U/10¹⁶)⁴ (35 α_U)⁻² is an estimate, reliable to a factor of about 3 from matrix elements. Two-loop running moved M_X by 4 and M_U by 2 and removed two of three candidates. Mass splits by factors of 3: M_X 6×10⁹ to 1.3×10¹¹, τ 1.1×10³⁴ to 1.1×10³⁵; 74 percent above Super-K, 4 percent above an assumed Hyper-K reach of 10³⁵.

## 12605: how unique

`pq_full_scan.py`. 85 decaying coloured sets with a one-loop solution reach two loops. **One** passes Super-K at the central estimate, Model A. Three pass within a factor of 3. **GUT-scale thresholds are not included**, and they can move M_U by more than the matrix-element factor, so "1 of 85" holds only if those are small.

## 12606: PQ signs and the coupling

I had set all charges to +1, giving N_DW = 5. For Model A:

| Charges (singlet, doublet, doublet) | N_DW | E/N | g/g_KSVZ |
|---:|---:|---:|---:|
| (+,+,+) | 5 | 22/15 | 0.236 |
| (+,+,−) | 1 | 2/3 | 0.653 |
| (−,+,+) | 3 | 2 | 0.042 |

With N_DW = 1, PQ can break after inflation, f = f_a, and simulations set f_a. So y_Q = M_X/f.

**Chance rates.** Of all 85 sets, 15 percent have M_X in the window 10⁹ to 2×10¹¹, and 47 percent allow N_DW = 1. I set that window after seeing Model A. So "natural y_Q" is about a 7 to 15 percent coincidence and is not impressive alone. The proton filter is the independent discriminator.

## 12607: σ stability narrows it

`pq_gates.py`. Fifteen colour components drive the quartic: 16π² β_λσ ⊃ −2·15·y⁴. Requiring λ_σ > 0 up to M_U:

| f (GeV) | y_Q | m_a (μeV) | min λ_σ | m_ρ (GeV) |
|---:|---:|---:|---:|---:|
| 2.7×10¹⁰ | 1.0 | 211 | 0.73 | 3.3×10¹⁰ |
| 5×10¹⁰ | 0.55 | 114 | 0.13 | 2.6×10¹⁰ |
| 10¹¹ | 0.27 | 57 | 0.008 | 1.3×10¹⁰ |
| 2×10¹¹ | 0.14 | 28 | 0.0005 | 6×10⁹ |

Threshold stabilisation of the Higgs needs m_ρ below λ_H's instability, near 10¹⁰ GeV at M_t = 173.1 and moving with M_t. So the consistent window is **y_Q ≈ 0.1 to 0.3, m_a ≈ 25 to 60 μeV**. A common y is assumed, and the fermion RGE is a simplified one-loop form.

**Tension.** Recent simulations favour heavier post-inflation axions: 40 to 180 μeV, and 95 to 450 μeV from Kaltschmidt et al, arXiv:2502.02398, with others higher. Only the low end of the first overlaps. Above about 60 μeV this model needs a higher instability scale, so a lower M_t, or it fails.

PQ quality: Planck-suppressed operators must start at dimension 12 or above for f = 10¹¹. Open: nothing here protects them.

## 12608: scorecard and falsifiers

| Gate | Status |
|---|---|
| Couplings meet | yes at two loops, common threshold: two unknowns from two differences, not a prediction by itself |
| Proton | 3.5×10³⁴ yr, at the limit |
| Strong CP | axion; PQ quality open |
| Dark matter | axion, post-inflation; tension with some simulations |
| Neutrinos, leptogenesis | seesaw with M_N ~ f available: y_ν ~ 0.01 to 0.1 for 0.05 eV; not predicted |
| Higgs stability | threshold mechanism available, narrows m_a |
| Inflation | Higgs-portal, as in SMASH; not recomputed |
| Generations, flavour | **not explained** |
| Dark energy | **not explained** |
| Quantum gravity | **not included** |
| GUT completion | **not built**, tuned split |

**How it dies, in order of likely reach:**
1. An axion at KSVZ or DFSZ strength, or a coupling other than the three in 12606. For N_DW = 1 the claim is E/N = 2/3.
2. No p→e⁺π⁰ at Hyper-K, at about 10³⁵ yr, without GUT thresholds to explain it.
3. Dark matter axion above about 60 μeV with M_t above about 173 GeV.

Colliders cannot test it directly, since Q sits at about 10¹⁰ GeV. I did not compare g = 0.65 g_KSVZ at 25 to 60 μeV against current haloscope limits. That is the next thing to do.

## Cross-boundary note

For `193b7c00a`, by the same estimate its one-field witnesses give τ ≈ 5×10³³ yr for the quark, and about 4×10²⁹ for the triplet, whose M_U is 2.4×10¹⁴. Both are below Super-K. At two loops the quark is 4×10³². The parallel track did flag proton decay as untested.

## Sources

arXiv:1705.05370, 2502.02398, 2308.08585, 2001.05235, 1611.05478. Super-K p→e⁺π⁰ 2.4×10³⁴ yr as quoted in `193b7c00a`.
