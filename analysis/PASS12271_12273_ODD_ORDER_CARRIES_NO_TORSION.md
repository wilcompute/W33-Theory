# Passes 12271–12273: odd versus even order

Claude track. Producer: `analysis/w33_pass12271_to_12273_odd_order_carries_no_torsion.py`. Drivers: `analysis/search_drivers_12271/`.

The question: is the spectrum a function of the Wilson lines' classes modulo the lattice, or does the lattice representative matter?
12267 found that on T6/Z3 the stock engine's spectrum of a mod-1-only input always equals that of its consistent repairs. This round
tests whether that is a property of order three, by running the same experiment at order two.

## 12271: the relabelling test

The relabelling is W → W + 2r, with r a root and r·V0 integral (on T6/Z3 both lines of an identical pair move together). It changes
no Ploger datum.

| set | spectra unchanged |
|---|---|
| T6/Z3, inputs failing only (7f) | **80/80** |
| T6/Z3, consistent models (A8 SMs among them) | **80/80** |
| T6/(Z2^W×Z2×Z2), order-2 inputs failing only (7f) | 60/80 |
| T6/(Z2^W×Z2×Z2), consistent repairs of those inputs | 39/80 |

The last row is the control. It refuted the first reading, which was that the order-2 stock outputs were simply ill-defined. At even
order the relabelling changes the spectrum **even on consistent models**. This is the published mirage-torsion statement of Plöger,
Ramos-Sánchez, Ratz and Vaudrevange (hep-th/0702176): lattice shifts of Wilson lines act as generalized discrete torsion. That
statement is cited here, not claimed.

**What is measured here:** at order three no such dependence appears, on consistent models or on the inputs the stock engine
accepted wrongly.

*Suspected mechanism, not proved:* the phases a lattice shift can induce are signs, and an order-3 projection admits no nontrivial
sign (Z2 ⊗ Z3 = 0).

## 12272: the even-order brothers

Each order-2 input has four consistent lifts: two repairs, and two relabellings of the first. The number of distinct spectra among
them is a lower bound on the torsion brothers per input:

| distinct spectra | inputs |
|---|---|
| 1 | 2 |
| 2 | 22 |
| 3 | 12 |
| 4 | 4 |

The stock engine's output for an order-2 input agrees with neither repair in 30 of 40 inputs, and with both in 3.

## 12273: synthesis

Together with 12267, the corpus's T6/Z3 spectra, counts and lead models (T115 included) are spectra of consistent models. The
consistent-subset restatement of 12259/12261 was therefore too strict.

An order-2 Wilson-line scan run on the stock engine would **not** be safe. The corpus has none on that engine.
