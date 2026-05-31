# Fano Affine Chart Atlas

Date: 2026-05-30

This globalizes the affine Fano completion theorem.

Previous theorem:

```text
PG(1,3)/tetrahedral four-point geometry
```

can be modeled as one affine chart

```text
AG(2,2)
```

inside the Fano plane, with the missing three points forming the line at infinity.

This theorem shows that the full Fano plane is an atlas of such tetrahedral affine charts.

## Main result

In the Fano plane, every line can serve as the line at infinity.

Removing that line leaves:

```text
4 affine points
```

and the remaining six lines become the affine lines of

```text
AG(2,2).
```

Those six affine lines split into:

```text
3 parallel classes of 2 lines.
```

Each parallel class meets at one point on the chosen line at infinity.

Therefore:

```text
Fano plane = seven AG(2,2) affine/tetrahedral charts.
```

There is one chart for each choice of line at infinity.

## Verified Fano facts

The verifier checks the full Fano plane:

```text
7 points
7 lines
3 points per line
3 lines through each point
each pair lies on exactly one line
```

Then, for each of the seven choices of infinity line, it checks:

```text
4 affine points
6 affine line segments
3 parallel classes
2 affine lines per parallel class
```

So every Fano line defines a valid tetrahedral `AG(2,2)` chart.

## Anchor changes inside a chart

Inside a fixed chart, choose an affine anchor.

The three non-anchor affine points determine the three directions on the selected line at infinity.

The verifier checks that every anchor in every chart sees all three infinity directions.

Changing the anchor inside a fixed chart is an affine translation of `AG(2,2)`.

So:

```text
changing anchor = translation inside one tetrahedral chart
changing infinity line = transition to another Fano affine chart
```

## Meaning for the global Fano wedge-dot codec

The global seven-axis Fano wedge-dot codec can now be read as an atlas:

```text
7 Fano lines = 7 possible infinity lines
```

Each choice gives:

```text
4 affine/tetrahedral points + 3 infinity/direction points.
```

This directly connects:

```text
PG(1,3) / tetrahedron / AG(2,2)
```

with the global seven-point Fano plane.

The local C3 qutrit triangle is the cyclic orientation of the chosen infinity line.

## Compressed theorem

```text
Every Fano line can be chosen as the line at infinity. Its complement is an AG(2,2) affine chart with four points and six affine lines grouped into three parallel classes. Inside a chart, changing anchor is affine translation; changing the infinity line changes the chart. Thus the seven-point Fano wedge-dot codec is an atlas of seven tetrahedral/AG(2,2) charts.
```

## Honest boundary

This proves the chart-atlas structure. The next hard step is to connect these seven affine charts to the seven Csaszar/Szilassi codec axes and verify that the earlier 7*12=84 local flag codec can be realized as seven Fano chart lines times the 12-state line codec.
