# BT1761-BT1763 execution summary

Executed the three requested next moves.

## BT1761: stabilizer/orientation fiber

Added `analysis/bt1761_stabilizer_orientation_fiber.py`.

BT1758 quotiented the one-position plateau by target Fano line. BT1761 resolves the next fiber layer for the incumbent nine automorphisms:

```text
target-line frequency = 4+2+2+1
orientation split = 5 cyclic / 4 reversed
line 4 orientation = 2 cyclic + 2 reversed
line 0 orientation = 1 cyclic + 1 reversed
line 2 orientation = 2 cyclic
line 3 orientation = 1 reversed
```

Boundary: classifies the incumbent orientation fiber; does not yet force the cyclic/reversed choices.

## BT1762: Coxeter-centralizer hexagon action

Added `analysis/bt1762_coxeter_centralizer_hexagon_action.py`.

BT1759 showed full Weyl simple reflections fragment most C^5 hexagons. BT1762 records the verified whole-hexagon action that remains:

```text
<C> has order 30
<C^5> has size 6 and fixes each C^5 hexagon as a set
<C>/<C^5> = C5 acts on the 40 hexagons
C acts as eight 5-cycles on the hexagons
```

Boundary: verified Coxeter-centralizer action; a larger Coxeter normalizer remains to be explicitly generated and checked.

## BT1763: self-frame selector uniqueness/falsifier

Added `analysis/bt1763_self_frame_selector_uniqueness.py`.

The BT1760 self-frame cross alone does not force the selector. Fixing the four line-4 cross entries plus the 4+2+2+1 multiset leaves:

```text
30 completions
```

Adding minimal Hesse/Q4 boundary rules collapses those 30 completions to the observed selector:

```text
[[0,4,0],
 [4,4,2],
 [2,4,3]]
```

Boundary: the minimal boundary rules are explicit; the next task is deriving them directly from 64-bit/Q4 geometry.
