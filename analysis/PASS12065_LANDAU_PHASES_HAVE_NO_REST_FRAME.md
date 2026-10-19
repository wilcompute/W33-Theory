# Pass 12065: the Landau phases have no rest frame

Claude track. Builds on 12054 and 12059–12061.

## Second realisation

The 12054 Landau patterns were rebuilt in the matrix model, independently of the root model. They reproduce all five
exact invariants:

- event V15 (35/216, 25/108);
- event V24 (197/540, 77/540);
- staggered factorisation (1/8, 1/4);
- isotropic line (73/360, 59/180);
- signed hyperbolic line (11/96, 7/96), with signs (+,+,−,−).

## Phase symmetries against observers

| Phase | Symmetry | Observer orbits | Distinguished observers |
|---|---|---|---|
| event | 1296 | 36 | none |
| context | 1296 | 9 + 27 | the 9 whose sky contains the context |
| staggered factorisation | 576 | 12 + 24 | the 12 whose J swaps the two qutrit factors |
| signed hyperbolic line | 96 | 12 + 24 | the same 12 |

## Results

- **No Landau phase fixes an observer.** The point condensate is frame-free in every phase.
- **The event phase does not choose the clock.** Its symmetry Stab(p) contains order-3 elements outside the clock
  group, so it permutes the three clocks at p.
- Both the clock choice (12055) and rest frames (12060–12061) are tick-level order parameters, not point-level ones.

Producer: `analysis/w33_pass12065_landau_phases_have_no_rest_frame.py`.
