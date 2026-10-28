# Passes 12334–12339: both momentum towers, no radius minimum, and a new lead

Claude track. Producer: `analysis/w33_pass12334_to_12339_towers_potential_leads.py`.

## 12334: the e6-odd spectrum without patching the engine

The bicharacter predicts the brother from the parent, sector by sector. Checked on all 15 lineage variants: **15/15 exact**.

| sector | effect |
|---|---|
| even Z6 power | parent states with V_h·λ even stay; odd ones move to half-integer e6 momentum (52 fermions + 16 tachyons per variant) |
| odd Z6 power, odd e6 fixed-point label | bosons ↔ fermions |
| odd Z6 power, otherwise | unchanged |

A first version applied the parity rule to every sector and failed its control. The corrected rule was read off the sector table,
then confirmed.

## 12335: truncated one-loop potential along R₆

- **Input:** both towers. The integer tower has 366 bosonic and 144 fermionic components; the half tower has 288 fermionic and
  16 tachyonic components.
- **Shape:** V rises monotonically across the window, from −∞ as R → 0 to a finite −165.5 at the edge R = √(3/8). Beyond the edge it
  diverges. **There is no minimum**, and the radius runs to small R.
- **Controls:**
  - the τ₂ cutoff is stable;
  - the tachyon threshold sits exactly at R² = 3/8.
- **Truncation:** massive internal levels are omitted.

## 12336: winding-state projections

Not computed: there is no calibration for absolute phases. The R₅ bound remains an upper bound on the danger.

## 12337: the standalone note against the corpus

No collisions in the rediscovery guard, and no prior index entries.

## 12338: a new lead

Among the 99 tachyon-free parents, **17 carry three net (3,2) doublets** for some SU(3) × SU(2) choice. They fall into five lineages:
SM_2618, SM_2503, SM_574, SM_2913 and SM_1105 (v12, which 12180 met only as an interpolation endpoint). Their Scherk–Schwarz brothers
have at most 2.

**Unchecked:** hypercharge, the full SM structure, and tachyons away from the orbifold point.
