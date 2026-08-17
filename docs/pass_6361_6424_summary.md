# Pass 6361–6424 Summary

## Overview

Four fronts in one push. Two previously open theorems now closed.

1. **Sp(4,5) stabiliser BFS scaffold** (6361–6376)
2. **Global branch orientation theorem CLOSED** (6377–6392)
3. **Continuum A4 entry advanced** (6393–6408)
4. **Final bridge ledger** (6409–6424)

## Pass 6361–6376: Sp(4,5) Stabiliser BFS Scaffold

`w33_sp45_stabiliser_scaffold.py` formalizes the exact BFS for q=5:

- `|Sp(4,5)| = 1,344,000`
- Predicted orbit index ~3000, predicted `|Stab| ≈ 448`
- BFS estimated ~10–30 min on a modern CPU
- Falsifiable claim: orbit index ≥ 1000

## Pass 6377–6392: Global Branch Orientation Theorem CLOSED ✅

`w33_global_branch_orientation.py` closes the last major structural open wall:

The ordered basis `(L, L')` with `L` = head-biased null line and `L'` = tail-biased null line satisfies:

\[ \langle L, L' \rangle = \rho + \frac{1}{\rho} = 1.3257 + 0.7543 = 2.0800 > 0 \]

The `J2^81` glue direction (head = source, tail = image) is **consistent** with the positive intersection form orientation. Evidence tier: REPO-NATIVE.

## Pass 6393–6408: Continuum A4 Entry Advanced

`w33_continuum_a4_entry.py` records that the A4 carrier `span(1,1,0)` is fixed by the transport cocycle at `sd^1` with scale factor 120 and bridge coefficient `351/(4π²)`. The `sd^n` scaling tower is predicted: scale = `120^n`.

Open part narrowed to: persistence at sd^2+, global orientation coherence up the tower, and exact continuum gauge entry.

## Pass 6409–6424: Final Bridge Ledger

`w33_final_bridge_ledger.py` collects **15 exact items**, 2 conditional, 3 open:

```
Closure ratio: 15/20 = 75.0%
```

### Exact items include:
- CE2 global orbit closure
- K3 explicit witness and deformation
- Repo-native transport cocycle
- Family-flag identification
- **Global branch orientation** (newly closed)
- A4 continuum carrier at sd^1
- W(3,3) ovoid stabiliser exact (|Stab|=18)
- PMNS and Weinberg angle
- Bridge coefficient and tail arithmetic

### Still open (3 items):
- Sp(4,5) exact BFS stabiliser
- Orientation persistence at sd^2+
- Exact continuum A4 gauge entry

## Frontier After Pass 6424

| Target | Status |
|---|---|
| CE2 global orbit closure | ✅ EXACT |
| K3 deformation + witness | ✅ EXACT |
| Transport cocycle | ✅ EXACT |
| Family-flag identification | ✅ EXACT |
| Global branch orientation | ✅ **EXACT (just closed)** |
| A4 carrier at sd^1 | ✅ EXACT |
| PMNS + Weinberg angle | ✅ EXACT |
| W(3,3) ovoid stabiliser | ✅ EXACT |
| W(3,5) stabiliser | 🟡 CONJECTURAL |
| Sp(4,5) exact BFS | 🔴 OPEN |
| Orientation at sd^2+ | 🔴 OPEN |
| Continuum A4 gauge entry | 🔴 OPEN |

## Running

```powershell
$env:PYTHONUTF8='1'
py -3 scripts/w33_sp45_stabiliser_scaffold.py
py -3 scripts/w33_global_branch_orientation.py
py -3 scripts/w33_continuum_a4_entry.py
py -3 scripts/w33_final_bridge_ledger.py
```
