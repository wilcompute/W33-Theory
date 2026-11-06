# Pass 12622: on DES-SN5YR, evolving dark energy again beats ΛCDM out of sample, but the leading model changes

Claude track. This is the replication promised in Pass 12620. Scripts: `analysis/toe_uv/class_holdout.py desy5 {sn,bao}` (neutral starts) and `DS=desy5 analysis/toe_uv/class_ppd.py {sn,bao} LCDM,free_neg,cpl,exp 40`. Producer: `analysis/w33_pass12622_desy5_ppd.py`. Test: `tests/test_w33_pass12622.py`.

**Method.** Same as Pass 12620. Train on everything except one probe (SN or BAO), starting from neutral points. Draw from the Fisher posterior at the lowest-training fit (40 draws, 1× width), and score the held probe by elpd = ln⟨e^(−χ²/2)⟩. Total = SN-held + BAO-held. Supernova sample: DES-SN5YR instead of Dovekie.

| gain in elpd over ΛCDM | Dovekie (Pass 12620) | DES-SN5YR |
|---|---:|---:|
| fading coupling | +6.0 | +3.9 |
| CPL (w₀wₐ) | +5.5 | **+9.5** |
| thawing exponential | +3.4 | +5.6 |

DES-SN5YR splits as follows:
- **SN held:** fading +4.7, CPL +3.4, exponential +3.6.
- **BAO held:** CPL +6.1, exponential +2.0, fading −0.8.

## Reading

1. **[N] Replicated:** on both supernova compilations, every evolving model beats ΛCDM out of sample, by 3.4 to 9.5 elpd.
2. **Not replicated:** the ordering among the evolving models. Fading leads on Dovekie and CPL on DES-SN5YR. There is still no evidence for the coupling c′ as opposed to evolving dark energy in general, the same conclusion as Pass 12620, now on two compilations.
3. **Fading's BAO-held score is a method artefact, at least in part.** Two DES-SN5YR training optima nearly tie:
   - c′ = 0.004 (c = −0.73) has train χ² 2252.28 and held BAO 39.3.
   - c′ = 0.033 (c = +0.77) has train χ² 2253.18 and held BAO 23.2.

   The draws are centred on the lower one, and many of them land in pathological regions (held χ² in the thousands). A Gaussian posterior cannot represent two optima of opposite sign in c, so this score is unreliable in both directions.

## Failed draws (disclosed)

CLASS fails on part of the draws ("ze too small"), and the elpd uses only the successful ones, which biases it.

| | SN held, 1× width | SN held, 2× width |
|---|---|---|
| exponential, Dovekie | lost 16/24 | lost 18/24 |
| exponential, DES-SN5YR | lost 20/40 | lost 31/40 |

Fading's BAO-held runs lost 2 to 11. **The exponential's SN-held numbers here and in Pass 12620 rest on 8 to 20 draws**, so treat them as rough.

## Limits

- Fisher draws, not MCMC; plik-lite; the BAO-held run was restarted once after a WSL reboot (resumable, rows unchanged).
- Novelty is not claimed: DESI DR2 already reports the w₀wₐ preference over ΛCDM with DES-SN5YR. What this pass adds is the out-of-sample check, and the finding that the ordering among the evolving models is not stable across compilations.

**Not a theory of everything.**
