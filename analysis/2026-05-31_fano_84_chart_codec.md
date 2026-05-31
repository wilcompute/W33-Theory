# Fano 84 Chart-Codec

Date: 2026-05-31

This connects the Fano affine-chart atlas to the recurring flag-codec count

```text
84 = 7 * 12.
```

Previous theorem:

```text
Fano plane = atlas of seven AG(2,2) / tetrahedral charts.
```

Each chart is obtained by choosing one Fano line as the line at infinity. Its complement has four affine points and three infinity directions.

This theorem isolates the exact 84-state chart codec.

## Main object

A state consists of:

```text
1. a Fano line chosen as line at infinity;
2. an affine anchor in the four-point complement;
3. one of the three infinity directions.
```

Therefore:

```text
7 * 4 * 3 = 84.
```

Equivalently:

```text
84 = 7 * 12.
```

where each local chart contributes

```text
12 = 4 affine anchors * 3 directions.
```

## Direction from non-anchor edge

Inside a fixed chart, choose an affine anchor `p`.

The three non-anchor affine points `q` determine the three directions at infinity by the Fano line through `p` and `q`.

So each local state can also be read as:

```text
infinity line + ordered affine edge p -> q.
```

The verifier checks both descriptions are equivalent and produce 84 unique states:

```text
(infinity line, anchor, direction)
```

and

```text
(infinity line, anchor, non-anchor).
```

## Verified structure

The verifier checks:

```text
7 Fano points
7 Fano lines
7 affine charts
12 states per chart
84 total states
```

For every chart:

```text
4 affine anchors, each with 3 outgoing direction states
3 infinity directions, each appearing 4 times
```

Globally:

```text
each Fano point appears as an infinity-line member 36 times
each Fano point appears as an affine anchor 48 times
each Fano point appears as a direction 12 times
```

## Interpretation

The exact dictionary is:

```text
7:
    choice of Fano line as chart / infinity axis

12:
    local chart codec = 4 affine anchors * 3 directions

84:
    full Fano atlas chart-edge/direction codec
```

This gives a precise finite Fano-atlas realization of the recurring

```text
84 = 7 * 12
```

flag-codec count.

## Relation to Csaszar/Szilassi flags

Both Csaszar and Szilassi carry 84 flags in the working theory stack.

This theorem does not yet prove a canonical equality with those flags. It proves a natural Fano-atlas object of the same size:

```text
84 = seven Fano chart lines * twelve local chart states.
```

To identify this with Csaszar/Szilassi flags, the next step is an explicit labeling of the seven Fano axes by the seven toroidal codec axes and then a comparison of adjacency/chirality relations.

## Compressed theorem

```text
The Fano plane has seven affine AG(2,2) charts, one for each choice of line at infinity. Each chart has four affine anchors and three infinity directions, giving 12 local states. Across all seven charts this gives 84 states. Equivalently, each state is a Fano line at infinity plus an ordered affine edge in its complement. This realizes 84=7*12 as a Fano atlas chart-codec.
```

## Honest boundary

This proves the Fano 84 chart-codec. The next hard step is to map it onto the 84 flags of Csaszar/Szilassi and determine whether the Fano chart adjacency agrees with vertex-maximal or face-maximal toroidal adjacency.
