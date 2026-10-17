# Search drivers for Passes 11936–11949 (Claude track)

## What this folder is

These are the exploratory and search scripts behind the **frozen search records** quoted in the producers of Passes
11936–11949. The producers (`analysis/w33_pass119xx_*.py`) are the certified, regression-tested statements. This folder
lets anyone regenerate the frozen numbers those producers quote instead of trusting them. Every path is repo-relative:
run each script from its own sub-folder with `py -3`. Outputs are written to the current directory, except the MCMC
chains, which are read from `data/w33_pass11942_mcmc_chains/`.

## Driver map

| sub-folder | scripts | produced | used by |
|---|---|---|---|
| `conic/` | `minba.py`, `minRt.py` (+ `minba_*.txt`, `minRt_*.txt`) | the m_u/m_c minimisation onto the stabiliser polar line; the cusp-regime floor R·t ≥ 0.80 | Pass 11938 |
| `conic/` | `near.py`, `perp.py`, `strange0.py`, `Rplane.py`, `ratioR.py`, `weber.py`, `gamma_closed.py`, `gscan.py`, `ellip.py`, `frame.py` | the rank-one polar line; exponents (0,1,2); the Weber law and its η-quotient; elliptic-point values; strange-plane R(t) | Pass 11938 |
| `conic/` | `members.py`, `orbits.py`, `tau.py` | the 54-member log(8/5) orbit scan; boundary τ′ | Pass 11937 |
| `conic/` | `seesaw.py` | seesaw preservation of the Weber invariant | Pass 11940 |
| `ckm/` | `th*.py` | theta with Wilson lines, truncation N = 12, 24, 40 | — |
| `ckm/` | `fit*.py`, `fit*_*.txt` | CKM multistart fits, including the cusp-regime record | Pass 11941 |
| `ckm/` | `fithy*.py`, `hy*_*.txt` | 5̄-only hypercharge fits (A and B branches) | Pass 11942 |
| `ckm/` | `lepbranches.py`, `lep6.py` | lepton ratios under the charge rules 6, 0, −3/2, 1 | Pass 11942 |
| `ckm/` | `mcmc.py`, `mcmc2.py`, `mc*_*.txt` | quark-data posteriors (chains A1, A2, B1, B2, A7, B7) | Passes 11942/11943 |
| `pmns/` | `pmns.py`, `pmns2.py`, `post.py` | PMNS at the best fits and over the posterior (`post.py` reads `data/w33_pass11942_mcmc_chains/xs_*_7.npy`) | Pass 11943 |
| `pmns/` | `lemma.py` | the parity lemma; odd contents | Pass 11944 |
| `pmns/` | `hd.py`, `hd2.py` | H_d Wilson-line lepton classes | Pass 11945 |
| `nu3/` | `scan.py` | odd-heaviest direct textures | Pass 11946 |
| `scp/` | `thbar.py`, `axion.py` | θ̄ at the fits; up-phase rephasing | Pass 11947 |
| `fa/` | `fa.py`, `curve.py` | f_a along the Weber curve | Pass 11948 (withdrawn as an axion by 11949) |
| `qual/` | `q.py`, `q2.py`, `q3.py` | top-Yukawa modulation and θ̄ at the extrema | Pass 11949 |

Two files are one-off paper-edit helpers kept for provenance: `conic/tex37.py` and the `p4x_edit.py` scripts that remain
in the local scratch archive.

## Data

`data/w33_pass11942_mcmc_chains/` holds:
* `chain_*.npy`: thinned (χ², lepton predictions) samples;
* `xs_*_7.npy`: thinned parameter samples of chains A7 and B7;
* `hy2_polished.json`: the polished A and B quark fits.

## Caveats

These are search drivers, not regression tests. Seeds are fixed, but multistart and MCMC outcomes can depend on library
versions. The statements that matter are pinned by the producers' checks.
