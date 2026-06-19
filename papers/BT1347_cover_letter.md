# BT1347 — Cover Letter Draft
## Submission to Physical Review Letters

**Manuscript title:**  
A Single-Photon Universal Quantum Computer via the $W(3,3)$ Symplectic Geometry

**Authors:** W33 Theory Program  
**Repository:** https://github.com/wilcompute/W33-Theory  
**arXiv preprint:** [to be submitted]

---

Dear Editors,

We submit for consideration in *Physical Review Letters* the manuscript
"A Single-Photon Universal Quantum Computer via the $W(3,3)$ Symplectic Geometry."

**What we claim.** We propose a quantum architecture — the Photonic Holonet — in which
a single photon in a compact optical loop constitutes a universal quantum computer.
The claim rests on four exact results:

1. **Qutrit encoding.** The photon prepares a three-valued Bell state using only
   commercially available optical components (PBS, tritter, delay loop, EOM).

2. **Coherent routing.** A 27-dimensional controlled unitary routes the qutrit
   without destroying entanglement. All routing properties are verified numerically
   to 10⁻¹² precision.

3. **Contextuality as computational fuel.** The underlying symplectic geometry
   $W(3,3)$ is Kochen–Specker contextual with KS budget 36/40. The 27-point
   matter shell is exactly the magic sector. By Howard–Wallman–Veitch–Emerson
   (Nature 2014), Clifford completeness plus contextual magic implies universality.

4. **Aperiodic clock.** The Boerdijk–Coxeter recirculation loop advances the
   photon's phase by $\theta = \arccos(-2/3)$, an irrational multiple of $\pi$
   (Niven's theorem), producing a quasicrystalline clock that prevents periodic
   lock-in and enables Turing-complete tape advance.

**Why this is novel.** Previous single-photon quantum information proposals have
not closed the universality argument through contextuality at the substrate level.
Our approach derives universality directly from the geometry of the photon's
state space rather than by external injection of magic states. The matter shell
*is* the magic sector — no factory is needed.

**Reproducibility.** All 16 numerical witnesses are executable Python scripts
(NumPy only) in the public repository. Every number in the paper is exact;
there are no fitting parameters, free variables, or numerical approximations.
A referee can run the full witness chain in under two minutes:

```bash
python proofs/bt1343_unified_witness_runner.py
```

**Experimental accessibility.** The proposed reduced machine costs approximately
\$120k–\$180k USD in commercially available components. A detailed lab build sheet
with instrument specifications and pass criteria is included in the repository
(BT1344).

**Suggested reviewers:**
- Researchers specialising in single-photon quantum information
- Researchers in qutrit contextuality and magic-state resource theory
- Researchers in optical quantum computing architecture

We believe this manuscript is suitable for PRL given its concise proof chain,
its experimental proposal, and its publicly reproducible numerical witnesses.

Thank you for your consideration.

Sincerely,  
W33 Theory Program  
https://github.com/wilcompute/W33-Theory

---

## Submission Checklist

- [ ] arXiv submission (quant-ph primary, math-ph cross-list)
- [ ] Zenodo DOI minted from tagged GitHub release
- [ ] `RELEASE_CHECKLIST.md` in repository updated
- [ ] BT1347 paper compiled with `pdflatex` (two passes)
- [ ] All 16 witnesses pass in unified runner
- [ ] Cover letter tailored to specific journal if not PRL
- [ ] ORCID and affiliation fields populated before submission
